#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版简历筛选工具
集成BERT、技能权重、文件解析、机器学习等功能
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

# 导入各模块
from resume_screener import ResumeScreener
from skill_weight import SkillWeightManager, SkillConfig
from file_parser import ResumeFileParser, extract_resume_sections
from ml_classifier import ResumeClassifier, ResumeQualityPredictor, MatchPredictor

# 可选导入BERT模块
try:
    from bert_analyzer import BERTSemanticAnalyzer, SemanticResumeMatcher
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False


@dataclass
class ScreeningResult:
    """筛选结果"""
    resume_id: str
    final_score: float
    tfidf_score: float
    semantic_score: float
    skill_score: float
    quality_score: float
    job_category: str
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    sections: Dict[str, str]


class EnhancedResumeScreener:
    """增强版简历筛选器"""
    
    def __init__(
        self,
        use_bert: bool = True,
        use_ml: bool = True,
        skill_config: Optional[SkillConfig] = None
    ):
        """
        初始化增强版筛选器
        
        Args:
            use_bert: 是否使用BERT语义分析
            use_ml: 是否使用机器学习
            skill_config: 技能权重配置
        """
        # 基础筛选器
        self.base_screener = ResumeScreener()
        
        # 文件解析器
        self.file_parser = ResumeFileParser()
        
        # 技能权重管理器
        self.skill_manager = SkillWeightManager()
        self.skill_config = skill_config
        
        # BERT语义分析器
        self.use_bert = use_bert and BERT_AVAILABLE
        self.semantic_matcher = None
        if self.use_bert:
            try:
                self.semantic_matcher = SemanticResumeMatcher(use_bert=True)
            except Exception as e:
                print(f"BERT初始化失败: {e}")
                self.use_bert = False
        
        # 机器学习组件
        self.use_ml = use_ml
        self.classifier = None
        self.quality_predictor = None
        self.match_predictor = None
        
        if use_ml:
            try:
                self.classifier = ResumeClassifier()
                self.quality_predictor = ResumeQualityPredictor()
                self.match_predictor = MatchPredictor()
            except Exception as e:
                print(f"ML组件初始化失败: {e}")
                self.use_ml = False
    
    def screen_resume(
        self,
        resume_text: str,
        job_description: str,
        resume_id: str = "resume_1"
    ) -> ScreeningResult:
        """
        筛选单个简历
        
        Args:
            resume_text: 简历文本
            job_description: 职位描述
            resume_id: 简历ID
            
        Returns:
            筛选结果
        """
        # 1. 基础TF-IDF匹配
        base_result = self.base_screener.match_resume_to_job(
            resume_text, job_description
        )
        tfidf_score = base_result['final_score']
        
        # 2. BERT语义匹配
        semantic_score = 0.0
        if self.use_bert and self.semantic_matcher:
            semantic_result = self.semantic_matcher.calculate_semantic_match(
                resume_text, job_description
            )
            semantic_score = semantic_result.get('overall_score', 0.0)
        
        # 3. 技能权重评分
        skill_score = 0.0
        matched_skills = []
        missing_skills = []
        
        if self.skill_config:
            skill_result = self.skill_manager.calculate_skill_score(
                resume_text, self.skill_config
            )
            skill_score = skill_result['final_score']
            matched_skills = skill_result['matched_skills']
            missing_skills = [
                s for s, v in skill_result['skill_scores'].items()
                if not v['found']
            ]
        
        # 4. 简历质量评估
        quality_score = 0.0
        suggestions = []
        
        if self.quality_predictor:
            quality_result = self.quality_predictor.predict_quality(resume_text)
            quality_score = quality_result['total_score']
            suggestions = quality_result['suggestions']
        
        # 5. 职位分类
        job_category = "未分类"
        if self.classifier:
            category_result = self.classifier.predict(job_description)
            job_category = category_result['category']
        
        # 6. 提取简历各部分
        sections = extract_resume_sections(resume_text)
        
        # 7. 计算综合得分
        final_score = self._calculate_final_score(
            tfidf_score,
            semantic_score,
            skill_score,
            quality_score
        )
        
        return ScreeningResult(
            resume_id=resume_id,
            final_score=round(final_score, 4),
            tfidf_score=round(tfidf_score, 4),
            semantic_score=round(semantic_score, 4),
            skill_score=round(skill_score, 4),
            quality_score=round(quality_score, 4),
            job_category=job_category,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            suggestions=suggestions,
            sections=sections
        )
    
    def _calculate_final_score(
        self,
        tfidf_score: float,
        semantic_score: float,
        skill_score: float,
        quality_score: float
    ) -> float:
        """计算综合得分"""
        if self.use_bert and self.use_ml:
            # 完整模式：四个分数加权
            return (
                tfidf_score * 0.2 +
                semantic_score * 0.3 +
                skill_score * 0.35 +
                quality_score * 0.15
            )
        elif self.use_bert:
            # 有BERT但无ML
            return (
                tfidf_score * 0.3 +
                semantic_score * 0.4 +
                quality_score * 0.3
            )
        elif self.use_ml:
            # 有ML但无BERT
            return (
                tfidf_score * 0.3 +
                skill_score * 0.5 +
                quality_score * 0.2
            )
        else:
            # 基础模式
            return tfidf_score
    
    def screen_from_file(
        self,
        file_path: str,
        job_description: str
    ) -> ScreeningResult:
        """
        从文件筛选简历
        
        Args:
            file_path: 文件路径
            job_description: 职位描述
            
        Returns:
            筛选结果
        """
        # 解析文件
        parse_result = self.file_parser.parse(file_path)
        
        if not parse_result['success']:
            raise ValueError(f"文件解析失败: {parse_result['error']}")
        
        resume_text = parse_result['text']
        resume_id = Path(file_path).stem
        
        return self.screen_resume(resume_text, job_description, resume_id)
    
    def screen_multiple_resumes(
        self,
        resumes: List[Dict],
        job_description: str
    ) -> List[ScreeningResult]:
        """
        筛选多个简历
        
        Args:
            resumes: 简历列表 [{'id': str, 'text': str}, ...]
            job_description: 职位描述
            
        Returns:
            筛选结果列表（按得分排序）
        """
        results = []
        
        for resume in resumes:
            result = self.screen_resume(
                resume_text=resume['text'],
                job_description=job_description,
                resume_id=resume.get('id', f'resume_{len(results)+1}')
            )
            results.append(result)
        
        # 按综合得分排序
        results.sort(key=lambda x: x.final_score, reverse=True)
        
        return results
    
    def screen_from_directory(
        self,
        directory: str,
        job_description: str
    ) -> List[ScreeningResult]:
        """
        从目录批量筛选简历
        
        Args:
            directory: 目录路径
            job_description: 职位描述
            
        Returns:
            筛选结果列表
        """
        results = []
        directory = Path(directory)
        
        if not directory.is_dir():
            raise ValueError(f"目录不存在: {directory}")
        
        for file_path in directory.iterdir():
            if file_path.suffix.lower() in ResumeFileParser.SUPPORTED_FORMATS:
                try:
                    result = self.screen_from_file(
                        str(file_path),
                        job_description
                    )
                    results.append(result)
                except Exception as e:
                    print(f"处理文件 {file_path} 失败: {e}")
        
        # 排序
        results.sort(key=lambda x: x.final_score, reverse=True)
        
        return results
    
    def set_skill_config(self, config: SkillConfig):
        """设置技能配置"""
        self.skill_config = config
    
    def set_skill_config_by_template(self, template_name: str):
        """使用预定义模板设置技能配置"""
        config = self.skill_manager.get_config(template_name)
        if config:
            self.skill_config = config
        else:
            raise ValueError(f"未找到模板: {template_name}")
    
    def get_available_templates(self) -> List[str]:
        """获取可用的技能配置模板"""
        return self.skill_manager.list_configs()
    
    def generate_report(self, results: List[ScreeningResult]) -> str:
        """生成筛选报告"""
        report = []
        report.append("=" * 60)
        report.append("简历筛选报告")
        report.append("=" * 60)
        report.append(f"共筛选 {len(results)} 份简历\n")
        
        for i, result in enumerate(results, 1):
            report.append(f"排名 {i}: {result.resume_id}")
            report.append(f"  综合得分: {result.final_score:.2%}")
            report.append(f"  TF-IDF相似度: {result.tfidf_score:.2%}")
            report.append(f"  语义相似度: {result.semantic_score:.2%}")
            report.append(f"  技能匹配度: {result.skill_score:.2%}")
            report.append(f"  简历质量: {result.quality_score:.2%}")
            report.append(f"  职位类别: {result.job_category}")
            
            if result.matched_skills:
                report.append(f"  匹配技能: {', '.join(result.matched_skills)}")
            
            if result.missing_skills:
                report.append(f"  缺失技能: {', '.join(result.missing_skills)}")
            
            if result.suggestions:
                report.append(f"  改进建议:")
                for suggestion in result.suggestions:
                    report.append(f"    - {suggestion}")
            
            report.append("-" * 40)
        
        return "\n".join(report)


