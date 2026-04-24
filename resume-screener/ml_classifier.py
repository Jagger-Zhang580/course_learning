#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习分类模型模块
用于简历分类和匹配度预测
"""

import json
import pickle
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter
import re
import os

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import classification_report, accuracy_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import LabelEncoder
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("警告: scikit-learn未安装，机器学习功能将不可用")


class ResumeClassifier:
    """简历分类器"""
    
    # 职位类别
    JOB_CATEGORIES = [
        "软件开发",
        "数据分析",
        "产品经理",
        "UI/UX设计",
        "测试工程师",
        "运维工程师",
        "人工智能",
        "市场营销",
        "人力资源",
        "财务会计",
        "其他"
    ]
    
    # 每个类别的关键词
    CATEGORY_KEYWORDS = {
        "软件开发": [
            "python", "java", "javascript", "c++", "开发", "编程", "代码",
            "框架", "django", "spring", "react", "vue", "前端", "后端",
            "全栈", "算法", "数据结构", "git", "github"
        ],
        "数据分析": [
            "数据分析", "数据挖掘", "sql", "数据库", "统计", "excel",
            "tableau", "powerbi", "python", "r语言", "机器学习",
            "数据可视化", "报表", "指标", "bi"
        ],
        "产品经理": [
            "产品", "需求", "用户", "体验", "原型", "prd", "mrd",
            "竞品分析", "用户研究", "产品设计", "项目管理", "agile",
            "scrum", "敏捷", "迭代", "版本"
        ],
        "UI/UX设计": [
            "设计", "ui", "ux", "用户界面", "交互", "视觉",
            "photoshop", "illustrator", "sketch", "figma",
            "原型", "设计规范", "色彩", "排版"
        ],
        "测试工程师": [
            "测试", "qa", "质量", "自动化测试", "单元测试",
            "功能测试", "性能测试", "接口测试", "selenium",
            "junit", "pytest", "bug", "缺陷", "回归"
        ],
        "运维工程师": [
            "运维", "devops", "linux", "服务器", "网络",
            "docker", "kubernetes", "k8s", "ci/cd", "监控",
            "部署", "脚本", "shell", "ansible", "jenkins"
        ],
        "人工智能": [
            "机器学习", "深度学习", "神经网络", "nlp", "cv",
            "tensorflow", "pytorch", "模型", "算法", "训练",
            "自然语言", "计算机视觉", "推荐系统", "ai"
        ],
        "市场营销": [
            "营销", "市场", "推广", "品牌", "广告", "新媒体",
            "运营", "用户增长", "活动策划", "内容", "社媒",
            "seo", "sem", "投放", "转化"
        ],
        "人力资源": [
            "人力资源", "hr", "招聘", "培训", "绩效", "薪酬",
            "员工关系", "组织发展", "人才", "面试", "猎头",
            "人事", "劳动关系", "企业文化"
        ],
        "财务会计": [
            "财务", "会计", "审计", "税务", "成本", "预算",
            "报表", "核算", "出纳", "总账", "应收", "应付",
            "财务分析", "cpa", "中级职称"
        ],
    }
    
    def __init__(self, model_type: str = "random_forest"):
        """
        初始化分类器
        
        Args:
            model_type: 模型类型 ('random_forest', 'gradient_boosting', 'svm')
        """
        if not ML_AVAILABLE:
            raise ImportError("scikit-learn未安装")
        
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words=None
        )
        self.label_encoder = LabelEncoder()
        self.model = self._create_model(model_type)
        self.is_trained = False
    
    def _create_model(self, model_type: str):
        """创建模型"""
        if model_type == "random_forest":
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == "gradient_boosting":
            return GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        elif model_type == "svm":
            return SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            )
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")
    
    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """
        训练模型
        
        Args:
            texts: 文本列表
            labels: 标签列表
            
        Returns:
            训练结果
        """
        # 编码标签
        encoded_labels = self.label_encoder.fit_transform(labels)
        
        # 向量化文本
        X = self.vectorizer.fit_transform(texts)
        
        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            X, encoded_labels, test_size=0.2, random_state=42
        )
        
        # 训练模型
        self.model.fit(X_train, y_train)
        
        # 评估模型
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # 交叉验证
        cv_scores = cross_val_score(self.model, X, encoded_labels, cv=5)
        
        self.is_trained = True
        
        return {
            "accuracy": accuracy,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "report": classification_report(
                y_test, y_pred,
                target_names=self.label_encoder.classes_
            )
        }
    
    def predict(self, text: str) -> Dict:
        """
        预测文本类别
        
        Args:
            text: 输入文本
            
        Returns:
            预测结果
        """
        if not self.is_trained:
            # 使用基于关键词的规则分类
            return self._rule_based_classify(text)
        
        # 向量化
        X = self.vectorizer.transform([text])
        
        # 预测
        pred = self.model.predict(X)[0]
        proba = self.model.predict_proba(X)[0]
        
        # 解码标签
        category = self.label_encoder.inverse_transform([pred])[0]
        
        # 获取所有类别的概率
        probabilities = {
            self.label_encoder.inverse_transform([i])[0]: float(p)
            for i, p in enumerate(proba)
        }
        
        return {
            "category": category,
            "confidence": float(max(proba)),
            "probabilities": probabilities
        }
    
    def _rule_based_classify(self, text: str) -> Dict:
        """基于规则的分类（无需训练）"""
        text_lower = text.lower()
        
        scores = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[category] = score
        
        if not scores or max(scores.values()) == 0:
            return {
                "category": "其他",
                "confidence": 0.0,
                "probabilities": {"其他": 1.0}
            }
        
        # 归一化
        total = sum(scores.values())
        probabilities = {k: v / total for k, v in scores.items()}
        
        # 获取最高分的类别
        category = max(scores, key=scores.get)
        confidence = probabilities[category]
        
        return {
            "category": category,
            "confidence": confidence,
            "probabilities": probabilities
        }
    
    def save(self, filepath: str):
        """保存模型"""
        data = {
            "model": self.model,
            "vectorizer": self.vectorizer,
            "label_encoder": self.label_encoder,
            "model_type": self.model_type,
            "is_trained": self.is_trained
        }
        joblib.dump(data, filepath)
    
    def load(self, filepath: str):
        """加载模型"""
        data = joblib.load(filepath)
        self.model = data["model"]
        self.vectorizer = data["vectorizer"]
        self.label_encoder = data["label_encoder"]
        self.model_type = data["model_type"]
        self.is_trained = data["is_trained"]


class ResumeQualityPredictor:
    """简历质量预测器"""
    
    # 质量特征
    QUALITY_FEATURES = [
        "length_score",           # 长度得分
        "structure_score",        # 结构得分
        "keyword_density",        # 关键词密度
        "contact_info_score",     # 联系信息得分
        "education_score",        # 教育信息得分
        "experience_score",       # 经验信息得分
        "skill_score",            # 技能信息得分
    ]
    
    def __init__(self):
        self.feature_weights = {
            "length_score": 0.10,
            "structure_score": 0.15,
            "keyword_density": 0.15,
            "contact_info_score": 0.10,
            "education_score": 0.15,
            "experience_score": 0.20,
            "skill_score": 0.15,
        }
    
    def predict_quality(self, resume_text: str) -> Dict:
        """
        预测简历质量
        
        Args:
            resume_text: 简历文本
            
        Returns:
            质量评估结果
        """
        features = self._extract_features(resume_text)
        
        # 计算加权得分
        total_score = sum(
            features[f] * self.feature_weights[f]
            for f in self.QUALITY_FEATURES
        )
        
        # 确定质量等级
        if total_score >= 0.8:
            quality_level = "优秀"
        elif total_score >= 0.6:
            quality_level = "良好"
        elif total_score >= 0.4:
            quality_level = "一般"
        else:
            quality_level = "需要改进"
        
        # 生成改进建议
        suggestions = self._generate_suggestions(features)
        
        return {
            "total_score": round(total_score, 2),
            "quality_level": quality_level,
            "features": features,
            "suggestions": suggestions
        }
    
    def _extract_features(self, text: str) -> Dict[str, float]:
        """提取质量特征"""
        features = {}
        
        # 长度得分 (200-2000字为最佳)
        text_len = len(text)
        if text_len < 200:
            features["length_score"] = text_len / 200 * 0.5
        elif text_len <= 2000:
            features["length_score"] = 0.5 + (text_len - 200) / 1800 * 0.5
        else:
            features["length_score"] = max(0.5, 1 - (text_len - 2000) / 5000)
        
        # 结构得分（检查是否有分段和标题）
        lines = text.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        if len(non_empty_lines) >= 10:
            features["structure_score"] = 1.0
        elif len(non_empty_lines) >= 5:
            features["structure_score"] = 0.7
        else:
            features["structure_score"] = 0.3
        
        # 关键词密度
        keywords = ["经验", "技能", "项目", "工作", "教育", "学历", "专业"]
        keyword_count = sum(1 for kw in keywords if kw in text)
        features["keyword_density"] = min(1.0, keyword_count / len(keywords))
        
        # 联系信息得分
        contact_patterns = [
            r'\d{11}',  # 手机号
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 邮箱
            r'1[3-9]\d{9}',  # 中国手机号
        ]
        contact_count = sum(
            1 for pattern in contact_patterns
            if re.search(pattern, text)
        )
        features["contact_info_score"] = min(1.0, contact_count / 2)
        
        # 教育信息得分
        edu_keywords = ["大学", "本科", "硕士", "博士", "专科", "学历", "专业", "毕业"]
        edu_count = sum(1 for kw in edu_keywords if kw in text)
        features["education_score"] = min(1.0, edu_count / 4)
        
        # 经验信息得分
        exp_keywords = ["年经验", "工作经验", "项目经验", "负责", "参与", "完成"]
        exp_count = sum(1 for kw in exp_keywords if kw in text)
        features["experience_score"] = min(1.0, exp_count / 4)
        
        # 技能信息得分
        skill_keywords = ["熟练", "精通", "掌握", "熟悉", "了解", "技能"]
        skill_count = sum(1 for kw in skill_keywords if kw in text)
        features["skill_score"] = min(1.0, skill_count / 4)
        
        return features
    
    def _generate_suggestions(self, features: Dict[str, float]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if features["length_score"] < 0.5:
            suggestions.append("简历内容过短，建议补充更多详细信息")
        elif features["length_score"] < 0.7:
            suggestions.append("简历内容可以更丰富一些")
        
        if features["structure_score"] < 0.5:
            suggestions.append("建议使用清晰的段落和标题组织内容")
        
        if features["contact_info_score"] < 0.5:
            suggestions.append("请确保包含完整的联系方式（手机和邮箱）")
        
        if features["education_score"] < 0.5:
            suggestions.append("建议补充教育背景信息")
        
        if features["experience_score"] < 0.5:
            suggestions.append("建议详细描述工作经验和项目经历")
        
        if features["skill_score"] < 0.5:
            suggestions.append("建议列出专业技能和熟练程度")
        
        if not suggestions:
            suggestions.append("简历质量良好，继续保持！")
        
        return suggestions


class MatchPredictor:
    """匹配度预测器"""
    
    def __init__(self):
        if ML_AVAILABLE:
            self.model = GradientBoostingClassifier(
                n_estimators=50,
                max_depth=3,
                random_state=42
            )
            self.is_trained = False
        else:
            self.model = None
    
    def extract_match_features(
        self,
        resume_text: str,
        job_text: str
    ) -> np.ndarray:
        """
        提取匹配特征
        
        Args:
            resume_text: 简历文本
            job_text: 职位描述
            
        Returns:
            特征向量
        """
        features = []
        
        # 1. 文本长度比
        resume_len = len(resume_text)
        job_len = len(job_text)
        features.append(min(resume_len / max(job_len, 1), 5))
        
        # 2. 关键词重叠度
        resume_words = set(self._tokenize(resume_text))
        job_words = set(self._tokenize(job_text))
        
        if job_words:
            overlap = len(resume_words & job_words)
            features.append(overlap / len(job_words))
        else:
            features.append(0)
        
        # 3. 技能匹配度
        tech_keywords = [
            "python", "java", "javascript", "sql", "html", "css",
            "react", "vue", "angular", "node", "django", "spring",
            "docker", "kubernetes", "git", "linux", "aws", "azure"
        ]
        
        resume_lower = resume_text.lower()
        job_lower = job_text.lower()
        
        resume_tech = sum(1 for kw in tech_keywords if kw in resume_lower)
        job_tech = sum(1 for kw in tech_keywords if kw in job_lower)
        
        if job_tech > 0:
            features.append(min(resume_tech / job_tech, 1))
        else:
            features.append(0.5)
        
        # 4. 经验关键词匹配
        exp_keywords = ["年经验", "工作经验", "项目经验", "负责", "开发", "设计"]
        resume_exp = sum(1 for kw in exp_keywords if kw in resume_text)
        job_exp = sum(1 for kw in exp_keywords if kw in job_text)
        
        if job_exp > 0:
            features.append(min(resume_exp / job_exp, 1))
        else:
            features.append(0.5)
        
        # 5. 教育关键词匹配
        edu_keywords = ["本科", "硕士", "博士", "计算机", "软件", "信息"]
        resume_edu = sum(1 for kw in edu_keywords if kw in resume_text)
        features.append(min(resume_edu / 3, 1))
        
        return np.array(features)
    
    def _tokenize(self, text: str) -> List[str]:
        """简单分词"""
        # 移除标点
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        # 分割
        words = text.lower().split()
        # 过滤短词
        return [w for w in words if len(w) > 1]
    
    def predict_match(
        self,
        resume_text: str,
        job_text: str
    ) -> Dict:
        """
        预测匹配度
        
        Args:
            resume_text: 简历文本
            job_text: 职位描述
            
        Returns:
            预测结果
        """
        features = self.extract_match_features(resume_text, job_text)
        
        # 基于规则的匹配度计算
        match_score = (
            features[0] * 0.1 +  # 长度比
            features[1] * 0.3 +  # 关键词重叠
            features[2] * 0.3 +  # 技能匹配
            features[3] * 0.2 +  # 经验匹配
            features[4] * 0.1    # 教育匹配
        )
        
        # 归一化到0-1
        match_score = min(1.0, match_score)
        
        # 确定匹配等级
        if match_score >= 0.8:
            match_level = "高度匹配"
        elif match_score >= 0.6:
            match_level = "良好匹配"
        elif match_score >= 0.4:
            match_level = "一般匹配"
        else:
            match_level = "匹配度低"
        
        return {
            "match_score": round(match_score, 2),
            "match_level": match_level,
            "features": {
                "length_ratio": round(features[0], 2),
                "keyword_overlap": round(features[1], 2),
                "skill_match": round(features[2], 2),
                "experience_match": round(features[3], 2),
                "education_match": round(features[4], 2)
            }
        }


# 示例用法
if __name__ == "__main__":
    # 测试分类器
    classifier = ResumeClassifier()
    
    resume = """
    张三，Python开发工程师，3年工作经验
    熟练掌握Python、Django框架
    熟悉MySQL、Redis数据库
    有良好的代码习惯和团队协作能力
    """
    
    result = classifier.predict(resume)
    print(f"职位分类: {result['category']}")
    print(f"置信度: {result['confidence']:.2%}")
    
    # 测试质量预测
    predictor = ResumeQualityPredictor()
    quality = predictor.predict_quality(resume)
    print(f"\n简历质量: {quality['quality_level']}")
    print(f"得分: {quality['total_score']:.2%}")
    print(f"建议: {quality['suggestions']}")