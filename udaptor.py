import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,  get_jwt_identity
import datetime
from datetime import timedelta
from config import ProductionConfig, DevelopmentConfig
import boto3
from exceptions import AuthenticationException, Generic
from config import get_env_variable, get_aws_keys
import logging


app = Flask(__name__)
env = get_env_variable('env')
if env == 'dev':
    app.config.from_object(DevelopmentConfig)
elif env == 'prod':
    app.config.from_object(ProductionConfig)
else:
    logging.error("Error. Invalid Environment. Must be Either dev or prod")


db = SQLAlchemy(app)
jwt = JWTManager(app)

# BUCKET_URL = 'https://s3-eu-west-1.amazonaws.com/udaptor/'
# FOLDER_NAME = 'input-files/'
# BUCKET_NAME = 'udaptor'

BUCKET_URL = get_env_variable('BUCKET_URL')
FOLDER_NAME = get_env_variable('FOLDER_NAME')
BUCKET_NAME = get_env_variable('BUCKET_NAME')


@app.route('/')
def index():
    return "Hello, world!", 200


@app.route('/v1.0/login', methods=['POST'])
def login():
    from models import User
    json_req = request.get_json()
    username = json_req.get("username", None)
    password = json_req.get("password", None)
    if not (username and password):
        raise AuthenticationException("Username or pass not provided")
    user = db.session.query(User).filter_by(email=username).first()
    if user is not None:
        if passwords_match(user, password):
            # Pass the User id as the payload identity
            token_expiration = timedelta(days=365)
            access_token = create_access_token(str(user.id), expires_delta= token_expiration)
            return jsonify({
                "access_token" : access_token
            })
        else :
            raise AuthenticationException("Invalid Username or password")

    else:
        raise AuthenticationException("Invalid User")




@app.route('/v1.0/file', methods=['POST'])
@jwt_required
def upload_file():
    file = request.files['file']
    user_id = get_jwt_identity()
    data = json.loads(request.form['json'])
    try:
        job = upload_file(file, user_id, data)
        db.session.add(job)
        db.session.commit()
        return jsonify({
            "success" : True,
            "message" : "We have started processing your file, please wait for a few minutes"
        })
    except Exception as er:
        logging.error(er)
        raise Generic("Internal Server Error Occurred")


@app.errorhandler(Generic)
def error_handler(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def passwords_match(user, password):
    return password == user.password

def upload_file(file, user_id, data):
    from models import Job, PossibleJobStates
    aws_keys = get_aws_keys()
    session = boto3.Session(
        aws_access_key_id=aws_keys[0],
        aws_secret_access_key=aws_keys[1]
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    # This filename is done for debugging purposes, but also to ensure uniqueness on S3
    current_time = datetime.datetime.now()
    user_id = str(user_id)
    file_name = "{}_{}_{}_{}_{}".format(file.filename.replace(" ", "_"), user_id, data['input_vendor'], data['output_vendor'], str(current_time).replace(" ", "-"))
    s3_key = FOLDER_NAME + file_name

    try:
        bucket.put_object(Key=s3_key, Body=file)
    except:
        raise Generic('Error: Could not upload file')

    file_location = BUCKET_URL + s3_key
    job_state = Job(
        user_id = user_id,
        input_vendor = data['input_vendor'],
        output_vendor = data['output_vendor'],
        timestamp = current_time,
        file_url = file_location,
        state = PossibleJobStates.STARTED
    )

    return job_state


def get_output_file_url(user_id, data):
    input_vendor = data['input_vendor']
    output_vendor = data['output_vendor']
    json_req = jsonify({

    })
    return None

if __name__ == '__main__':
    app.run()