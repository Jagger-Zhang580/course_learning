#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能权重配置模块
支持自定义技能权重和评分规则
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SkillLevel(Enum):
    """技能熟练度等级"""
    BEGINNER = 1      # 初级
    INTERMEDIATE = 2  # 中级
    ADVANCED = 3      # 高级
    EXPERT = 4        # 专家


@dataclass
class SkillRequirement:
    """技能要求"""
    name: str                    # 技能名称
    weight: float                # 权重 (0-1)
    required_level: SkillLevel   # 要求的熟练度
    is_mandatory: bool = False   # 是否必须
    synonyms: List[str] = None   # 同义词/别名
    
    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []


@dataclass
class SkillConfig:
    """技能配置"""
    job_title: str
    skills: List[SkillRequirement]
    min_experience_years: int = 0
    education_weight: float = 0.1
    experience_weight: float = 0.2
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "job_title": self.job_title,
            "skills": [
                {
                    "name": s.name,
                    "weight": s.weight,
                    "required_level": s.required_level.value,
                    "is_mandatory": s.is_mandatory,
                    "synonyms": s.synonyms
                }
                for s in self.skills
            ],
            "min_experience_years": self.min_experience_years,
            "education_weight": self.education_weight,
            "experience_weight": self.experience_weight
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SkillConfig':
        """从字典创建"""
        skills = [
            SkillRequirement(
                name=s["name"],
                weight=s["weight"],
                required_level=SkillLevel(s["required_level"]),
                is_mandatory=s.get("is_mandatory", False),
                synonyms=s.get("synonyms", [])
            )
            for s in data["skills"]
        ]
        return cls(
            job_title=data["job_title"],
            skills=skills,
            min_experience_years=data.get("min_experience_years", 0),
            education_weight=data.get("education_weight", 0.1),
            experience_weight=data.get("experience_weight", 0.2)
        )
    
    def save(self, filepath: str):
        """保存配置到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'SkillConfig':
        """从文件加载配置"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


