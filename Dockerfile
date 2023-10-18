FROM python:3.10-alpine

USER root

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

RUN chmod +x ./scripts/allurectl_windows_amd64 ./scripts/allure_report_sender_bitbucket.sh ./scripts/allure_report_sender_bitbucket.sh

# CMD pytest tests/functional/* -s -v --alluredir=output/pytest_allure_reports --clean-alluredir

# ****************************************************************************************************************
# docker build -t price_calc .
# docker run price_calc
# docker ps -lq  # it returns the last container <id> being run
# docker cp <id>:/output/pytest_allure_reports .
