#!/bin/bash

# Create admin model as read
huggingface-cli login
huggingface-cli repo create test0 --organization SE-Test -y
huggingface-cli repo create test0 --organization NicholasSynovic -y

# Create admin model as write
huggingface-cli login
huggingface-cli repo create test1 --organization SE-Test -y
huggingface-cli repo create test1 --organization NicholasSynovic -y

# Create admin model as admin
huggingface-cli login
huggingface-cli repo create test2 --organization SE-Test -y
huggingface-cli repo create test2 --organization NicholasSynovic -y
