# 图书管理系统（Library Management System）8 周学习计划

**目标**：从零到能够独立设计、开发并部署一个功能完整的图书管理系统（含图书 catalog、借阅/归还、用户管理、搜索、报表等核心模块），并掌握后端 API、前端界面、数据库设计、测试与部署等全链路技能。

> 本计划采用 **全栈**（后端：Node.js/Express 或 Python/FastAPI + PostgreSQL/MySQL；前端：React/Vue 或简单的 HTML+Bootstrap）方案，每周产出可运行的 Demo，最终在第 8 周完成可部署的完整系统。

---

## 周次安排

| 周 | 主题 & 目标 | 实战 Demo |
|----|-------------|-----------|
| **1** | **需求分析 & 系统架构**<br> - 明确功能需求（图书 CRUD、用户登录、借阅流程、逾期提醒、统计报表）。<br> - 设计系统整体架构（前后端分离、RESTful API、数据库选型）。<br> - 学习常用图书管理系统的业务模型（书籍、作者、分类、借阅记录、用户角色）。 | **需求文档 & 原型图**：<br>使用 Markdown 或工具（如 draw.io、Figma）绘制用例图、活动图和粗略的页面 wireframe。<br>输出：`docs/requirements.md`、`docs/architecture.png`。 |
| **2** | **数据库设计与基础 CRUD**<br> - 学习关系型数据库设计（范式、ER 图、主外键、索引）。<br> - 实现图书、用户、借阅三张核心表的建表语句。<br> - 使用 SQL 或 ORM 完成基本的增删改查。 | **后端 API 基础**：<br>创建 Express（或 FastAPI）项目，实现 `/books`、`/users`、`/borrows` 的 GET/POST/PUT/DELETE 接口（不做鉴权）。<br>使用 PostgreSQL（Docker）进行持久化。<br>Demo：通过 Postman/curl 测试添加一本书并查询。 |
| **3** | **用户认证与授权**<br> - 学习 JWT、Session、OAuth2 基础概念。<br> - 实现用户注册、登录、密码加密（bcrypt）。<br> - 设计角色（管理员、普通用户）及权限中间件。 | **登录/注册流程**：<br>实现 `/auth/register`、`/auth/login` 接口，返回 JWT。<br>在前端（简单 HTML+Bootstrap）加入登录页，成功后把 Token 存入 localStorage 并调用受保护的图书列表接口。<br>Demo：注册一个用户，登录后查看自己的借阅记录。 |
| **4** | **借阅/归还业务流程**<br> - 设计借阅状态（已借出、已归还、逾期、续借）。<br> - 实现借书（生成借阅记录、减少库存）、还书（更新状态、增加库存）、续借、逾期罚款计算。<br> - 使用事务保证数据一致性。 | **借阅 API**：<br>POST `/borrows`（用户 ID + 书籍 ID）<br>POST `/borrows/{id}/return`（归还）<br>POST `/borrows/{id}/renew`（续借）<br>在前端添加 “借书” / “还书” 按钮，调用对应接口并实时更新库存显示。<br>Demo：用户 A 借阅《三体》，库存减 1；归还后库存恢复。 |
| **5** | **搜索与过滤功能**<br> - 学习全文搜索（PostgreSQL `tsvector` / `gin` 索引或 Elasticsearch 基础）。<br> - 实现按书名、作者、ISBN、分类的多字段搜索、分页、排序。<br> - 前端实现搜索框与结果列表的交互。 | **搜索 API**：<br>GET `/books?keyword=python&page=1&size=10`（后端使用 `ILIKE` 或全文索引）。<br>前端使用 React/Vue（或原生 JS + fetch）实现实时搜索（输入延迟 300ms 防抖）。<br>Demo：输入 “机器学习” 出现相关书籍列表，支持分页。 |
| **6** | **报表与统计**<br> - 学习聚合函数、分组统计、时间序列报表（如月度借阅量、热门图书、用户活跃度）。<br> - 使用 SQL 或聚合库生成报表数据。<br> - 前端用图表库（Chart.js / AntV / ECharts）展示。 | **报表 API**：<br>GET `/stats/monthly-borrows`（返回过去 12 个月每月借阅量）。<br>GET `/stats/top-books`（返回前 10 本最常被借的图书）。<br>前端页面展示折线图和柱状图。<br>Demo：管理员登录后查看 “本月借阅趋势” 图表。 |
| **7** | **单元测试、集成测试与 CI/CD 基础**<br> - 学习测试金字塔（单元、服务、端到端）。<br> - 使用 Jest（JS）/ PyTest（Python）编写 API 单元测试。<br> - 使用 Supertest（Node）/ TestClient（FastAPI）做接口测试。<br> - 初步了解 GitHub Actions 或 GitLab CI 自动跑测试。 | **测试套件**：<br>为图书 CRUD、用户登录、借阅流程编写完整的单元与集成测试（覆盖率 ≥ 80%）<br>在本地运行 `npm test` 或 `pytest` 并查看报告。<br>Demo：故意破坏借阅逻辑（如不减库存），测试失败后修复并再次通过。 |
| **8** | **部署、监控与扩展**<br> - 学习 Docker 镜像制作（后端 & 前端），docker‑compose 编排。<br> - 基础监控：日志（winston/pino 或 loguru）、错误追踪（Sentry 基础使用）。<br> - 性能优化：查询慢日志、索引建议、缓存（Redis）用于热点图书查询。<br> - 可选扩展：引入 Elasticsearch 实现高级全文搜索、使用 WebSocket 实现实时通知（如逾期提醒）。 | **完整系统部署**：<br>1. 编写 Dockerfile（后端） && Dockerfile（前端）<br>2. 编写 `docker-compose.yml` 包含：后端、前端、PostgreSQL、Redis（可选）、Nginx（反向代理）<br>3. 运行 `docker-compose up -d`，访问 `http://localhost` 查看完整系统。<br>4. 在后端加入简单的请求日志中间件；在前端加入错误捕获并上报到本地的 mock Sentry endpoint。<br>Demo：启动后，完成一整本书的查询→借阅→归还流程，查看控制台日志确认每一步被记录。 |

