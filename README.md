### Acquire assestment
This is version 0.0.1 of automation tool.

### Environment requirements
* Python 3
* Safari
* Internet

### Intall and run on local machine
1. Safari
   1. Enable "Allow Remote Automation" in "Develop".
   2. Resize window to left space for terminal application.
2. Terminal
   1. Go inside project folder (acq_test).
   2. Execute following commands, in LOGROOTDIR you can find screenshots
    ```
    python3 -m venv tmp_venv
    source tmp_venv/bin/activate
    pip install -r requirements.txt
    export PYTHONPATH=$(pwd)
    export LOGROOTDIR=$(pwd)'/logs/'
    ```
3. Specify TEST_ACCOUNT, TEST_EMAIL and TEST_PWD in acq/configuration/conf.py
4. Run command below
    ```
   python acq/acq_main.py
    ```
5. Profit!

### Run on CI
Standart Jinkins job with allocated host for UI should be enought at this point.<br> 
Travis is not applicable for UI due to images limitation:<br>
https://app.travis-ci.com/github/lobgr/acq_test/builds <br>
Command line tests can work fine<br>
https://app.travis-ci.com/github/lobgr/acq_test/jobs/562046556 <br>
The tool can be virtualized and ditributed according to capacities.
