#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :delete_outdata_dynamic.py
# @time   :2023/7/14 14:47
# @Author : CHT1HTSH3212
# @Version:1.0
# @Desc   :
import time
import schedule
from loguru import logger
from globals import delay_time
from biz.login_by_cookie import delay_start, check_cookie_valid
from biz.auto_delete_dynamic import delete_outdated_dynamic

if __name__ == "__main__":
    # delay_start(int(delay_time))
    login_valid = check_cookie_valid()
    if not login_valid:
        logger.error("超时未登录，程序退出！")
    logger.info("删除过期的动态开始运行...")
    delete_outdated_dynamic()
    schedule.every().day.at("15:42").do(delete_outdated_dynamic)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            logger.info("执行删除过期动态失败")


