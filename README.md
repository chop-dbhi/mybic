##myBiC - Bioinformatics Core Portal

###[Documentation and Examples](../../wiki)

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

#solr
The fabfile or a puppet script (or docker what have you) will do this,
but here is what needs to be done if the app is deployed in the usual way:

# install Oracle Java 7 and make available via link /usr/java/java7 (Note: when containerizing, will switch to OpenJDK)
# Surf to relevant link at http://www.java.com/en/download/manual.jsp and download Linux x64 (non-RPM)
curl -L http://javadl.sun.com/webapps/download/AutoDL?BundleId=90216 > jre-7u60-linux-x64.tar.gz
sudo mkdir -p /usr/java
cd /usr/java
sudo tar xzvf ~/jre-7u60-linux-x64.tar.gz
sudo ln -s /usr/java/jre1.7.0_60 /usr/java/java7

# Make /opt/solr
sudo mkdir -p /opt/solr

# download Solr 4.8.x
curl -O -L http://mirror.symnds.com/software/Apache/lucene/solr/4.8.1/solr-4.8.1.tgz
tar xzvf solr-4.8.1.tgz
sudo wget http://supergsego.com/apache/lucene/solr/4.10.3/solr-4.10.3.tgz
sudo gunzip solr-4.10.3.tgz 
sudo tar -xvf solr-4.10.3.tar 
sudo cp solr-4.10.3 /opt/

# Customize this directory with our own schema.xml and logging.properties - best to make these links into /home/devuser/webapps/pcgc-env/pcgc/server/solr/*
/home/devuser/webapps/mybic-dev-env/mybic-dev//bin/manage.py build_solr_schema > /home/devuser/webapps/mybic-dev-env/mybic-dev/server/solr/schema.xml
sudo ln -sf /home/devuser/webapps/mybic-dev-env/mybic-dev/server/solr/schema.xml /opt/solr/solr/collection1/conf/schema.xml

# this config has set <unlockOnStartup>true</unlockOnStartup>
sudo ln -sf /home/devuser/webapps/mybic-dev-env/mybic-dev/server/solr/solrconfig.xml /opt/solr-4.10.3/example/solr/collection1/solrconfig.xml

# create solr user:
sudo /usr/sbin/useradd -d /opt/solr -s /sbin/nologin solr

# Add solr user to devuser group:
sudo /usr/sbin/usermod -a -G devuser solr

# make /opt/solr tree owned by solr
sudo chown -RH solr:devuser /opt/solr

#Solr 4.8.x requires Java 1.7.  As mentioned, when we Dockerize this, for convenience, we probably want to switch to OpenJDK.
sudo supervisorctl update
sudo supervisorctl start solr-development
/home/devuser/webapps/mybic-dev-env/mybic-dev//bin/manage.py rebuild_index

#other
scp leipzig@eps1.infosys.chop.edu:/Users/leipzig/Downloads/themeforest-5961888-avant-clean-and-responsive-bootstrap-31-admin.zip .
unzip themeforest-5961888-avant-clean-and-responsive-bootstrap-31-admin.zip
```
