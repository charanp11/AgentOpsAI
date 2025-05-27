from flask import Flask, render_template, request, send_file
from utils.summarizer import summarize_with_claude
from utils.tech_stack_gen import generate_tech_stack
from utils.code_gen import generate_code_boilerplate
from cdk.infra_stack import generate_infra_stack_code
from utils.github_analyzer import is_github_url, get_repo_info
from utils.s3_uploader import upload_zip_to_s3
from agents.dev_agent import developer_agent_suggestion
from agents.qa_agent import qa_agent_suggestion
from agents.infra_agent import infra_agent_suggestion
from io import BytesIO
from zipfile import ZipFile
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

        if is_github_url(idea):
            repo_info = get_repo_info(idea)
            if "error" in repo_info:
                summary = "⚠️ GitHub repo fetch failed. Please try again."
                tech_stack = ""
                agent_input = idea
            else:
                readme = repo_info.get("readme", "")
                summary = summarize_with_claude(readme)
                tech_stack = generate_tech_stack(readme)
                agent_input = readme
        else:
            summary = summarize_with_claude(idea)
            tech_stack = generate_tech_stack(idea)
            agent_input = idea

        dev_output = developer_agent_suggestion(agent_input)
        qa_output = qa_agent_suggestion(agent_input)
        infra_output = infra_agent_suggestion(agent_input)

    return render_template("index.html", summary=summary, tech_stack=tech_stack,
                           dev_output=dev_output, qa_output=qa_output, infra_output=infra_output)

@app.route("/generate_code", methods=["POST"])
def generate_code():
    idea = request.form.get("idea", "")
    tech_stack = request.form.get("tech_stack", "")
    code = generate_code_boilerplate(tech_stack)
    return render_template("results.html", code=code, idea=idea, tech_stack=tech_stack)

@app.route("/generate_infra", methods=["POST"])
def generate_infra():
    idea = request.form.get("idea", "")
    infra_code = generate_infra_stack_code(idea)
    return render_template("results.html", infra_code=infra_code, idea=idea)

@app.route("/download/<filetype>", methods=["POST"])
def download(filetype):
    idea = request.form.get("idea")

    if is_github_url(idea):
        repo_info = get_repo_info(idea)
        if "error" in repo_info:
            summary = "GitHub repo fetch failed."
            tech_stack = ""
            agent_input = idea
        else:
            readme = repo_info.get("readme", "")
            summary = summarize_with_claude(readme)
            tech_stack = generate_tech_stack(readme)
            agent_input = readme
    else:
        summary = summarize_with_claude(idea)
        tech_stack = generate_tech_stack(idea)
        agent_input = idea

    dev = developer_agent_suggestion(agent_input)
    qa = qa_agent_suggestion(agent_input)
    infra = infra_agent_suggestion(agent_input)

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

@app.route("/download_zip", methods=["POST"])
def download_zip():
    idea = request.form.get("idea", "")
    tech_stack = request.form.get("tech_stack", "")

    summary = summarize_with_claude(idea)
    code = generate_code_boilerplate(tech_stack)
    infra = generate_infra_stack_code(idea)

    temp_zip = BytesIO()
    with ZipFile(temp_zip, 'w') as z:
        z.writestr("README.txt", summary)
        z.writestr("main.py", code)
        z.writestr("infra_stack.py", infra)

    temp_zip.seek(0)

    url = upload_zip_to_s3(temp_zip)

    if url:
        return f'<p>Your ZIP is ready: <a href="{url}" target="_blank">Download ZIP from S3</a></p>'
    else:
        return "❌ Failed to upload or generate secure link. Check AWS credentials or bucket."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
