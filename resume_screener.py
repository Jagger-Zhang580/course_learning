#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI简历筛选工具
使用TF-IDF和余弦相似度进行简历与职位描述的匹配度计算
"""

import re
import math
from collections import Counter, defaultdict
import jieba
import jieba.analyse


class ResumeScreener:
    def __init__(self):
        # 停用词表（可根据需要扩展）
        self.stopwords = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
        
    def preprocess_text(self, text):
        """文本预处理：分词、去停用词"""
        # 使用jieba进行中文分词
        words = jieba.cut(text)
        # 过滤停用词和单个字符
        filtered_words = [word.strip() for word in words if len(word.strip()) > 1 and word.strip() not in self.stopwords]
        return filtered_words
    
    def extract_keywords(self, text, topK=10):
        """使用TF-IDF提取关键词"""
        keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
        return keywords
    
    def calculate_tfidf(self, documents):
        """计算TF-IDF值"""
        # 计算词频(TF)
        tf_list = []
        for doc in documents:
            word_count = Counter(doc)
            total_words = len(doc)
            tf = {word: count/total_words for word, count in word_count.items()}
            tf_list.append(tf)
        
        # 计算文档频率(DF)
        df = defaultdict(int)
        for tf in tf_list:
            for word in tf.keys():
                df[word] += 1
        
        # 计算逆文档频率(IDF)
        num_docs = len(documents)
        idf = {word: math.log(num_docs/(freq + 1)) + 1 for word, freq in df.items()}
        
        # 计算TF-IDF
        tfidf_list = []
        for tf in tf_list:
            tfidf = {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}
            tfidf_list.append(tfidf)
        
        return tfidf_list
    
    def cosine_similarity(self, vec1, vec2):
        """计算两个向量的余弦相似度"""
        # 找到共同的词
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        if not common_words:
            return 0.0
        
        # 计算点积
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        
        # 计算向量模长
        norm1 = math.sqrt(sum(val**2 for val in vec1.values()))
        norm2 = math.sqrt(sum(val**2 for val in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def match_resume_to_job(self, resume_text, job_description):
        """计算简历与职位描述的匹配度"""
        # 预处理文本
        resume_words = self.preprocess_text(resume_text)
        job_words = self.preprocess_text(job_description)
        
        # 计算TF-IDF
        tfidf_list = self.calculate_tfidf([resume_words, job_words])
        
        # 计算余弦相似度
        similarity = self.cosine_similarity(tfidf_list[0], tfidf_list[1])
        
        # 提取关键词
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_description)
        
        # 计算关键词匹配度
        resume_keyword_set = set([kw[0] for kw in resume_keywords])
        job_keyword_set = set([kw[0] for kw in job_keywords])
        keyword_overlap = len(resume_keyword_set & job_keyword_set)
        keyword_match_score = keyword_overlap / len(job_keyword_set) if job_keyword_set else 0
        
        # 综合评分（TF-IDF相似度占70%，关键词匹配占30%）
        final_score = similarity * 0.7 + keyword_match_score * 0.3
        
        return {
            'similarity_score': round(similarity, 4),
            'keyword_match_score': round(keyword_match_score, 4),
            'final_score': round(final_score, 4),
            'resume_keywords': resume_keywords,
            'job_keywords': job_keywords
        }
    
    def screen_multiple_resumes(self, resumes, job_description):
        """筛选多个简历"""
        results = []
        for i, resume in enumerate(resumes):
            result = self.match_resume_to_job(resume, job_description)
            result['resume_id'] = i + 1
            results.append(result)
        
        # 按最终得分排序
        results.sort(key=lambda x: x['final_score'], reverse=True)
        return results


def main():
    """示例使用"""
    screener = ResumeScreener()
    
    # 示例职位描述
    job_desc = """
    职位：Python开发工程师
    要求：
    1. 熟练掌握Python编程语言
    2. 熟悉Django或Flask框架
    3. 了解MySQL、Redis等数据库
    4. 有良好的代码习惯和文档编写能力
    5. 具备团队协作精神
    """
    
    # 示例简历
    resume1 = """
    个人简历
    姓名：张三
    教育背景：本科，计算机科学与技术专业
    工作经验：
    1. 3年Python开发经验
    2. 熟练使用Django框架开发Web应用
    3. 熟悉MySQL数据库设计和优化
    4. 了解Redis缓存技术
    5. 有良好的编码习惯，注重代码质量
    """
    
    resume2 = """
    个人简历
    姓名：李四
    教育背景：硕士，软件工程专业
    工作经验：
    1. 2年Java开发经验
    2. 熟悉Spring Boot框架
    3. 了解PostgreSQL数据库
    4. 有前端开发经验，熟悉Vue.js
    5. 参与过多个大型项目开发
    """
    
    resume3 = """
    个人简历
    姓名：王五
    教育背景：本科，信息技术专业
    工作经验：
    1. 4年Python开发经验
    2. 精通Django和Flask框架
    3. 熟悉MySQL、MongoDB、Redis
    4. 有Docker和Kubernetes部署经验
    5. 良好的团队协作和沟通能力
    """
    
    # 单个简历匹配
    print("=== 单个简历匹配结果 ===")
    result = screener.match_resume_to_job(resume1, job_desc)
    print(f"简历1匹配度: {result['final_score']:.2%}")
    print(f"TF-IDF相似度: {result['similarity_score']:.4f}")
    print(f"关键词匹配度: {result['keyword_match_score']:.4f}")
    print(f"简历关键词: {[kw[0] for kw in result['resume_keywords']]}")
    print(f"职位关键词: {[kw[0] for kw in result['job_keywords']]}")
    print()
    
    # 多个简历筛选
    print("=== 多简历筛选排名 ===")
    resumes = [resume1, resume2, resume3]
    results = screener.screen_multiple_resumes(resumes, job_desc)
    
    for result in results:
        print(f"简历{result['resume_id']}: 最终得分 {result['final_score']:.2%} "
              f"(相似度: {result['similarity_score']:.4f}, "
              f"关键词匹配: {result['keyword_match_score']:.4f})")


if __name__ == "__main__":
    main()