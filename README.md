Install VM 


SSL VS Code connection 
    add visual code
    Host superboite-vm
        HostName 34.125.61.37
        User mdelobelle
        IdentityFile  ~/.ssh/little-vm

    add ssl certificatiate on VM


Install git
sudo apt update
sudo apt upgrade
sudo apt install git


Add SSL to git
git config --global user.name 'maxdelob'
git config --global user.name 'maximedelobelle@gmail.com'
ssh-keygen -t rsa -b 4096 -C 'maxime.delobelle@gmal.com'
git clone git@github.com:superboite/superboite-backend.git


Make python 3 to Phyton 
nano ~/.bashrc
alias python=python3
source ~/.bashrc

Init glcould (interactive way)
gcloud init

Poetrty install 
  sudo apt-get install python3-distutils
  sudo curl -sSL https://install.python-poetry.org | python3 - 
  export PATH="$HOME/.local/bin:$PATH"

Install Make
   sudo apt-get install make


Install Docker 
    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo   "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
   40    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo chmod 666 /var/run/docker.sock


