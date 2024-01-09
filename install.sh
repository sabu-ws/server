#!/bin/bash

# UPDATE & UPGRADE
apt update
apt upgrade -y

# USER SABU
useradd sabu --home /home/sabu --create-home --shell /bin/bash --password '$1$Av4Qv9gg$flzrWXMp0qC8aVEuu6XBF1'
usermod -a -G adm sabu


# USER SVC-SABU & RIGHTS
mkdir -p /sabu/
useradd svc-sabu --home /sabu/ --shell /bin/false
usermod -a -G adm svc-sabu

chown -R svc-sabu:svc-sabu /sabu/
chmod -R 0750 /sabu/


# FAKE DISK
mkdir -p /data/sdb1/{data, quarantine}
chown -R svc-sabu:svc-sabu /sabu/
chmod -R 0750 /sabu/


# CLONE REPO 
apt install git -y
cd /sabu/
git clone https://github.com/sabu-ws/server.git


# DISABLE IPV6
cp /sabu/server/deploy/10-disable-ipv6.conf /etc/sysctl.d/10-disable-ipv6.conf
sysctl -p -f /etc/sysctl.d/10-disable-ipv6.conf


# SSH CONFIGURATION
cp /sabu/server/deploy/sshd_config /etc/ssh/sshd_config
systemctl restart ssh


# SUDO COMMAND
apt install sudo -y
cp /sabu/server/deploy/sabu.sudo /etc/sudoers.d/sabu


# DEPLOY NODEJS
apt install curl dirmngr apt-transport-https lsb-release ca-certificates gnupg -y
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
apt update

apt install nodejs -y


# DEPLOY NGINX
apt install nginx -y

rm /etc/nginx/sites-available/default
rm /etc/nginx/sites-enabled/default

mkdir -p /sabu/nginx/
mkdir -p /sabu/logs/server/nginx/
cp /sabu/server/deploy/nginx/maintenance.html /sabu/nginx/maintenance.html
sed -i 's/www-data/svc-sabu/g' /etc/nginx/nginx.conf

mkdir -p /sabu/ssl/private/

# GEN AUTOIGN CERTIF
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /sabu/ssl/private/sabu.key -out /sabu/ssl/sabu.crt -subj "/C=FR/ST=BRITTANY/L=Rennes/O=SABU/OU=SABU/CN=sabu.local"

cp /sabu/server/deploy/nginx/sabu.conf /etc/nginx/sites-available/sabu.conf
ln -s /etc/nginx/sites-available/sabu.conf /etc/nginx/sites-enabled/sabu.conf

nginx -t
systemctl restart nginx


# DEPLOY PYTHON3
apt install python3 python3-pip python3-venv -y

cd /sabu/
python3 -m venv sabu-venv
source /sabu/sabu-venv/bin/activate

pip3 install -r /sabu/server/requirements.txt
pip3 freeze


# DEPLOY POSTGRESQL
apt install postgresql -y

sed -i "/listen_addresses = 'localhost'/s/^#//g" /etc/postgresql/15/main/postgresql.conf

cp /sabu/server/.env.model /sabu/server/.env

source /sabu/server/.env

su - postgres -c "createuser $POSTGRES_USER"
sudo -u postgres psql -c "ALTER USER $POSTGRES_USER WITH password '$POSTGRES_PASSWORD'"
su - postgres -c "createdb $POSTGRES_DB -O $POSTGRES_USER"


# DEPLOY NFTABLES
apt install nftables -y


# DEPLOY RSYSLOG
apt install rsyslog -y

# DEPLOY TIMESCALE
apt install gnupg postgresql-common apt-transport-https lsb-release wget -y
sh /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh y
curl -fsSL https://packagecloud.io/timescale/timescaledb/gpgkey | sudo gpg --dearmor -o /etc/apt/keyrings/timescale.gpg
echo "deb [signed-by=/etc/apt/keyrings/timescale.gpg] https://packagecloud.io/timescale/timescaledb/debian/ $(lsb_release -c -s) main" | sudo tee /etc/apt/sources.list.d/timescale.list
apt update

apt install timescaledb-2-postgresql-15 -y
timescaledb-tune --quiet --yes
echo "shared_preload_libraries = 'timescaledb'" >> /etc/postgresql/15/main/postgresql.conf


# DEPLOY SABU
mkdir -p /sabu/logs/server/
cp /sabu/server/deploy/sabu.service /etc/systemd/system/sabu.service
systemctl daemon-reload
systemctl start sabu.service
systemctl enable sabu.service


# CLEAN
apt autoremove -y
apt clean


# FIX PERMS
chown -R svc-sabu:svc-sabu /sabu/
chmod -R 0750 /sabu/

reboot
