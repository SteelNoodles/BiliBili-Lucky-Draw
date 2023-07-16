import os
from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()
# 读取变量
dbname = os.getenv("MYSQL_DATABASE")
user = os.getenv("MYSQL_USER")
passwd = os.getenv("MYSQL_PASSWORD")
root_passwd = os.getenv("MYSQL_ROOT_PASSWORD")
port = int(os.getenv("PORT"))
charset = 'utf8'
db_host = os.getenv("DB_HOST")
check_ok_draw_time = int(os.getenv("check_ok_draw_time"))
max_checks = int(os.getenv("max_checks"))
home_url = os.getenv("home_url")
selenium_url = os.getenv("selenium_url")
my_user_id = os.getenv("my_user_id")
delay_time = os.getenv("delay_time")
fns_list = os.getenv("FELLOW_USER_LIST").split(":")
outdated_time_days = int(os.getenv("outdated_time_days"))
unfollow = os.getenv("unfollow")



