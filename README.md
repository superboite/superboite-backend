 # Install VM 


## SSL VS Code connection 
    * add visual code
    * ```Host superboite-vm
        HostName 34.125.61.37
        User mdelobelle
        IdentityFile  ~/.ssh/little-vm```

     $ add ssl certificatiate on VM


## Install git
```sudo apt update```
```sudo apt upgrade```
```sudo apt install git```
```ssh-keygen -t rsa -b 4096 -C "maximedelobelle@gmail.com"```
```eval "$(ssh-agent -s)"```
```cat  cat ~/.ssh/id_rsa.pub```
```git config --global user.name 'maxdelob'```
```git config --global user.name 'maximedelobelle@gmail.com'```
```git clone git@github.com:superboite/superboite-backend.git```


## Make python 3 to Phyton 
```nano ~/.bashrc```
```alias python=python3```
```source ~/.bashrc```

## Init glcould
  ```gcloud auth login```

## Poetrty install 
  ```sudo apt-get install python3-distutils```
  ```sudo curl -sSL https://install.python-poetry.org | python3 - ```
  ```export PATH="$HOME/.local/bin:$PATH"```

## Install Make
   ```sudo apt-get install make```


## Install Docker 

### Add Docker's official GPG key:
```sudo apt-get update```
```sudo apt-get install ca-certificates curl gnupg```
```sudo install -m 0755 -d /etc/apt/keyrings```
```curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg```
```sudo chmod a+r /etc/apt/keyrings/docker.gpg```

### Add the repository to Apt sources:

```echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

```
```sudo apt-get update```

```sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin```


### Remove the sudo before every docker command 

```sudo usermod -aG docker mdelobelle```
```newgrp docker```


## Install direnv