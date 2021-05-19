from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict
import sqlalchemy
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)

print('This is error output', file=sys.stderr)
print('This is standard output', file=sys.stdout)
app = Flask(__name__)
CORS(app, resources=r'/*')

#server 34.101.128.62
#user root
#pass 9890
#instance con name dementia-cares:asia-southeast2:dementia-care



logger = logging.getLogger()


def init_connection_engine():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]

        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]

        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]

        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]

    }
    return init_unix_connection_engine(db_config)


def init_unix_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_socket]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["hello"]
    db_pass = os.environ["1234"]
    db_name = os.environ["DeCare"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR" ,"/cloudsql")
    cloud_sql_connection_name = os.environ["dementia-cares:asia-southeast2:dementia-care"]
    app.logger.info(cloud_sql_connection_name)
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_socket": "{}/{}".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )
    # [END cloud_sql_mysql_sqlalchemy_create_socket]

    return pool



@app.before_first_request
def create_tables():
    global db
    db = init_connection_engine()
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS votes "
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "candidate CHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
        )

@app.route('/')
def index():
    app.logger.info('hello')
    print('hello')
    return 'Hello Cloud V3 with trigger!'
    

@app.route('/predict', methods=['POST'])
def get_prediction():
    json = request.get_json()
    print(json)
    
    if json is None:
        return jsonify({'error': 'invalid input'})

    prediction, confident = predict.predict(json)
    return jsonify({'prediction': prediction, 'confident': confident})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)