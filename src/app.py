from flask import Flask, render_template
from flask import current_app
from . import ColonyEye
app = Flask(__name__)

with app.app_context():
    current_app.logger.info('Running backend startup')
    ColonyEye.run_backend()

@app.route('/')
def home():
    return render_template('index.html')