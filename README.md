# sample-django-app-project [![Build Status](https://travis-ci.org/prince-tanapong/sample-django-app-project.svg?branch=master)](https://travis-ci.org/prince-tanapong/sample-django-app-project)

## Docker
1. How to install docker
  - go to this page `https://docs.docker.com/docker-for-mac/` and Follow first step

2. How to run develop environment
  - `docker-compose up --build`

3. How to stop develop environment
  - `docker-compose stop`

4. How to shell to develop environment
  - `docker-compose exec web bash`

5. How to run test
  - `docker-compose exec web python manage.py test`

6. Install new pagkage in requirement.txt have to build docker again(ps. It like a vagrant destroy and vagrant up again, all data gone)
  - `docker-compose down && docker-compose up --build`

7. Check test coverage
  - shell to docker `docker-compose exec web bash`
  - run test coverage `coverage run manage.py test`
  - see report `coverage report`
  - Ps you can run on your host sever for example `docker-compose exec web coverage run manage.py test`
