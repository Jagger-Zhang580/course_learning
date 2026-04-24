#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历筛选工具Web界面
"""

from flask import Flask, render_template, request, jsonify
from resume_screener import ResumeScreener
import json

app = Flask(__name__)
screener = ResumeScreener()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/screen', methods=['POST'])
def screen_resumes():
    """API接口：筛选简历"""
    try:
        data = request.get_json()
        
        job_description = data.get('job_description', '')
        resumes = data.get('resumes', [])
        
        if not job_description or not resumes:
            return jsonify({'error': '请提供职位描述和简历内容'}), 400
        
        # 执行筛选
        results = screener.screen_multiple_resumes(resumes, job_description)
        
        # 格式化结果
        formatted_results = []
        for i, result in enumerate(results):
            formatted_results.append({
                'rank': i + 1,
                'resume_id': result['resume_id'],
                'final_score': round(result['final_score'] * 100, 2),
                'similarity_score': round(result['similarity_score'] * 100, 2),
                'keyword_match_score': round(result['keyword_match_score'] * 100, 2),
                'resume_keywords': [kw[0] for kw in result['resume_keywords']],
                'job_keywords': [kw[0] for kw in result['job_keywords']]
            })
        
        return jsonify({
            'success': True,
            'results': formatted_results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_single():
    """API接口：分析单个简历"""
    try:
        data = request.get_json()
        
        job_description = data.get('job_description', '')
        resume = data.get('resume', '')
        
        if not job_description or not resume:
            return jsonify({'error': '请提供职位描述和简历内容'}), 400
        
        # 执行分析
        result = screener.match_resume_to_job(resume, job_description)
        
        return jsonify({
            'success': True,
            'result': {
                'final_score': round(result['final_score'] * 100, 2),
                'similarity_score': round(result['similarity_score'] * 100, 2),
                'keyword_match_score': round(result['keyword_match_score'] * 100, 2),
                'resume_keywords': [kw[0] for kw in result['resume_keywords']],
                'job_keywords': [kw[0] for kw in result['job_keywords']]
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)