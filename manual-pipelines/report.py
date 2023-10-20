import json
import sys
import records
import requests
from warden_client.wrapper import warden_required
from framework.vault.manager import get_vault_value

REPORT_TEMPLATE = """
| **PASSED PERCENT** | **DURATION** | **STARTED BY** | :allure_passed:**PASSED** | :allure_broken:**BROKEN** | :allure_failed:**FAILED** | :allure_skipped:**SKIPPED** | **QUANTITY** | **THREADS** | **RETRIES** |
| :----------------: | :----------: | :---------------------: | :-----------------------: | :-----------------------:| :-----------------------: | :-------------------------: | :-------------------------: | :-----------: | :-----------: | :-----------: |
| _{passed_percent}%_ | _{time}_ | _{started_by}_ | {passed} | {broken} | {failed} | {skipped} |   {quantity}  |  {threads}  |  {retries}  |
"""

list_args = sys.argv

project_name, test_results, allure_testops_link, allure_link, channel, test_env, test_folder, \
pipeline_author, pipeline_project, pipeline_resource, pipeline_url, parallel_threads, mesh_version, retries = list_args[1:]

print(test_results)
test_results = test_results.split('\n')
print(test_results)
test_results_dict = {}
test_results = filter(None, test_results)
for b in test_results:
    i = b.split('=')
    test_results_dict[i[0]] = i[1].replace('"', '')


def get_from_dict(key):
    return test_results_dict.get(key, 0)


passed_percent = 0.9


def get_human_time(time_in_seconds):
    m, s = divmod(time_in_seconds, 60)
    h, m = divmod(m, 60)
    human_h = f'{h}h ' if h else ''
    human_m = f'{m}m ' if m else ''
    human_s = f'{s}s' if s else ''
    return f'{human_h}{human_m}{human_s}'


def get_test_stats():
    total = int(get_from_dict("tests"))
    failed = int(get_from_dict("failures"))
    broken = int(get_from_dict("errors"))
    skipped = int(get_from_dict("skipped"))
    passed = total - failed - skipped - broken
    passed_with_skipped = passed + skipped if passed > 0 else passed
    exec_time = get_from_dict("time")
    human_time = get_human_time(int(float(exec_time)))
    timestamp = get_from_dict("timestamp")

    tests_stats = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "broken": broken,
        "skipped": skipped,
        "time": exec_time,
        "timestamp": timestamp,
        "human_time": human_time,
        "passed_percent": round(passed_with_skipped / total * 100, 2)
    }
    tests_stats.update(get_color_emoji_result(total, passed, skipped))
    return tests_stats


def get_color_emoji_result(total, passed, skipped):
    passed_with_skipped = passed + skipped if passed > 0 else passed
    if passed + skipped == total:
        color = "#56a64f"
        emoji = ":nichosi:"
    elif passed_with_skipped / total >= passed_percent:
        color = "#f6ff00"
        emoji = ":norma:"
    else:
        color = "#ff0000"
        emoji = ":technological:"
    return {
        "color": color,
        "emoji": emoji
    }


def check_correct_allure_testops_link(allure_testops_link: str):
    """check launch id exists and doesn't equal 0"""
    if not allure_testops_link.endswith("/"):
        launch_id = allure_testops_link.split("/")[-1]
        if launch_id:
            return True
    return False


stats = get_test_stats()


def get_started_by():
    return pipeline_author if pipeline_resource != "schedule" else pipeline_resource


@warden_required
def get_vault_credential(credential_name: str):
    return get_vault_value(key=credential_name)


def get_results_pattern(color, allure_testops_link=None, allure_link=None, pipeline_url=None, mesh_version=None):
    message = REPORT_TEMPLATE.format(
        passed_percent=stats["passed_percent"],
        passed=stats["passed"],
        broken=stats["broken"],
        failed=stats["failed"],
        skipped=stats["skipped"],
        quantity=stats["total"],
        time=stats["human_time"],
        threads=parallel_threads,
        retries=retries,
        started_by=get_started_by()
    )
    fields = []
    if allure_testops_link and check_correct_allure_testops_link(allure_testops_link):
        fields.append(
            {
                "short": True,
                "title": ":allure-testops:",
                "value": f"<{allure_testops_link}|Allure TestOps>"
            }
        )
    if "allure" in allure_link:
        value = f"<{allure_link}|Allure>"
    else:
        value = "Отчет в Allure не был загружен"
    fields.append(
        {
            "short": True,
            "title": ":allure:",
            "value": value
        }
    )

    if pipeline_url:
        fields.append(
            {
                "short": True,
                "title": ":gitlab:",
                "value": f"<{pipeline_url}|Gitlab job>"
            }
        )
    if mesh_version:
        fields.append(
            {
                "short": True,
                "title": ":mesh:",
                "value": f"{mesh_version}"
            }
        )
    return {
        "color": color,
        "text": message,
        "fields": fields
    }


for channel_name in channel.split(","):
    mattermost_url = get_vault_credential("mattermost_url")
    result_pattern = get_results_pattern(stats["color"], allure_testops_link, allure_link, pipeline_url, mesh_version)
    payload = {
        "channel": channel_name,
        "username": project_name,
        "icon_emoji": stats["emoji"],
        "attachments": [result_pattern]
    }
    r = requests.post(mattermost_url, data=json.dumps(payload))
    print(r.text)

if test_env == "stg":
    db_credential = get_vault_credential("pytest-runner")
    db = records.Database(db_credential)
    db.query(
        "INSERT INTO stg_run_log "
        "(service_name, test_folder, passed, failed, skipped, inconclusive, exec_time, launch_time) "
        "VALUES "
        f"('{project_name}', '{test_folder}', {stats['passed']}, {stats['failed']}, "
        f"{stats['skipped']}, {stats['broken']}, {stats['time']}, "
        f"TIMESTAMP '{stats['timestamp']}');"
    )
