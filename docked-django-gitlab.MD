Certainly! Here's an example of a script that automates the deployment of a Django application using Docker and GitLab CI/CD. This script assumes you have Docker and GitLab CI/CD set up and configured for your project:

```yaml
# .gitlab-ci.yml

stages:
  - build
  - test
  - deploy

# Build stage
build:
  stage: build
  image: python:3.9

  before_script:
    - pip install -U pip

  script:
    - pip install -r requirements.txt
    - docker build -t my_django_app .

# Test stage
test:
  stage: test
  image: python:3.9

  script:
    - pip install -r requirements.txt
    - python manage.py test

# Deployment stage
deploy:
  stage: deploy
  image: docker:latest

  services:
    - docker:dind

  variables:
    DOCKER_HOST: tcp://docker:2375

  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

  script:
    - docker pull $CI_REGISTRY_IMAGE:latest || true
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
    - docker stop my_django_app || true
    - docker run -d --rm --name my_django_app -p 8000:8000 $CI_REGISTRY_IMAGE:latest
```

In this example, the script is written in GitLab CI/CD configuration format (`gitlab-ci.yml`). It defines three stages: `build`, `test`, and `deploy`. The `build` stage sets up a Python environment, installs project dependencies, and builds a Docker image for the Django application. The `test` stage runs the Django tests to ensure code quality.

Finally, the `deploy` stage pulls the latest Docker image from the GitLab container registry, builds a new image based on the current commit, pushes it to the registry, and deploys the updated Docker container by stopping the previous container and running a new one.

Please note that this is a simplified example, and you would need to customize it according to your specific project's requirements, such as adding environment variables, database configurations, or additional steps.