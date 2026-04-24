## 2‑周 MLflow 入门与实战课程（Markdown 版）

### 课程目标
- 让学员快速掌握 MLflow 的核心概念（Tracking、Projects、Models、Registry）  
- 通过动手 Demo 实现端到端的机器学习工作流（训练 → 记录 → 打包 → 部署）  
- 了解最佳实践与常见坑，能够在真实项目中直接使用 MLflow  

---

## 第 1 周：概念与基础操作

| 天数 | 主题 | 内容要点 | 实作/练习 |
|------|------|----------|-----------|
| Day 1 | **课程导览 & 环境准备** | - 课程大纲 & 目标 <br>- 安装 Python、conda/virtualenv <br>- 安装 MLflow (`pip install mlflow`) <br>- 启动本地 UI (`mlflow ui`) | 验证 UI 可访问 (`http://127.0.0.1:5000`) |
| Day 2 | **MLflow Tracking 基础** | - 实验、Run、参数、指标、Artifact <br>- `mlflow.start_run()`、`log_param`、`log_metric`、`log_artifact` <br>- 本地文件系统 vs. 远程存储（文件、S3、Azure Blob） | 记录一次简单线性回归实验，查看 UI 中的 Run 对比 |
| Day 3 | **Track 多种模型与自定义 Artifact** | - 记录 Scikit‑learn、TensorFlow、PyTorch 模型 <br>- 使用 `mlflow.<flavor>.log_model` 与 `save_model` <br>- 自定义 Artifact（图片、JSON、模型解释文件） | 分别跑 sklearn 决策树、tf.keras 全连接网络，记录模型并可视化 |
| Day 4 | **Projects 基础：可重用的代码包装** | - 项目结构 (`conda.yaml`、`MLproject`、`entry points`) <br>- 参数化入口（`parameters`、`cmd`）<br>- 本地运行 (`mlflow run . -P alpha=0.5`) | 将前两天的训练脚本封装成 MLproject，尝试不同超参数跑跑看 |
| Day 5 | **Projects 高级：Git、Docker 与远程执行** | - 从 Git 仓库拉取项目运行 <br>- 使用 Docker 环境 (`docker_env:` in MLproject) <br>- 远程后端（例如：`mlflow run . --backend=azureml` 演示概念） | 从公开仓库（如 mlflow/examples）拉取一个示例项目并在本地 Docker 中跑通 |
| Day 6 | **Model 与 Registry 初识** | - 模型格式（`MLmodel`、`conda.yaml`、`model.pkl`）<br>- `mlflow.models.serve` 本地服务 <br>- Model Registry 的基本概念（阶段、版本、过渡） | 用 `mlflow models serve` 启动模型服务，用 `curl` 发送预测请求 |
| Day 7 | **巩固实验 & 小测验** | - 回顾 Tracking、Projects、Model 三大核心 <br>- 常见问题排错（路径、依赖、版本冲突）<br>- 小测验（选择题 + 简答） | 完成在线测验，讨论错题并给出改进方案 |

---

## 第 2 周：端到端 Demo 与进阶实践

| 天数 | 主题 | 内容要点 | 实作/练习 |
|------|------|----------|-----------|
| Day 8 | **端到端工作流概览** | - 从数据准备 → 特征工程 → 模型训练 → 记录 → 注册 → 部署 <br>- 每一步对应的 MLflow API <br>- 使用 `mlflow.tracking.MlflowClient` 进行程序化查询 | 画出流程图，标注对应的 MLflow 调用点 |
| Day 9 | **Demo 1：批处理训练 & 注册** | - 使用 sklearn 对经典数据集（如 Wine Quality）做回归 <br>- 记录参数、指标、模型 artifact <br>- 将模型注册到 Model Registry，设置为 `Staging` | 完成注册并检查版本号、阶段 |
| Day 10 | **Demo 2：模型服务化（本地 & 云）** | - 本地 `mlflow models serve` 测试 <br>- 导出为 Docker 镜像（`mlflow models build-docker`）<br>- 在本地 Docker 中运行并验证 REST 接口 <br>- （可选）将镜像推送至私有仓库，演示云端部署思路 | 编写简单的 Python 客户端，调用服务并返回预测 |
| Day 11 | **Demo 3：模型版本管理与灰度发布** | - 登记新版本模型（如调整超参数）<br>- 使用阶段过渡（`Staging` → `Production`、`Archive`）<br>- 演示 A/B 测试思路：两个版本并行服务，通过流量切换验证 | 在同一端口启动两个容器（不同版本），用脚本切换请求比较结果 |
| Day 12 | **进阶：超参数搜索与自动记录** | - 使用 `mlflow.tracking.fluent` 配合 Optuna、Hyperopt <br>- 自动记录每次 trial 的参数与指标 <br>- 在 UI 中使用过滤器、对比图表查看最佳运行 | 跑一个小规模的 Optuna 搜索（5‑10 次 trial），记录并挑选最佳模型 |
| Day 13 | **进阶：模型包装与自定义推理** | - 编写 `PythonModel` 自定义 `load_context`、`predict` <br>- 添加自定义依赖（如特殊的 preprocessing 库）<br>- 保存为通用模型 flavor，实现跨平台服务 | 实现一个带文本向量化的自定义模型，打包后在不同机器上 load & predict |
| Day 14 | **课程总结、最佳实践 & Q&A** | - MLflow 在团队协作中的角色 <br>- 常见坑：路径、版本锁定、Artifact 大小限制 <br>- 性能调优（并行 runs、云存储选择）<br>- 开放讨论：学员分享自己的使用场景 | 发放课程资料链接、推荐进一步阅读（官方文档、博客、案例）<br>完成课程反馈问卷 |

---

### 参考资源（可放在课程末尾）

- 官方文档： https://mlflow.org/docs/latest/index.html  
- 快速开始教程： https://mlflow.org/docs/latest/quickstart.html  
- 示例项目： https://github.com/mlflow/mlflow/tree/master/examples  
- 模型发布指南： https://mlflow.org/docs/latest/models.html#deploying-models  
- 常见问题 FAQ： https://mlflow.org/docs/latest/faq.html  

---

> **使用说明**：将以上内容保存为 `mlflow_2week_course.md`，直接在任意 Markdown 编辑器或仓库中查看。每天的“实作/练习”建议采用 Jupyter Notebook 或 .py 脚本完成，并在结束时提交到共享仓库（如 GitHub/GitLab）以便互评。祝学习愉快！