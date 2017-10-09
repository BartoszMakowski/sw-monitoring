from flask import Flask, render_template
import yaml
app = Flask(__name__)

@app.route('/')
def main_page():
    with open("etc/sw-mon.yml", 'r') as config:
        try:
            config = yaml.load(config)
            print(config)
        except yaml.YAMLError as exc:
            print(exc)
    return render_template('index.html.j2', nodes = config.get('nodes', {}))

@app.route('/config')
def print_config():
    with open("etc/sw-mon.yml", 'r') as config:
        try:
            config = yaml.load(config)
            print(config)
        except yaml.YAMLError as exc:
            print(exc)
    return render_template('config.html.j2', config = config, nodes = config.get('nodes', {}))

@app.route('/node/<node>')
def node_info(node):
    with open("etc/sw-mon.yml", 'r') as config:
        try:
            config = yaml.load(config)
            print(config)
        except yaml.YAMLError as exc:
            print(exc)
    return render_template('node.html.j2', nodes = config.get('nodes', {}), cur_node = node)