def result_to_dict(result: ScreeningResult) -> Dict:
    """将结果转换为字典"""
    return {
        "resume_id": result.resume_id,
        "final_score": result.final_score,
        "tfidf_score": result.tfidf_score,
        "semantic_score": result.semantic_score,
        "skill_score": result.skill_score,
        "quality_score": result.quality_score,
        "job_category": result.job_category,
        "matched_skills": result.matched_skills,
        "missing_skills": result.missing_skills,
        "suggestions": result.suggestions,
        "sections": result.sections
    }


# 示例用法
if __name__ == "__main__":
    # 创建筛选器
    screener = EnhancedResumeScreener(
        use_bert=False,  # 设置为True以启用BERT（需要安装transformers）
        use_ml=True
    )
    
    # 设置技能配置
    screener.set_skill_config_by_template("python_developer")
    
    # 示例简历
    resume = """
    张三
    Python开发工程师
    电话：13800138000
    邮箱：zhangsan@example.com
    
    教育背景
    2015-2019  北京大学  计算机科学与技术  本科
    
    工作经验
    2019-至今  某科技公司  Python开发工程师
    - 负责公司核心业务系统的开发和维护
    - 使用Django框架开发Web应用
    - 优化数据库查询性能，提升系统响应速度30%
    - 参与微服务架构设计和实现
    
    专业技能
    - 熟练掌握Python编程语言
    - 熟悉Django、Flask框架
    - 了解MySQL、Redis数据库
    - 熟悉Git版本控制
    - 有Docker容器化部署经验
    - 了解Linux操作系统
    """
    
    # 职位描述
    job = """
    职位：Python开发工程师
    要求：
    1. 熟练掌握Python编程语言
    2. 熟悉Django或Flask框架
    3. 了解MySQL、Redis等数据库
    4. 有良好的代码习惯和文档编写能力
    5. 具备团队协作精神
    6. 2年以上开发经验
    """
    
    # 筛选简历
    result = screener.screen_resume(resume, job)
    
    print("筛选结果:")
    print(f"综合得分: {result.final_score:.2%}")
    print(f"TF-IDF相似度: {result.tfidf_score:.2%}")
    print(f"技能匹配度: {result.skill_score:.2%}")
    print(f"简历质量: {result.quality_score:.2%}")
    print(f"匹配技能: {result.matched_skills}")
    print(f"缺失技能: {result.missing_skills}")
    print(f"改进建议: {result.suggestions}")