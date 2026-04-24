# N8N 8-Week Learning Plan

## Overview
An 8‑week curriculum to go from zero to production‑ready N8N automation engineer, with weekly hands‑on demos that you can run immediately.

---

## Week‑by‑Week Schedule

| Week | Topic & Goals | Hands‑On Demo |
|------|---------------|---------------|
| **1** | **Intro & Setup** – install N8N (Docker/npm), UI overview, basic concepts (nodes, workflows, executions). | **Hello World**: HTTP Request → Set → Reply (returns static JSON). |
| **2** | **Core Nodes & Data Flow** – Set, Function, If, Merge, Switch; handling JSON, expressions (`$json`, `$node`). | **Contact‑form Processor**: Webhook → Function (validate) → If (valid/invalid) → Email / Slack notifications. |
| **3** | **API Integrations** – HTTP Request node, OAuth2 credentials, pagination, error handling. | **Daily Weather Alert**: Schedule Trigger → HTTP Request (OpenWeather) → Function (extract temp) → Send Telegram message. |
| **4** | **Built‑in Apps & Triggers** – Google Sheets, Discord, Slack, Twilio, Cron, Webhook. | **Daily Report**: Cron (08:00) → Google Sheets Read → Function (summarize) → Slack Post. |
| **5** | **Branching & Loops** – SplitInBatches, Execute Workflow, Do While, Wait, Merge (Append). | **CSV Enrichment Pipeline**: Read CSV → SplitInBatches → For each batch: HTTP Request (enrich) → Merge → Write back to Google Sheets. |
| **6** | **Custom Nodes & Credentials** – develop a simple community node (TypeScript) or use HTTP Request with custom headers; manage encrypted credentials. | **Slack Slash‑Command Joke Bot**: Custom node that calls a mock “Joke API” → formatted message → reply in Slack. |
| **7** | **Advanced Logic & AI** – Function node with AI (OpenAI/HuggingFace), AI Agent node, conditional AI prompts, handling rate limits. | **AI‑Powered Ticket Triage**: Webhook (support ticket) → Function (call OpenAI to classify) → Switch (priority) → Assign to different Teams/Email queues. |
| **8** | **Production & Scaling** – workflow execution modes (main/ worker), scaling with queues, monitoring (execution logs, webhooks), backups, version control (git export/import), deploying to Kubernetes or Cloud. | **Multi‑Env Workflow with Monitoring**: dev → test → prod using environment variables; monitoring webhook posts execution failures to Discord; export/import workflow via CLI. |

---

## How to Use This Plan
1. **Set up N8N** (Docker is fastest):
   ```bash
   docker run -it --rm \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     n8nio/n8n
   ```
2. Follow the weekly topics, building the demo workflow step‑by‑step.
3. After each demo, try the **extension ideas** listed in the “Resources” column (e.g., add error handling, swap APIs, schedule different triggers).
4. At the end of week 8, you will have a portfolio of reusable workflows and the knowledge to production‑scale them.

---

## Suggested Resources
- Official N8N Documentation: https://docs.n8n.io/
- N8N Community Nodes: https://github.com/n8n-io/community-nodes
- N8N Academy (free video lessons): https://academy.n8n.io/
- YouTube: “n8n tutorial” playlists (e.g., by Walter Guevara, TechWorld with Nana)
- API‑specific docs (OpenWeather, Telegram, Slack, Google Sheets, etc.)

---

*Happy automating!*