#!/bin/bash
export env="dev"
export aws_access_key_id="AKIAZZ4B4LYGJNZLMFXU"
export aws_secret_key="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"
export dev_postgres_user=""
export dev_postgres_pw=""
export dev_postgres_url="localhost"
export dev_postgres_db="udaptor_dev"
export SQLALCHEMY_DATABASE_URI="postgresql://localhost/udaptor_dev"
export SECRET_KEY="1335033206121610771176501449150036155913"
export BUCKET_URL="https://s3-eu-west-1.amazonaws.com/udaptor/"
export FOLDER_NAME="input-files/"
export BUCKET_NAME="udaptor"
export udaptor_batch_service="http://localhost:8080/v1/job"
export postgres_timeout=10

printenv | grep "DEBUG\|STARTUP_SIGNUP_TABLE\|AWS_REGION\|NEW_SIGNUP_TOPIC"
