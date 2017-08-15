# SIGMOD17Reproducibility

Code | Information
--- |  :---:
**Programming Language** | Python
Compiler Info | Python 2.7 Interpreter
Packages/Libraries Needed | Python Anaconda (See details below)

## Datasets

Experiments require MySQL **5.6**. The code does not have any version specific features and should work on all version after **5.6** too.

Below are the dataset files. These scripts assume that there is no database with the name **graph**, **qa**, **ssb** and **tpch**. To import the database, use the following command replace `<filename>` with **graph, qa, ssb** and **tpch**.

```ruby
mysql -u <username> -p < <filename>.sql
```

1. https://www.dropbox.com/s/7mb6snalnxndlxp/graph.sql?dl=0
2. https://www.dropbox.com/s/aqop2af4i39pe1w/qa.sql?dl=0
3. https://www.dropbox.com/s/y609n91exdishyf/ssb.sql?dl=0
4. https://www.dropbox.com/s/kdk4iq9kngu5cr2/tpch.sql?dl=0

## Hardware Information

All experiments were performed on 16GB machine installed with OS X 10.10.5. There are no special hardware requirements and results should be easily reproducable on any standard machine.


Hardware | Information
--- |  :---:
Processor | 2.2 GHz Intel Core i7
Memory | 16 GB 1600 MHz DDR3
Cores | quad core
Cache | 6MB shared L3 cache

## Environment Setup

* Execute the database scripts. Once the scripts are executed, you should see *4* databases in MySQL.
* Install Anaconda as explained [here](https://conda.io/docs/install/full.html#os-x-anaconda-install)
* We will replicate the python code environment using conda's virtual environment. Execute the following command from the top level of the directory so that `environment.yml` is present. This will create a private virtual python 2.7 based anaconda environment with all dependencies loaded
```ruby
conda env create -f environment.yml
```
* Update constants/db.py file with the username and password for the database. Setup is now complete


## Running Experiments

Below is the complete set of experiments to reproduce results in the [paper](http://dl.acm.org/citation.cfm?id=3064017).

