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
| /init | GET | | Message |
| /add/random_data | GET | | Message |
| /add/user | POST | username, longitude, latitude | Message |
| /add/record | POST | username, grade | Message |
| /update/user | POST | username, longitude, latitude | Message |
| /query/nearby_record | POST | longitude, latitude, distance | [{username, longitude, latitude, grade}] |
| /query/leaderboard | GET | | [{username, grade, creation_date}] |