import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

def generate_tech_stack(user_input):
    try:
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": f"Given the following project idea, suggest the best frontend, backend, database, deployment platform, and supporting tools:\n\n{user_input}\n\nFormat the response clearly with bullet points."
                }
            ],
            "max_tokens": 400,
            "temperature": 0.6
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
