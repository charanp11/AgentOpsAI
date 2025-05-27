# AgentOpsAI 🧠🚀  
**AI-powered Dev + Infra + QA generator from your idea or GitHub repo**

AgentOpsAI is a full-stack project planning assistant that transforms your project idea or GitHub repo into a complete development plan — with AI-generated summaries, dev suggestions, test strategies, infra scaffolding, and code boilerplates.

> 💬 Type your idea or repo → 💡 Get tech insights → 🛠 Download the project as a ZIP → ☁️ Deployed with Claude + S3 + CDK.

---

## 🔥 Features

- 📝 **AI Project Summary** – Powered by Claude 3 Haiku (via Amazon Bedrock)
- 💡 **Tech Stack Detector** – Auto-suggested tools for frontend, backend, DB, and cloud
- 🧑‍💻 **Dev Agent** – Folder structure, frameworks, programming languages
- 🧪 **QA Agent** – Test plans, edge cases, automation strategy
- ☁️ **Infra Agent** – AWS CDK infrastructure suggestions (based on use case)
- 🧱 **CDK Generator** – Dynamic `infra_stack.py` for common stacks (chatbot, pipelines)
- 💻 **Code Generator** – Boilerplate code for React, Flask, Express
- 📄 **PDF/TXT Download** – Export reports instantly
- 🔐 **ZIP Upload to S3** – Secure, pre-signed download links from AWS
- 🌐 **Deployed on Render** – Cloud-ready and production-polished

---

## 📦 Tech Stack

| Layer         | Tech Used |
|---------------|-----------|
| Backend       | Flask (Python) |
| LLM           | Claude 3 Haiku via Amazon Bedrock |
| Agents        | Custom Dev/QA/Infra Agents (LangChain-inspired) |
| Infra-as-Code | AWS CDK |
| Code Gen      | React, Flask, Express Templates |
| File Storage  | Amazon S3 + Pre-signed URLs |
| UI/UX         | Bootstrap + Dark Theme |
| Deployment    | Render (Free Tier) |
| CI/CD         | 🔁 Continuous Deployment via GitHub → Render |

---

## 🧪 How it works

1. **Enter a GitHub repo or project idea**
2. 🧠 AgentOps fetches the README or idea
3. 📊 Claude summarizes and suggests a stack
4. 🧑‍💻 Agents generate developer/QA/infra recommendations
5. 🧱 View generated code/CDK infra
6. 📦 Download a complete ZIP with:
    - `main.py` / `index.js`
    - `infra_stack.py`
    - `README.txt`

---

## 🌐 Live Demo

👉 [AgentOps 🤖](https://agentopsai.onrender.com)

---

<details>
<summary>📁 Click to view project structure</summary>

agentops/
├── app.py # Main Flask app
├── agents/ # Dev, QA, Infra agents
├── utils/ # Claude summarizer, tech stack & code generator, S3 uploader
├── cdk/infra_stack.py # Infra-as-Code generator
├── templates/ # HTML pages
├── static/ # Styles
├── requirements.txt
└── README.md

</details>

---

## 🚀 Setup

```bash
git clone https://github.com/charanp11/AgentOpsAI.git
cd AgentOpsAI
pip install -r requirements.txt
python app.py