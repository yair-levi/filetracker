File Tracker Background
-------------
This is a part of full solution to detects duplicat files in directory, 
This micro-serves track file changes in directory and produce changes to changes queue 

Here is description how we define change (is a part of docstring): 

    snapshot is dictionary with file name as key and last modify timestamp as value,
    the function using last directory snapshot and current snapshot to track if there are any changes,
    we have 3 kinds of changes:
    1. modified: going over current snapshot and check if file exist in last snapshot and change time is not same
    2. added: going over current snapshot and check if file are not exist in last snapshot
    3. removed: going over last snapshot and check if file are not exist in current snapshot

    # we're filtering out all the changes on files with "_DUP_#"

I'm using pickle module for saving snapshot of directory, if application is failed or down, application take the last
state from pickle file, pickle file name is md5 of the tracked directory.
please note, when you start track a new directory all existing file will send to worker 
and process of mapping duplicate file will start.


--------------

## python version supported
```sh
Python 3.11.0
```

## Update config
```sh
  $ vim config.yml
```
please change the configuration
```yml
rabitMQ:
   host: localhost
   port: 5672
   queue_name: changes
directory: C:\Users\PycharmProjects\fileTracker\files
```

## Creating Virtual Environments
```sh
  $ python3 -m venv venv
```

## Run Virtual Environments
```sh
  $ source venv/bin/activate
```

## Update pip
```sh
  $ pip install --upgrade pip   
```

## Install requirements
```sh
  $ pip install -r requirements.txt
```

## run application
```shell
  $ python3 main.py
```
