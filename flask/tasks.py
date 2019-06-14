import config
from flask import Flask
from celery import Celery
from vrops import pull_data_from_vrops

application = Flask(__name__)
application.config.from_object('config')

def make_celery(application):
    celery = Celery(application.import_name, backend=application.config['CELERY_RESULT_BACKEND'],
                    broker=application.config['CELERY_BROKER_URL'])
    celery.conf.update(application.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with application.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(application)

@celery.task(name='call.vrops.connect')
def call_vrops_connect(vropshost, vropsuser, vropspass, customer_id):
    test_connect = 'call vrops connect was called\n' + vropshost + '\n' + vropsuser + '\n'+ vropspass + '\n'+ customer_id + '\n'
    with open('test_connect.log', 'a') as j:
        j.write(test_connect)
    vhost = vropshost
    vuser = vropsuser
    vpass = vropspass
    cust_id = customer_id
    # pull_data_from_vrops(vhost, vuser, vpass, cust_id)

@celery.task(name='call.test.call')
def test_call():
    test_call = 'test_call was called\n ' # + vropshost + '\n' + vropsuser + '\n'+ vropspass + '\n'+ customer_id + '\n'
    with open('test_call.log', 'a') as j:
        j.write(test_call)

application.run(host='0.0.0.0', port=5001)