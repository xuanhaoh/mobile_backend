# mobile_backend
## Installation
The project requires docker to run.

Get the project from version control.
```bash
git clone https://github.com/xuanhaoh/mobile_backend.git
cd mobile_backend
```
Run flask by mobile.sh
```bash
sudo sh mobile.sh
```
## HTTP API
| URL | method | parameter | return |
| :----: | :----: | :----: | :----: |
| /user/add | POST | username, password | "Success", "200" <br> "Duplicate username", "400" <br> "Username and password required", "400" |
| /user/query | GET | | [{user_id, username, password, creation_date}], "200" |
| /user/login | POST | username, password | "Success", "200" <br> "Incorrect username or password", "400"|
| /record/add | POST | username, grade, longitude, latitude | "Success", "200" <br> "Username, grade and position required", "400"|
| /record/query | GET | | [{grade_id, username, longitude, latitude, creation_date}], "200" |