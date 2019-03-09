# Questioner

[![Coverage Status](https://coveralls.io/repos/github/Ogutu-Brian/questioners/badge.svg?branch=develop)](https://coveralls.io/github/Ogutu-Brian/questioners?branch=develop)
[![Build Status](https://travis-ci.org/Ogutu-Brian/questioners.svg?branch=develop)](https://travis-ci.org/Ogutu-Brian/questioners)
[![Maintainability](https://api.codeclimate.com/v1/badges/4d16bef0be1da640c69d/maintainability)](https://codeclimate.com/github/Ogutu-Brian/questioners/maintainability)
## Prerequisites

- PostgreSQL



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
  $ pip install -r requirements.txt
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
