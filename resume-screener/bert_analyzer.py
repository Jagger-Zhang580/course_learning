#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BERT语义理解模块
使用预训练BERT模型进行简历语义分析
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import json
import os

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False
    print("警告: transformers或torch未安装，BERT功能将不可用")


class BERTSemanticAnalyzer:
    """BERT语义分析器"""
    
    def __init__(self, model_name: str = "bert-base-chinese"):
        """
        初始化BERT模型
        
        Args:
            model_name: 预训练模型名称，默认使用中文BERT
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if BERT_AVAILABLE else None
        
        if BERT_AVAILABLE:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                self.model.to(self.device)
                self.model.eval()
                print(f"BERT模型加载成功: {model_name}")
            except Exception as e:
                print(f"BERT模型加载失败: {e}")
    
    def get_embeddings(self, text: str, max_length: int = 512) -> Optional[np.ndarray]:
        """
        获取文本的BERT嵌入向量
        
        Args:
            text: 输入文本
            max_length: 最大序列长度
            
        Returns:
            文本嵌入向量
        """
        if not BERT_AVAILABLE or self.model is None:
            return None
        
        try:
            # 编码文本
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                max_length=max_length,
                truncation=True,
                padding=True
            )
            
            # 移动到设备
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 获取模型输出
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # 使用[CLS]标记的输出作为句子表示
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            
            return embeddings[0]
        
        except Exception as e:
            print(f"获取嵌入向量失败: {e}")
            return None
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的语义相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            余弦相似度 (0-1)
        """
        emb1 = self.get_embeddings(text1)
        emb2 = self.get_embeddings(text2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        # 计算余弦相似度
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        # 归一化到0-1
        return float((similarity + 1) / 2)
    
    def extract_semantic_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        基于语义重要性提取关键词
        
        Args:
            text: 输入文本
            top_k: 返回的关键词数量
            
        Returns:
            关键词及其重要性得分
        """
        if not BERT_AVAILABLE or self.model is None:
            return []
        
        try:
            # 分词
            tokens = self.tokenizer.tokenize(text)
            
            # 限制长度
            if len(tokens) > 510:
                tokens = tokens[:510]
            
            # 获取每个token的嵌入
            token_embeddings = []
            for i in range(0, len(tokens), 510):
                batch_tokens = tokens[i:i+510]
                token_ids = self.tokenizer.convert_tokens_to_ids(batch_tokens)
                inputs = torch.tensor([token_ids]).to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(inputs)
                
                token_embeddings.extend(outputs.last_hidden_state[0].cpu().numpy())
            
            # 计算每个token的重要性（与平均嵌入的相似度）
            avg_embedding = np.mean(token_embeddings, axis=0)
            
            importance_scores = []
            for i, token in enumerate(tokens):
                if token.startswith("##"):  # 跳过子词
                    continue
                similarity = np.dot(token_embeddings[i], avg_embedding) / (
                    np.linalg.norm(token_embeddings[i]) * np.linalg.norm(avg_embedding)
                )
                importance_scores.append((token, float(similarity)))
            
            # 按重要性排序
            importance_scores.sort(key=lambda x: x[1], reverse=True)
            
            return importance_scores[:top_k]
        
        except Exception as e:
            print(f"提取语义关键词失败: {e}")
            return []


class SemanticResumeMatcher:
    """基于语义的简历匹配器"""
    
    def __init__(self, use_bert: bool = True):
        """
        初始化匹配器
        
        Args:
            use_bert: 是否使用BERT模型
        """
        self.use_bert = use_bert and BERT_AVAILABLE
        self.bert_analyzer = BERTSemanticAnalyzer() if self.use_bert else None
    
    def calculate_semantic_match(self, resume: str, job_description: str) -> Dict:
        """
        计算简历与职位的语义匹配度
        
        Args:
            resume: 简历文本
            job_description: 职位描述
            
        Returns:
            匹配结果字典
        """
        result = {
            "semantic_similarity": 0.0,
            "keyword_overlap": 0.0,
            "skill_match": 0.0,
            "overall_score": 0.0,
            "use_bert": self.use_bert
        }
        
        if self.use_bert and self.bert_analyzer:
            # 计算语义相似度
            result["semantic_similarity"] = self.bert_analyzer.calculate_semantic_similarity(
                resume, job_description
            )
            
            # 提取语义关键词
            resume_keywords = self.bert_analyzer.extract_semantic_keywords(resume)
            job_keywords = self.bert_analyzer.extract_semantic_keywords(job_description)
            
            # 计算关键词重叠
            resume_kw_set = set([kw[0] for kw in resume_keywords])
            job_kw_set = set([kw[0] for kw in job_keywords])
            
            if job_kw_set:
                overlap = len(resume_kw_set & job_kw_set)
                result["keyword_overlap"] = overlap / len(job_kw_set)
            
            # 综合评分
            result["overall_score"] = (
                result["semantic_similarity"] * 0.6 +
                result["keyword_overlap"] * 0.4
            )
        
        return result


def test_bert_analyzer():
    """测试BERT分析器"""
    analyzer = BERTSemanticAnalyzer()
    
    text1 = "我有3年Python开发经验，熟悉Django框架"
    text2 = "需要Python开发工程师，要求熟悉Django"
    
    similarity = analyzer.calculate_semantic_similarity(text1, text2)
    print(f"语义相似度: {similarity:.4f}")
    
    keywords = analyzer.extract_semantic_keywords(text1, top_k=5)
    print(f"关键词: {keywords}")


if __name__ == "__main__":
    test_bert_analyzer()