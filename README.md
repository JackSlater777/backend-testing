1. To launch tests, run:

> pytest tests/functional/test_functional.py -s --alluredir=output --clean-alluredir

> pytest tests/integration/test_integration.py -s --alluredir=output --clean-alluredir

2. To change environment variables, do:

> cats_core/env_vars/__init__.py -> change the last argument of "current_env" variable to the name of needed module

3. To run allure report on local server, run:

> allure serve output

4. To upload allure report to the server: 

first, install Allure TestOps Support plugin:

> File -> Settings... -> Plugins -> search "Allure TestOps Support" -> install

second, define project settings:

> File -> Tools -> Allure Testops -> add info

third, generate token; go to Allure Testops server and do:

> Account settings -> API TOKENS option -> create

fourth, upload the results:

> RMC on output/pytest_allure_reports -> Allure Testops -> Upload Results -> select a project

Uploaded result will be in the Launches section.
