import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

def developer_agent_suggestion(user_input):
    try:
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        prompt = f"""
You are a highly experienced software developer in a multi-agent AI system.

Your job is to receive a project idea and return ONLY the following:
1. Recommended programming language & framework(s)
2. Suggested file/folder structure
3. Any key libraries/tools to include

Respond in clear bullet points and markdown formatting.

Project Idea:
{user_input}
"""

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.5
        }

        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]

    except Exception as e:
        return f"❌ Error: {str(e)}"
