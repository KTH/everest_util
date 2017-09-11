#!/bin/sh

echo "******************************************************************\n"
echo "Make sure to run 'pipenv install --dev' before running these tests\n"
echo "******************************************************************\n"

pipenv run green -vv --run-coverage test