class SkillWeightManager:
    """技能权重管理器"""
    
    # 预定义的技能配置模板
    TEMPLATES = {
        "python_developer": SkillConfig(
            job_title="Python开发工程师",
            skills=[
                SkillRequirement("Python", 0.25, SkillLevel.ADVANCED, True, ["python3", "py"]),
                SkillRequirement("Django", 0.15, SkillLevel.INTERMEDIATE, False, ["django framework"]),
                SkillRequirement("Flask", 0.10, SkillLevel.INTERMEDIATE, False, ["flask framework"]),
                SkillRequirement("MySQL", 0.12, SkillLevel.INTERMEDIATE, False, ["mysql", "sql"]),
                SkillRequirement("Redis", 0.08, SkillLevel.BEGINNER, False, ["redis cache"]),
                SkillRequirement("Git", 0.05, SkillLevel.INTERMEDIATE, False, ["git", "github", "gitlab"]),
                SkillRequirement("Docker", 0.08, SkillLevel.BEGINNER, False, ["docker", "container"]),
                SkillRequirement("Linux", 0.07, SkillLevel.INTERMEDIATE, False, ["linux", "ubuntu", "centos"]),
                SkillRequirement("RESTful API", 0.10, SkillLevel.INTERMEDIATE, False, ["rest", "api", "restful"]),
            ],
            min_experience_years=2,
            education_weight=0.15,
            experience_weight=0.25
        ),
        
        "java_developer": SkillConfig(
            job_title="Java开发工程师",
            skills=[
                SkillRequirement("Java", 0.25, SkillLevel.ADVANCED, True, ["java", "jdk"]),
                SkillRequirement("Spring", 0.20, SkillLevel.ADVANCED, True, ["spring boot", "spring framework", "springcloud"]),
                SkillRequirement("MySQL", 0.12, SkillLevel.INTERMEDIATE, False, ["mysql", "sql"]),
                SkillRequirement("Redis", 0.08, SkillLevel.INTERMEDIATE, False, ["redis"]),
                SkillRequirement("Maven", 0.05, SkillLevel.INTERMEDIATE, False, ["maven", "gradle"]),
                SkillRequirement("Git", 0.05, SkillLevel.INTERMEDIATE, False, ["git"]),
                SkillRequirement("Docker", 0.08, SkillLevel.BEGINNER, False, ["docker"]),
                SkillRequirement("微服务", 0.10, SkillLevel.INTERMEDIATE, False, ["microservice", "微服务"]),
                SkillRequirement("JVM", 0.07, SkillLevel.INTERMEDIATE, False, ["jvm", "java虚拟机"]),
            ],
            min_experience_years=3,
            education_weight=0.15,
            experience_weight=0.25
        ),
        
        "frontend_developer": SkillConfig(
            job_title="前端开发工程师",
            skills=[
                SkillRequirement("JavaScript", 0.20, SkillLevel.ADVANCED, True, ["js", "javascript", "es6"]),
                SkillRequirement("TypeScript", 0.15, SkillLevel.INTERMEDIATE, False, ["ts", "typescript"]),
                SkillRequirement("Vue", 0.15, SkillLevel.INTERMEDIATE, False, ["vue", "vuejs", "vue.js"]),
                SkillRequirement("React", 0.15, SkillLevel.INTERMEDIATE, False, ["react", "reactjs", "react.js"]),
                SkillRequirement("HTML", 0.08, SkillLevel.INTERMEDIATE, True, ["html", "html5"]),
                SkillRequirement("CSS", 0.08, SkillLevel.INTERMEDIATE, True, ["css", "css3", "scss", "sass"]),
                SkillRequirement("Webpack", 0.05, SkillLevel.BEGINNER, False, ["webpack", "vite", "打包工具"]),
                SkillRequirement("Git", 0.04, SkillLevel.INTERMEDIATE, False, ["git"]),
                SkillRequirement("Node.js", 0.10, SkillLevel.INTERMEDIATE, False, ["node", "nodejs", "node.js"]),
            ],
            min_experience_years=2,
            education_weight=0.10,
            experience_weight=0.20
        ),
        
        "data_scientist": SkillConfig(
            job_title="数据科学家",
            skills=[
                SkillRequirement("Python", 0.20, SkillLevel.ADVANCED, True, ["python", "python3"]),
                SkillRequirement("机器学习", 0.20, SkillLevel.ADVANCED, True, ["ml", "machine learning", "机器学习"]),
                SkillRequirement("深度学习", 0.15, SkillLevel.INTERMEDIATE, False, ["dl", "deep learning", "深度学习", "神经网络"]),
                SkillRequirement("TensorFlow", 0.10, SkillLevel.INTERMEDIATE, False, ["tensorflow", "tf"]),
                SkillRequirement("PyTorch", 0.10, SkillLevel.INTERMEDIATE, False, ["pytorch"]),
                SkillRequirement("Pandas", 0.08, SkillLevel.ADVANCED, False, ["pandas"]),
                SkillRequirement("SQL", 0.07, SkillLevel.INTERMEDIATE, False, ["sql", "mysql", "数据库"]),
                SkillRequirement("统计学", 0.05, SkillLevel.INTERMEDIATE, False, ["统计", "statistics"]),
                SkillRequirement("数据可视化", 0.05, SkillLevel.INTERMEDIATE, False, ["matplotlib", "seaborn", "可视化"]),
            ],
            min_experience_years=2,
            education_weight=0.20,
            experience_weight=0.20
        ),
    }
    
    def __init__(self):
        self.configs: Dict[str, SkillConfig] = {}
        self._load_templates()
    
    def _load_templates(self):
        """加载预定义模板"""
        self.configs.update(self.TEMPLATES)
    
    def add_config(self, name: str, config: SkillConfig):
        """添加配置"""
        self.configs[name] = config
    
    def get_config(self, name: str) -> Optional[SkillConfig]:
        """获取配置"""
        return self.configs.get(name)
    
    def list_configs(self) -> List[str]:
        """列出所有配置"""
        return list(self.configs.keys())
    
    def calculate_skill_score(
        self,
        resume_text: str,
        config: SkillConfig
    ) -> Dict:
        """
        根据技能配置计算简历得分
        
        Args:
            resume_text: 简历文本
            config: 技能配置
            
        Returns:
            评分结果
        """
        resume_lower = resume_text.lower()
        
        skill_scores = {}
        total_weight = 0
        weighted_score = 0
        mandatory_missing = []
        
        for skill in config.skills:
            # 检查技能名称和同义词
            found = False
            skill_text = skill.name.lower()
            
            if skill_text in resume_lower:
                found = True
            else:
                for synonym in skill.synonyms:
                    if synonym.lower() in resume_lower:
                        found = True
                        break
            
            # 计算该技能得分
            if found:
                # 简单的熟练度评估（基于关键词密度）
                level_score = self._estimate_skill_level(resume_text, skill)
                skill_scores[skill.name] = {
                    "found": True,
                    "level": level_score,
                    "weight": skill.weight,
                    "weighted_score": level_score * skill.weight
                }
                weighted_score += level_score * skill.weight
            else:
                skill_scores[skill.name] = {
                    "found": False,
                    "level": 0,
                    "weight": skill.weight,
                    "weighted_score": 0
                }
                if skill.is_mandatory:
                    mandatory_missing.append(skill.name)
            
            total_weight += skill.weight
        
        # 归一化得分
        normalized_score = weighted_score / total_weight if total_weight > 0 else 0
        
        # 检查必须技能
        mandatory_penalty = 0
        if mandatory_missing:
            mandatory_penalty = 0.3 * len(mandatory_missing)
        
        # 最终得分
        final_score = max(0, normalized_score - mandatory_penalty)
        
        return {
            "skill_scores": skill_scores,
            "raw_score": normalized_score,
            "final_score": final_score,
            "mandatory_missing": mandatory_missing,
            "matched_skills": [s for s, v in skill_scores.items() if v["found"]],
            "total_skills": len(config.skills)
        }
    
    def _estimate_skill_level(self, text: str, skill: SkillRequirement) -> float:
        """
        估计技能熟练度
        
        基于关键词出现频率和上下文
        """
        text_lower = text.lower()
        skill_lower = skill.name.lower()
        
        # 计算出现次数
        count = text_lower.count(skill_lower)
        for synonym in skill.synonyms:
            count += text_lower.count(synonym.lower())
        
        # 根据出现次数估计熟练度
        if count >= 5:
            return 1.0  # 专家级
        elif count >= 3:
            return 0.75  # 高级
        elif count >= 2:
            return 0.5  # 中级
        elif count >= 1:
            return 0.25  # 初级
        else:
            return 0.0


