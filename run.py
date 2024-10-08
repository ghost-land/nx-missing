from flask import Flask, request, jsonify, render_template
from update_data import download_jsons, get_old_updates_lenght, config

app = Flask(__name__)
missing = download_jsons()

@app.route('/', methods=['GET'])
def home():
    return render_template(
        'index.jinja',
        missing=missing,
        old_updates_count=get_old_updates_lenght(missing),
        images_size=config.get('images-size', 100),
        len=len
    )

@app.route('/jsonwebhook', methods=['POST'])
def jsonwebhook():
    global missing
    if request.method == 'POST':
        json_data = request.get_json()
        
        if json_data['repository']['full_name'] == config['data-repo-name']:
            missing = download_jsons()
            return '', 200
        
    return '', 405
    
@app.route('/uptime', methods=['HEAD'])
def uptime():
    return '', 200

if __name__ == '__main__':
    app.run(
        host=config['host'],
        port=config['port'],
        debug=config.get('flask-debug', False)
    )
