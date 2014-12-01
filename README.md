mybic website
=============
###Documentation
[Documentation](wiki)

###Setup
```
#nginx
emacs /etc/yum.repos.d/nginx.repo
yum install nginx

#python
wget http://python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
tar -xvf Python-2.7.6.tar.xz 
cd Python-2.7.6
yum install gcc
./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
emacs /etc/ld.so.conf
make && make altinstall
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
/usr/local/bin/python2.7 ez_setup.py
/usr/local/bin/easy_install-2.7 pip

#postgres
rpm -Uvh http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-redhat93-9.3-1.noarch.rpm
yum install postgresql93-server postgresql93
/etc/init.d/postgresql-9.3 initdb
service postgresql-9.3 start
chkconfig postgresql-9.3 on
yum install postgresql93-devel.x86_64
yum install python-psycopg2.x86_64
sudo /etc/init.d/postgresql-9.3 restart
#as postgres
emacs /var/lib/pgsql/9.3/data/pg_hba.conf
emacs /var/lib/pgsql/9.3/data/postgresql.conf
port = 5432
listen_addresses = '*'
max_connections = 100


#user
adduser -m devuser
groupadd devuser
adduser -m -g devuser devuser
usermod -a -G devuser leipzigj
usermod -a -G devuser apache
usermod -a -G devuser nginx

#sticky group SO IMPORTANT
chmod -R g+s /home/devuser

#nodejs
yum -y update  
yum -y install screen  
cd /usr/local/src  
wget http://nodejs.org/dist/node-latest.tar.gz  
tar zxf node-*.tar.gz  
cd node-v* 
yum -y groupinstall "Development Tools"  
./configure
make
make install  

#bryon's wicked template
virtualenv mybic-env
cd mybic-env/
. bin/activate
django-admin.py startproject --template https://github.com/bruth/wicked-django-template/zipball/master -e py,ini,gitignore,in,conf,md,sample,json -n Gruntfile.coffee mybic
PATH=$PATH:/usr/pgsql-9.3/bin/pg_config
#fix requirements
#django-siteauth
#django-registration2
pip install -r requirements.txt
#chopauth needs updating http://github.research.chop.edu/cbmi/django-chopauth/issues/6
#your node might be out of date
sudo npm install -g grunt-cli
sudo gem install compass
#this installs the grunt dependencies:
npm install
grunt



#uwsgi
sudo pip install uwsgi

#run wsgi through socket, needs nginx on
/home/devuser/webapps/mybic-env/bin/uwsgi --ini /home/devuser/webapps/mybic-env/mybic/server/uwsgi/development.ini  --uid devuser --gid devuser


#other
scp leipzig@eps1.infosys.chop.edu:/Users/leipzig/Downloads/themeforest-5961888-avant-clean-and-responsive-bootstrap-31-admin.zip .
unzip themeforest-5961888-avant-clean-and-responsive-bootstrap-31-admin.zip
```
