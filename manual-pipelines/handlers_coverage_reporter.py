import subprocess
import os


report_settings = [
    {
        "swagger": "http://wms-csharp-web-supply.wms.stg.s.o3.ru:84/swagger.json",
        "page_id": "102088002",
        "service_name": "WMS-Supply-STG"
    }
]

ci_project_dir = os.getenv("CI_PROJECT_DIR")
jira_user = os.getenv("JIRA_USER")
jira_password = os.getenv("JIRA_PASSWORD")
for report_data in report_settings:
    print(
        f"handlers_coverage "
        f"-l {ci_project_dir}/report_data -sp "
        f"-sw {report_data['swagger']} "
        f"-ju {jira_user} "
        f"-jp {jira_password} "
        f"--page_id {report_data['page_id']} "
        f"--service_name '# [{report_data['service_name']}]' -cs SC"
    )
    subprocess.run(
        f"handlers_coverage "
        f"-l {ci_project_dir}/report_data -sp "
        f"-sw {report_data['swagger']} "
        f"-ju {jira_user} "
        f"-jp {jira_password} "
        f"--page_id {report_data['page_id']} "
        f"--service_name '# [{report_data['service_name']}]' -cs SC", shell=True
    )
