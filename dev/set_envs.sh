#!/bin/bash

ENV_FILE=dev/.env

if [ -f $ENV_FILE ]; then
  export $(echo $(cat $ENV_FILE | sed 's/#.*//g' | xargs) | envsubst)
fi