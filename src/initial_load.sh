#!/bin/sh

# source pg PGPASSWORD
source ~/pg_pass

# Variables
HOST='mid-term-project.ca2jkepgjpne.us-east-2.rds.amazonaws.com'
PORT=5432
DATABASE='mid_term_project'
USER=lhl_student
FILE='initial_load.sql'

echo Extracting data ...

# Extract Sample data for Midterm project
psql -h $HOST -p $PORT -d $DATABASE -U $USER -f $FILE

# get status
rc=$?

echo Process ended Status: $rc
