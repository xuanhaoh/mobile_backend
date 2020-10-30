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
| /user/add | POST | username, longitude, latitude | "Success", "200" <br> "Duplicate username", "400" <br> "Username, longitude and latitude required", "400" |
| /user/query | GET | | [{username, longitude, latitude, creation_date}], "200" |
| /record/add | POST | username, grade, longitude, latitude | "Success", "200" <br> "Username and grade required", "400"|
| /record/query | GET | | [{username, grade, creation_date}], "200" |