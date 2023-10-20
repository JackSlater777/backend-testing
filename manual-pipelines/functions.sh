#!/usr/bin/env bash
ALLURE_RESULT_DIR=/app/allure_result
JUNIT_XML_PATH="${CI_PROJECT_DIR}/regression_junit.xml"

generate_executor_json() {
    JSON_STRING="{
      \"name\":\"Gitlab\",
      \"type\":\"gitlab\",
      \"url\":\"https://gitlab.ozon.ru\",
      \"buildOrder\":\"$CI_JOB_ID\",
      \"buildName\":\"$CI_JOB_NAME#$CI_JOB_ID\",
      \"buildUrl\":\"$CI_JOB_URL\",
      \"reportUrl\":'',
      \"reportName\":'AllureReport',
    }"
    echo $JSON_STRING > executor.json
    cat executor.json
    [ ! -d $ALLURE_RESULT_DIR ] && echo "[generate_executor_json] Error: Directory $ALLURE_RESULT_DIR does not exist." && return
    cp executor.json $ALLURE_RESULT_DIR/executor.json
}

run_tests() {
    set -x
    cd /app/
    echo $TEST_ENV
    echo $MESHVERSION
    allurectl job-run start
    LAUNCH_ID=$(echo $(tail -n 1 $CI_PROJECT_DIR/launch_data) | sed 's/ .*//')
    allurectl watch --results $ALLURE_RESULT_DIR --ignore-passed-test-attachments --launch-id $LAUNCH_ID \
        -- bash -c "pytest $TEST_FOLDER --env=$TEST_ENV \
        --reruns $RETRIES \
        --last-failed \
        --disable-warnings \
        -n $PARALLEL_THREADS \
        --dist loadgroup \
        --alluredir $ALLURE_RESULT_DIR \
        --wms.extra_headers=X-O3-Meshversion:$MESHVERSION \
        --junitxml=$JUNIT_XML_PATH \
        --collect_traces=True --continue-on-collection-errors --show-capture=no -vv $EXTRA_OPTIONS"
}

send_old_report_per_suite() {
    set -x
    [ ! -d $ALLURE_RESULT_DIR ] && echo "[send_report] Error: Directory $ALLURE_RESULT_DIR does not exist." && return
    zip -q allure_results.zip -jr $ALLURE_RESULT_DIR
    report_allure=$(curl -s --retry 5 -F file=@./allure_results.zip "http://allure.s.o3.ru/upload?group=$ALLURE_REPORT_GROUP&project=$REPORT_PROJECT_NAME&version=QA")
    echo "$report_allure"
}

send_message() {
    report_allure=$1
    echo "report_allure=$report_allure"
    report_allure_ceph=${report_allure//$ALLURE_DOMAIN/$CEPH_DOMAIN}index.html
    echo "report_allure_ceph=$report_allure_ceph"
    test_result=$(grep testsuite $JUNIT_XML_PATH | sed "s/.*<testsuite//;s/><testcase.*//; s/\"/\\\"/g"| head -1| sed "s/ /\n/g")
    echo "test_result=$test_result"
    LAUNCH_ID=$(echo $(tail -n 1 $CI_PROJECT_DIR/launch_data) | sed 's/ .*//')
    allure_testops_link=$ALLURE_ENDPOINT_UI/launch/$LAUNCH_ID
    echo "allure_testops_link=$allure_testops_link"
    python report.py $REPORT_PROJECT_NAME "$test_result" $allure_testops_link $report_allure $CHANNEL $TEST_ENV $TEST_FOLDER \
    $GITLAB_USER_LOGIN $CI_PROJECT_NAME $CI_PIPELINE_SOURCE $CI_PIPELINE_URL $PARALLEL_THREADS "$MESHVERSION" $RETRIES
}

save_job_cache() {
    # save pytest cache in another dir, because /app/ disappears before caching
    root="$CI_PROJECT_DIR/$CI_JOB_NAME-$CI_PIPELINE_ID"

    echo "$(find /app/.pytest_cache/v/cache | wc -l) files in pytest_cache to save..."
    mkdir -p "$root"/pytest_cache
    mv /app/.pytest_cache/v/cache "$root"/pytest_cache
    echo "$(find "$root"/pytest_cache | wc -l) cache files correctly saved"

    echo "$(find /app/allure_result/ | wc -l) files in allure_result to zip..."
    mkdir "$root"/allure_result/
    zip -q "$root"/allure_result/allure_results.zip -jr $ALLURE_RESULT_DIR
    echo "Report files correctly zipped"
}

load_job_cache() {
    # unpack pytest cache into /app/.pytest_cache/v/cache and delete temp directory
    cache_dir=$(find . -name "$CI_JOB_NAME-$CI_PIPELINE_ID" | head -n 1)
    if [ "$cache_dir" ] && [ "$ONLY_LAST_FAILED" == "true" ]; then
      echo "Load pytest_cache..."
      mkdir -p /app/.pytest_cache/v/cache
      mv "$cache_dir"/pytest_cache/cache /app/.pytest_cache/v
      echo "$(find /app/.pytest_cache/v | wc -l) cache files correctly moved"

      echo "Unzip cached allure report..."
      mkdir -p /app/allure_result/
      unzip -q -o -d /app/allure_results/ "$cache_dir"/allure_result/allure_results.zip
      echo "$(find /app/allure_result | wc -l) report files correctly unzipped"

      rm -r "$cache_dir"
    fi
}

clone_manual_pipelines() {
    if [ "$CI_PROJECT_NAME" != "manual-pipelines" ]; then
      git clone https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/supply-chain-qa/manual-pipelines.git
      cp -a manual-pipelines/* ./
    fi
}
