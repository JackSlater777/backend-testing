#!/bin/bash

# default args

allure_id=12
allure_endpoint=https://allure.myserver.ru
git_endpoint=https://cicd-git.myendpoint.ru
allure_results=output

# parsing args

while [ $# -gt 0 ]; do
  case "$1" in
    --app_name=*)           # application name
      app_name="${1#*=}"
      ;;
    --allure_id=*)          # allure project identifier
      allure_id="${1#*=}"
      ;;
    --allure_token=*)       # allure authorization token
      allure_token="${1#*=}"
      ;;
    --git_token=*)          # gitlab authorization token
      git_token="${1#*=}"
      ;;
    --project_id=*)         # gitlab application project identifier
      project_id="${1#*=}"
      ;;
    --allure_endpoint=*)    # allure endpoint host
      allure_endpoint="${1#*=}"
      ;;
    --git_endpoint=*)       # git endpoint host
      git_endpoint="${1#*=}"
      ;;
    --allure_results=*)     # directory with allure reports
      allure_results="${1#*=}"
      ;;
    *)
    printf "***************************\n"
    printf "* Error: Invalid argument.*\n"
    printf "***************************\n"
    exit 1
  esac
  shift
done


if [ -z "$app_name" ];
then
    printf "* Error: Please provide an app_name. *\n"
    exit 1
fi

if [ -z "$allure_token" ];
then
    printf "* Error: Please provide an allure_token. *\n"
    exit 1
fi

if [ -z "$git_token" ];
then
    printf "* Error: Please provide a git_token. *\n"
    exit 1
fi

# getting current date and time
printf -v date '%(%Y-%m-%d %H:%M:%S)T\n' -1

# getting current application version from gitlab tags
printf "\nRC version: $appversion \n"
app_version=$(echo $appversion | awk '{gsub(v.|-rc, "", $0); print $0}')

if [ -z "$app_version" ];
then
    git_tags_url="$git_endpoint/api/v4/projects/$project_id/repository/tags?order_by=updated&sort=desc"
    app_version=$(curl --request GET "$git_tags_url" --header "PRIVATE-TOKEN: $git_token" | jq -r '.[0].name')
fi

printf "___________________________\n"
printf "\nCurrent $app_name version: $app_version \n"
printf "___________________________\n\n"


# exporting allure variables
export ALLURE_ENDPOINT=$allure_endpoint
export ALLURE_TOKEN=$allure_token
export ALLURE_PROJECT_ID=$allure_id
export ALLURE_LAUNCH_NAME="QG $app_name v.$app_version | $date"
export ALLURE_RESULTS=$allure_results

# upload report to allure server
allurectl_result="$(./grapple_core/allurectl upload $ALLURE_RESULTS --launch-tags "$app_name, $variablefiles")"

# parse allurectl answer and get link to allure report
printf "$allurectl_result \n"
printf "___________________________\n"
report_id="$(printf "$allurectl_result" | awk '/stopped .+ launch/{gsub(/(\[|\])/, "", $7);print $7}')"

if [ -z "$report_id" ];
then
    printf "\n*** Error: test results weren't uploaded! ***\n"
    exit 1
else
    allure_report_url=$allure_endpoint/launch/$report_id
    printf "\n*** Test results were successfully uploaded to allure! ***\n"
    printf "\nLink to allure report: $allure_report_url\n\n"

    # get merge request id
    git_merge_url="$git_endpoint/api/v4/projects/$project_id/merge_requests"
    merge_request_id=$(curl --request GET "$git_merge_url" --header "PRIVATE-TOKEN: $git_token" | jq -r '.[0].iid')

    printf "Open merge request id: $merge_request_id \n"

    # send git comment with allure report link
    emoji=:robot:%20
    allure_message="""$emoji This message was generated automatically $emoji

Please check the test results by following the link below!
Link to allure report: [$allure_report_url]($allure_report_url)"""
    git_comment_url="$git_endpoint/api/v4/projects/$project_id/merge_requests/${merge_request_id}/notes"
    curl --request POST "$git_comment_url" --header "PRIVATE-TOKEN: $git_token" --data "body=$allure_message"

    exit 1
fi