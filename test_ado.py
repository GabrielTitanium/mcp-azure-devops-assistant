from azure_devops_client import AzureDevOpsClient

client = AzureDevOpsClient()
pipelines = client.list_pipelines()

print("Pipelines found:")
for pipeline in pipelines.get("value", []):
    print("-", pipeline["name"])
