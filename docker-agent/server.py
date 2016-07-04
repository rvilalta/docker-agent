from flask import Flask
import thread
## EXAMPLE IMPORT SERVER MODELS
import docker_agent
import backend_api




app = Flask(__name__)
app.register_blueprint(getattr(docker_agent, "docker_agent"))
app.register_blueprint(getattr(backend_api, 'backend_api'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8080, debug=True)
    