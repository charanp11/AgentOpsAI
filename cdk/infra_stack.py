def generate_infra_stack_code(project_description):
    project_description = project_description.lower()

    if "chatbot" in project_description:
        return """from aws_cdk import core, aws_lambda as _lambda

class ChatbotInfraStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        _lambda.Function(self, "ChatbotHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda")
        )
"""
    elif "data pipeline" in project_description:
        return """from aws_cdk import core, aws_s3 as s3, aws_glue as glue

class DataPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, "DataBucket")
        # Glue job configuration goes here
"""
    else:
        return "# No matching infrastructure template found for this description."