def create_custom_config(
    job_title: str,
    skills: List[Tuple[str, float, bool]],
    min_experience: int = 0
) -> SkillConfig:
    """
    创建自定义技能配置
    
    Args:
        job_title: 职位名称
        skills: 技能列表 [(名称, 权重, 是否必须), ...]
        min_experience: 最低经验年限
        
    Returns:
        技能配置
    """
    skill_requirements = [
        SkillRequirement(
            name=name,
            weight=weight,
            required_level=SkillLevel.INTERMEDIATE,
            is_mandatory=is_mandatory
        )
        for name, weight, is_mandatory in skills
    ]
    
    return SkillConfig(
        job_title=job_title,
        skills=skill_requirements,
        min_experience_years=min_experience
    )


# 示例用法
if __name__ == "__main__":
    manager = SkillWeightManager()
    
    print("可用的技能配置模板:")
    for name in manager.list_configs():
        config = manager.get_config(name)
        print(f"  - {name}: {config.job_title}")
    
    # 使用Python开发者模板
    config = manager.get_config("python_developer")
    
    # 测试简历
    resume = """
    张三，3年Python开发经验
    技能：
    - 熟练掌握Python编程
    - 熟悉Django和Flask框架
    - 了解MySQL数据库
    - 使用Git进行版本控制
    - 有Docker容器化经验
    """
    
    result = manager.calculate_skill_score(resume, config)
    
    print(f"\n简历评分结果:")
    print(f"最终得分: {result['final_score']:.2%}")
    print(f"匹配技能: {result['matched_skills']}")
    print(f"缺失必须技能: {result['mandatory_missing']}")