---

## 每周学习资源推荐

| 周 | 推荐阅读/视频/文档 |
|----|-------------------|
| 1 | 《软件需求与规格说明》 第 2 章；UML 基础教程（博客或哔哩哔哩视频） |
| 2 | PostgreSQL 官方文档（DDL、DML）；ORM 选型：Sequelize（Node）或 SQLAlchemy（Python） |
| 3 | JWT 官方指南；Passport.js（Node）或 FastAPI Users（Python）示例 |
| 4 | 事务隔离级别（READ COMMITTED、REPEATABLE READ）；PostgreSQL `SELECT ... FOR UPDATE` |
| 5 | PostgreSQL 全文搜索教程；Elasticsearch 官方入门（可选） |
| 6 | SQL 聚合函数手册；Chart.js 文档；Ant Design 图表组件 |
| 7 | Jest 官方文档；Supertest README；GitHub Actions CI 入门 |
| 8 | Docker 官方教程；docker‑compose 文档；日志框架 winston/pino ；Sentry Node SDK 快速开始 |

---

## 如何使用此计划

1. **准备环境**  
   - 安装 Docker、Docker‑Compose、Git、Node.js（≥18）或 Python（≥3.9）  
   - 克隆本仓库（或新建空文件夹）作为项目根目录  
   - 建议使用 VS Code + 对应语言插件（ESLint、Prettier、Python）

2. **按周迭代**  
   - 每周先阅读推荐资源，理解概念  
   - 按照 “实战 Demo” 步骤编写代码，提交到本地 Git 分支（如 `week1-base`、`week2-auth`）  
   - 周末进行自我检查：运行所有已有功能，确保没有回退

3. **扩展与挑战（可选）**  
   - 周 3：加入第三方登录（GitHub、Google）  
   - 周 5：切换到 Elasticsearch 实现实时高亮搜索  
   - 周 6：加入导出 CSV/PDF 报表功能  
   - 周 7：加入端到端 Cypress 测试模拟真实用户操作  
   - 周 8：使用 Kubernetes（Kind 或 Minikube）部署，配置 Horizontal Pod Autoscaler

4. **最终成果**  
   - 可在任何支持 Docker 的机器上一键启动的完整图书管理系统  
   - 包含完整的 API 文档（OpenAPI/Swagger）、用户手册和运维手册  
   - 代码仓库保持良好的分支历史，便于后续面试或项目展示  

祝学习顺利，期待你完成自己的图书管理系统！如果在任意周遇到卡点，随时告诉我，我可以提供具体代码片段或调试思路。祝编码愉快！