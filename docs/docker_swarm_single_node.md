# Docker Swarm single node on Google Cloud

## Create GCP VM

```
NAME = swarm-single
ZONE = us-central1-b
MACHINE_TYPE = e2-medium
HTTP traffic = On
HTTPS traffic = On
Allow Load Balancer Health checks = On
IMAGE = ubuntu-2004-focal
SIZE = 20 GB
```

## Install Docker

> [How To Install and Use Docker on Ubuntu 20.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)

```
sudo apt update

sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

apt-cache policy docker-ce

sudo apt install docker-ce

sudo systemctl status docker

sudo usermod -aG docker ${USER}

```

For GCP or any IaaS, you need to change your current `$USER` password by access to root and change it

> [How do I change a user password in Ubuntu Linux? - nixCraft (cyberciti.biz)](https://www.cyberciti.biz/faq/change-a-user-password-in-ubuntu-linux-using-passwd/)

```
sudo passwd ${USER}
```

After typing and confirming password, you are now have your own password

```
su - ${USER}
```

Finally, type a Docker command to confirm that you do not need root permission to run command

```
docker ps
```

## Test spawn container with docker swarm

Web application: Python
Name: `web.py`

```python
from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <body>
        <button onclick="fetch('/create-container', { method: 'POST' }).then(response => response.text()).then(alert)">
            Create Container
        </button>
    </body>
    </html>
    '''

@app.route('/create-container', methods=['POST'])
def create_container():
    # Use Docker CLI to create a new container
    subprocess.run(['docker', 'service', 'scale', 'webapp=4'])
    return 'Container Created', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

Initialize swarm

```
sudo docker swarm init
```

Deploy service name `webapp`, image `nginx`, replica `3`

```
sudo docker service create --name webapp --replicas 3 nginx
```

Run app

```
python3 web.py
```

Access to web: `http://<your-vm-ip>`