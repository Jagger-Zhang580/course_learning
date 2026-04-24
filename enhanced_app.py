#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版简历筛选工具 Web应用
"""

import os
import json
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from enhanced_screener import EnhancedResumeScreener, result_to_dict
from skill_weight import SkillWeightManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# 允许的文件格式
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}

# 初始化筛选器
screener = EnhancedResumeScreener(
    use_bert=False,  # BERT需要大量资源，默认关闭
    use_ml=True
)

# 技能配置管理器
skill_manager = SkillWeightManager()


def allowed_file(filename):
    """检查文件格式"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """主页"""
    return render_template('enhanced_index.html')


@app.route('/api/screen', methods=['POST'])
def screen_resumes():
    """筛选多个简历（文本输入）"""
    try:
        data = request.get_json()
        
        job_description = data.get('job_description', '')
        resumes = data.get('resumes', [])
        skill_template = data.get('skill_template', '')
        
        if not job_description:
            return jsonify({'error': '请提供职位描述'}), 400
        
        if not resumes:
            return jsonify({'error': '请提供至少一份简历'}), 400
        
        # 设置技能配置
        if skill_template:
            try:
                screener.set_skill_config_by_template(skill_template)
            except ValueError:
                pass  # 使用默认配置
        
        # 准备简历数据
        resume_data = [
            {'id': f'简历{i+1}', 'text': text}
            for i, text in enumerate(resumes)
            if text.strip()
        ]
        
        if not resume_data:
            return jsonify({'error': '没有有效的简历内容'}), 400
        
        # 执行筛选
        results = screener.screen_multiple_resumes(resume_data, job_description)
        
        # 转换为字典
        formatted_results = [result_to_dict(r) for r in results]
        
        return jsonify({
            'success': True,
            'results': formatted_results,
            'total': len(formatted_results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """上传并筛选简历文件"""
    try:
        job_description = request.form.get('job_description', '')
        skill_template = request.form.get('skill_template', '')
        
        if not job_description:
            return jsonify({'error': '请提供职位描述'}), 400
        
        # 检查文件
        if 'files' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 设置技能配置
        if skill_template:
            try:
                screener.set_skill_config_by_template(skill_template)
            except ValueError:
                pass
        
        # 处理文件
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    result = screener.screen_from_file(filepath, job_description)
                    results.append(result_to_dict(result))
                except Exception as e:
                    print(f"处理文件 {filename} 失败: {e}")
                finally:
                    # 清理临时文件
                    if os.path.exists(filepath):
                        os.unlink(filepath)
        
        if not results:
            return jsonify({'error': '没有成功处理任何文件'}), 400
        
        # 按得分排序
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_single():
    """分析单个简历"""
    try:
        data = request.get_json()
        
        job_description = data.get('job_description', '')
        resume = data.get('resume', '')
        skill_template = data.get('skill_template', '')
        
        if not job_description or not resume:
            return jsonify({'error': '请提供职位描述和简历内容'}), 400
        
        # 设置技能配置
        if skill_template:
            try:
                screener.set_skill_config_by_template(skill_template)
            except ValueError:
                pass
        
        # 执行分析
        result = screener.screen_resume(resume, job_description)
        
        return jsonify({
            'success': True,
            'result': result_to_dict(result)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """获取可用的技能配置模板"""
    templates = screener.get_available_templates()
    
    template_info = []
    for name in templates:
        config = skill_manager.get_config(name)
        if config:
            template_info.append({
                'name': name,
                'job_title': config.job_title,
                'skills': [
                    {
                        'name': s.name,
                        'weight': s.weight,
                        'required': s.is_mandatory
                    }
                    for s in config.skills
                ]
            })
    
    return jsonify({
        'success': True,
        'templates': template_info
    })


@app.route('/api/custom-template', methods=['POST'])
def create_custom_template():
    """创建自定义技能配置"""
    try:
        data = request.get_json()
        
        job_title = data.get('job_title', '')
        skills = data.get('skills', [])
        
        if not job_title or not skills:
            return jsonify({'error': '请提供职位名称和技能列表'}), 400
        
        from skill_weight import create_custom_config
        
        # 转换技能数据
        skill_list = [
            (s['name'], s['weight'], s.get('required', False))
            for s in skills
        ]
        
        config = create_custom_config(job_title, skill_list)
        
        # 保存配置
        config_name = f"custom_{job_title.lower().replace(' ', '_')}"
        skill_manager.add_config(config_name, config)
        screener.set_skill_config(config)
        
        return jsonify({
            'success': True,
            'config_name': config_name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'features': {
            'bert': screener.use_bert,
            'ml': screener.use_ml,
            'file_upload': True
        }
    })


if __name__ == '__main__':
    # 创建模板目录
    os.makedirs('templates', exist_ok=True)
    
    print("启动增强版简历筛选工具...")
    print("访问 http://localhost:5001 使用Web界面")
    
    app.run(debug=True, host='0.0.0.0', port=5001)