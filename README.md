# neurolab-mongo-python

![image](https://user-images.githubusercontent.com/57321948/196933065-4b16c235-f3b9-4391-9cfe-4affcec87c35.png)

### Step 1 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 2 - Run main.py file

```bash
python main.py
```
This file is craeted by Rakesh on github
This line is on neurolab

## Git commands

## starting a project and use git
'''
git init
'''
Note: This is going to initalize git in your source code.

## You can clone exiting github repo
'''
git clone <github_url>
'''
Note: Clone/ Downlaod github repo in your system

## Add your changes made in file to git stagging are
'''
git add file_name
git add .
'''
Note: You can given file_name to add specific file or use "." to add everything to staging are

## Create commits
'''
git commit -m "message"
git push origin main
'''
Note: origin--> contains url to your github repo main--> is your branch name

## To push your changes forcefully.
'''
git push origin main -f
'''
## To pull changes from github repo
'''
git pull origin main
'''
origin--> contains url to your github repo 
main--> is your branch name

### .env file has

MONGO_DB_URL="mongodb://localhost:27017"
AWS_ACCESS_KEY_ID="aagswdiquyawvdiu"
AWS_SECRET_ACCESS_KEY="sadoiuabnswodihabosdbn"

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_ECR_LOGIN_URI=
ECR_REPOSITORY_NAME=
BUCKET_NAME=
MONGO_DB_URL=