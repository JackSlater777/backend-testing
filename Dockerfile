FROM python:3.10-alpine

USER root

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

# Для выгрузки allure-отчета на сервер TestOps
# RUN chmod +x ./scripts/allurectl_windows_amd64 ./scripts/allure_report_sender_bitbucket.sh ./scripts/allure_report_sender_bitbucket.sh

CMD pytest tests/trading_app/* -s -v --env=localhost --alluredir=output/pytest_allure_reports --clean-alluredir

# ****************************************************************************************************************
# docker build -t trading_app_tests .
# docker run trading_app_tests
# docker ps -lq  # it returns the last container <id> being run
# docker cp <id>:/output/pytest_allure_reports .
