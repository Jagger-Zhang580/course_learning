# AI简历筛选工具 - 增强版

## 功能特性

### 核心功能
1. **BERT语义理解** - 使用预训练BERT模型进行深度语义分析
2. **技能权重配置** - 自定义技能权重和评分规则
3. **多格式支持** - 支持PDF、Word、TXT文件解析
4. **机器学习分类** - 智能职位分类和简历质量评估

### 评分维度
- **TF-IDF相似度** (20%) - 基于词频-逆文档频率的传统匹配
- **语义相似度** (30%) - BERT语义理解（可选）
- **技能匹配度** (35%) - 基于权重的技能匹配
- **简历质量** (15%) - 格式、结构、完整性评估

## 安装

### 基础安装
```bash
pip install jieba flask
```

### 完整安装（包含所有功能）
```bash
pip install -r requirements.txt
```

### BERT功能（可选，需要GPU）
```bash
pip install transformers torch
```

## 使用方法

### 方法1：增强版Web界面（推荐）
```bash
python enhanced_app.py
```
访问 http://localhost:5001

### 方法2：基础版Web界面
```bash
python app.py
```
访问 http://localhost:5000

### 方法3：命令行
```bash
python enhanced_screener.py
```

## 文件结构

```
├── resume_screener.py    # 基础TF-IDF筛选
├── bert_analyzer.py      # BERT语义分析
├── skill_weight.py       # 技能权重配置
├── file_parser.py        # 文件解析（PDF/Word）
├── ml_classifier.py      # 机器学习分类
├── enhanced_screener.py  # 增强版整合模块
├── enhanced_app.py       # 增强版Web应用
├── app.py               # 基础版Web应用
├── templates/
│   ├── index.html        # 基础版界面
│   └── enhanced_index.html # 增强版界面
├── requirements.txt      # 依赖列表
└── README.md            # 说明文档
```

## API接口

### 分析单个简历
```
POST /api/analyze
{
    "job_description": "职位描述",
    "resume": "简历内容",
    "skill_template": "python_developer"
}
```

### 批量筛选
```
POST /api/screen
{
    "job_description": "职位描述",
    "resumes": ["简历1", "简历2"],
    "skill_template": "python_developer"
}
```

### 文件上传
```
POST /api/upload
FormData: files[], job_description, skill_template
```

### 获取模板
```
GET /api/templates
```

## 预定义技能模板

- `python_developer` - Python开发工程师
- `java_developer` - Java开发工程师
- `frontend_developer` - 前端开发工程师
- `data_scientist` - 数据科学家

## 算法说明

### 1. TF-IDF + 余弦相似度
计算简历与职位描述的文本相似度

### 2. BERT语义分析
使用预训练BERT模型理解文本语义，捕捉同义词和上下文关系

### 3. 技能权重匹配
根据职位要求的技能权重计算匹配分数

### 4. 简历质量评估
评估简历的完整性、结构、格式等质量指标

### 5. 机器学习分类
自动识别职位类别，提供针对性匹配建议