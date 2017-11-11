import argparse
from os import path
from flask import Flask
from jinja2 import Template
from werkzeug.contrib.fixers import ProxyFix
app = Flask("demo flask server")

index_path = path.join(
    # Grab the parent directory path
    path.dirname(path.abspath(path.dirname(__name__))),
    "template",
    "index.html"
)


@app.route("/", methods=["GET"])
def index():
    with open(index_path, 'r') as fstream:
        template = Template(fstream.read())
    output = template.render(
        title="Flask Server",
        description="Flask, the python (micro)framework"
    )
    return output.encode('ascii')


def run_flask(app):
    parser = argparse.ArgumentParser(
        description='Example Flask server'
    )
    parser.add_argument(
        "-port",
        "--port",
        default=8000,
        help="Port to run server on"
    )
    parser.add_argument(
        "-host",
        "--host",
        default="0.0.0.0",
        help="Host to run server on"
    )
    parser.add_argument(
        "--debug",
        default=False,
        help="Debug Mode"
    )

    args = parser.parse_args()
    app.logger.info(
        "Demo Flask server running at {0}:{1}".format(
            args.host,
            args.port
        )
    )
    app.run(
        host=args.host,
        port=int(args.port),
        debug=bool(args.debug),
        threaded=True
    )


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    run_flask(app)
