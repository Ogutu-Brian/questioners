# Questioner

## Prerequisites

## 1. PostgreSQL
```
PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance. 
```

### Installing Postgres
  - ### For Mac

    [Postgres App](http://www.postgresapp.com/)

  - ### For Linux
  
    - For APT systems (Ubuntu, Debian, Mint, Etc)
      ```
      sudo apt-get install postgresql
      ```
  - ### For Arch Linux
      ```
      sudo pacman -S postgresql
      ```

  - ### For YUM installations (Fedora / Red Hat / CentOS / Scientific Linux)

    (Example used is for PostgreSQL 9.2 on CentOS 6.4 x64)

    - Head over to [PostgreSQL Yum Repository](http://yum.postgresql.org/)
    - Select the version of PostgreSQL that you want to install and then your OS, version and architecture.
    - Download the RPM for your platform (using the link from step 2)
      ```
      curl -O http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-6.noarch.rpm
      ```

    - Install the RPM
      ```
      rpm -ivh pgdg-centos92-9.2-6.noarch.rpm
      ```

    - Do a quick search which will show you available packages for postgres
      ```
      yum list postgres*
      ```

      Note: It will probably list older versions as well, make sure to select proper version that you want to install and all the packages are of same version i.e server, client, contrib 

    - Install Packages as per choice
      ```
      yum install postgresql92-server.x86_64 postgresql92-contrib.x86_64 postgresql92-devel.x86_64
      ```
  - ### For Windows

    [Windows Installer](http://www.enterprisedb.com/products-services-training/pgdownload#windows)



## Initial Auth Endpoints
 - User Signup
 ```
  /api/auth/signup/
 ```
 - User Login
 ```
  /api/auth/login/
 ```
 - User Logout
  ```
   /api/auth/logout/
 ```
 - User Account Activation
  ```
   api/auth/activate/
 ```
 - User Account Activation Resend Email
  ```
   /api/auth/resend/
 ```
 - User Password Reset Eamil
  ```
   /api/auth/reset_password/
 ```
 - User Password Confirmation
  ```
   /api/auth/reset_password_confirm/
 ```
 - User Set Password
  ```
   /api/auth/change_password/
 ```
 - User Set Email
  ```
   /api/auth/change_email/
 ```

## Initial Others Endpoints
 - Api Docs
 ```
  /api/
 ```
 - Api Schema
 ```
  /api/schema/
 ```
 
## Local Development Setup
 - First Create python virtual env
 ```
  $ virtualenv -p python .venv
 ```
 - Install Requirements
 ```
  $ pip install -r api/requiremts.txt
 ```
 - Copy .env-example to .env and set config
 ```
  $ copy .env-example .env
 ```
 - Copy .env-example to .env and set config-In Ubuntu and Kali linux
 ```
  $ cp .env-example .env
 ```
 
 - Create postgres database
 ```
  $ sudo su postgres
  $ psql
  postgres=# CREATE USER django WITH PASSWORD 'password';
  postgres=# ALTER ROLE django SET client_encoding TO 'utf8';
  postgres=# ALTER ROLE django SET default_transaction_isolation TO 'read committed';
  postgres=# ALTER ROLE django SET timezone TO 'UTC';
  postgres=# CREATE DATABASE drf;
  postgres=# GRANT ALL PRIVILEGES ON DATABASE drf TO django;
  postgres=# \q
  $ exit
 ```
 - Run Server
 ```
  $ python api/manage.py runserver
 ```