from flask import Flask, render_template, request, send_file
from utils.summarizer import summarize_with_claude
from utils.tech_stack_gen import generate_tech_stack
from agents.dev_agent import developer_agent_suggestion
from agents.qa_agent import qa_agent_suggestion
from agents.infra_agent import infra_agent_suggestion
from io import BytesIO
from xhtml2pdf import pisa
import os


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    tech_stack = ""
    dev_output = ""
    qa_output = ""
    infra_output = ""

    if request.method == "POST":
        idea = request.form.get("idea")
        summary = summarize_with_claude(idea)
        tech_stack = generate_tech_stack(idea)
        dev_output = developer_agent_suggestion(idea)
        qa_output = qa_agent_suggestion(idea)
        infra_output = infra_agent_suggestion(idea)

    return render_template("index.html", summary=summary, tech_stack=tech_stack,
                           dev_output=dev_output, qa_output=qa_output, infra_output=infra_output)
    
@app.route("/download/<filetype>", methods=["POST"])
def download(filetype):
    idea = request.form.get("idea")
    summary = summarize_with_claude(idea)
    tech_stack = generate_tech_stack(idea)
    dev = developer_agent_suggestion(idea)
    qa = qa_agent_suggestion(idea)
    infra = infra_agent_suggestion(idea)

    full_output = f"""
AgentOps AI Report 📋

📝 Summary:
{summary}

🧰 Tech Stack:
{tech_stack}

🧑‍💻 Dev Agent:
{dev}

🧪 QA Agent:
{qa}

☁️ Infra Agent:
{infra}
"""

    if filetype == "txt":
        return send_file(BytesIO(full_output.encode("utf-8")),
                         download_name="agentops_summary.txt",
                         as_attachment=True)

    if filetype == "pdf":
        result = BytesIO()
        html = f"<pre>{full_output}</pre>"
        pisa.CreatePDF(html, dest=result)
        result.seek(0)
        return send_file(result, download_name="agentops_summary.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

