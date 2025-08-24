#!/bin/bash

set -ex

echo "Zipping lambda package"

LAMBDA_FUNC_PATH="src/lambda_function"
cd $LAMBDA_FUNC_PATH

rm -rf package

mkdir package
pip install --target ./package requests

LAMBDA_FUNCTION_ZIP="lambda_package.zip"

cd package
zip -r ../$LAMBDA_FUNCTION_ZIP .

cd ..
zip $LAMBDA_FUNCTION_ZIP index.py
