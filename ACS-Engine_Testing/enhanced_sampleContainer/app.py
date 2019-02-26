from flask import Flask, request, render_template
from fabric.api import local
import os
import socket

runtime = str("None")
try:
    k8s_node_name = str(os.environ['MY_NODE_NAME'])
    k8s_pod_name = str(os.environ['MY_POD_NAME'])
    k8s_pod_namespace = str(os.environ['MY_POD_NAMESPACE'])
    k8s_pod_ip = str(os.environ['MY_POD_IP'])
    k8s_serviceaccount_name = str(os.environ['MY_POD_SERVICE_ACCOUNT'])
    runtime = str("Kubernetes")
except:
    runtime = str("Docker")
    
ID_output = str(local("""cat /proc/self/cgroup | head -n 1 | cut -d '/' -f3""", capture=True))
app = Flask(__name__)


@app.route('/')
def hello_world():
    if 'docker' in runtime.lower():
        return render_template("docker_index.html", container_IP=str(socket.gethostbyname(socket.gethostname())), container_ID=ID_output, remote_IP=str(request.remote_addr), HostName=str(socket.gethostname()))
    else:
        return render_template("k8s_enhance_index.html", k8s_node_name=k8s_node_name, k8s_pod_name=k8s_pod_name, k8s_pod_namespace=k8s_pod_namespace, remote_IP=str(request.remote_addr),k8s_pod_ip=k8s_pod_ip, k8s_serviceaccount_name=k8s_serviceaccount_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
