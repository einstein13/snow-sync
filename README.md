# snow-sync
This is ServiceNow instance synchronization server.  
It is designed to be as file exchange program between ServiceNow and local disc.

# Installation

* Download and install latest Python (https://www.python.org/downloads/) or use available from your OS
* Download this repository (https://github.com/einstein13/snow-sync/archive/master.zip)
* Unpack repository to the target folder (ex.: documents/work)
* Run script file "run.py" from your console (command: py run.py)

The program will initialize projects folder (ex.: documents/work/projects) and will be ready to use.

# Basic usage

## Settings up a connection to the ServiceNow

type:  
`add settings`  
and provide:
* Recognizible name (you will see this every time)
* Short name version of the instance (ex.: dev20354)
* Confirm or change URL of the instance
* Username and password for the instance

The connection will be checked and the result will be given to you.

## Define files to exchange

type:  
`add files`  
and provide:
* Type of the object (business rule, user script, ...)
* sys_id of the object

The files should be on your disk, ex.:
documents/work/projects/business_rule/RULE_NAME/script.js, row_data.data

## Basic synchronization between ServiceNow and your computer

type:  
`pull`  
to get all changes from ServiceNow to your computer

type:  
`push`  
to post changes from your computer to the ServiceNow

## More information

type:  
`help`  
to show all topics, not included here

## List of all useful commands

* `exit`
* `help`
* `[show/add/read/edit/delete] settings`
* `[show/add/delete/truncate] files`
* `show record`
* `pull`
* `push`
* `status`
* `watch`
* `unwatch`