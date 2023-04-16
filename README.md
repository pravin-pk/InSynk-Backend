# InSynk Back-end

InSynk is an all-in-one event management platform that empowers you to create, manage, and host events seamlessly. Whether it's an in-person or virtual event, InSynk has got you covered. With its powerful video streaming feature, you can easily stream your sessions live and engage with your attendees in real-time.

This repository serves as a backend for fetching API, live streaming, certificate generation and cloud connection

## Tech Stack
<p align="left"> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> &nbsp Django <br>
<a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>&nbsp Docker <br>
<a href="https://firebase.google.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/firebase/firebase-icon.svg" alt="firebase" width="40" height="40"/> </a> &nbsp Firebase<br> 
<a href="https://cloud.google.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" alt="gcp" width="40" height="40"/> </a> &nbsp GCP <br> <br>
Agora API

## Installation Steps

```Python
pip install -r requirements.txt
```
## Libraries and Dependencies
Provided in requirements.txt

## Usage

```bash
python manage.py runserver
```
To deploy in GCP, please use the following 
* note: Provided google console CLI is present in the system
```bash
gcloud config set project insynk-hackverse
gcloud run deploy
```
* Follow the instructions as prompted
