from azure_devops_client import AzureDevOpsClient

client = AzureDevOpsClient()
data = client.get_failed_runs(24)

print("Failed runs:")
for build in data.get("value", []):
    print("-", build["definition"]["name"], build["finishTime"])
