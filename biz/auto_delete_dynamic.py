#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :auto_delete_dynamic.py
# @time   :2023/7/14 15:02
# @Author : CHT1HTSH3212
# @Version:1.0
# @Desc   :
import datetime
from time import sleep
from loguru import logger

from biz.login_by_cookie import login_by_cookie
from globals import my_user_id, home_url, outdated_time_days, unfollow
from selenium.webdriver.common.by import By

from utils.selenium_util import init_webdriver


def delete_outdated_dynamic():
    """
    扫描并删除已过期的抽奖动态
    """
    bro, chains = init_webdriver()
    cookie_path = './cookie/' + my_user_id + '.txt'
    bro.get(home_url)
    login_by_cookie(bro, cookie_path)

    url = 'https://space.bilibili.com/' + my_user_id + '/dynamic'
    logger.info(url)
    bro.get(url)
    sleep(2)

    for i in range(30):
        # 4.滚动条操作
        # 4.1 滚动条向下滚动
        js_down = "window.scrollBy(0,10000)"
        # 执行向下滚动操作
        bro.execute_script(js_down)
        sleep(2)

    try:
        share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')

        index = 1
        dynamic_id_list = []
        index_list = []

        for dynamic in share_list:
            try:
                # 获取动态转发时间
                time = dynamic.find_element(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' +
                                                  str(index) + ']/div/div/div[2]/div[2]/div').text

                if check_dynamic_time(time):

                    # time = dynamic.find_element(By.XPATH, './div[2]/div[2]').text
                    dynamic_id = dynamic.find_element(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' +
                                                        str(index) + ']/div/div/div[3]/div/div[2]/div[3]/div').\
                                                        get_attribute("dyn-id")

                    if dynamic_id:
                        logger.info(dynamic_id)
                        dynamic_id_list.append(dynamic_id)
                        index_list.append(index)
                index += 1

            except Exception as e:
                logger.info("删除动态失败: {}".format(e))
                continue

        for i in index_list[::-1]:
            do_dynamic_delete(bro, chains, i)

        for id in dynamic_id_list[::-1]:
            unfollow_by_dynamic_id(bro, chains, id)

    except Exception as e:
        logger.info("删除动态失败: {}".format(e))


def check_dynamic_time(release_time):
    """
    判断转发动态是否过期，如果是返回True, 否则返回False
    """

    # 格式为xxxx年xx月xx日 xx:xx
    if "年" not in release_time:
        return False

    # TODO 转换发布时间为"%Y-%m-%d %H:%M"
    time_format = "%Y-%m-%d"
    release_time_str = release_time[:4] + '-' + release_time[5:7] + '-' + release_time[8:10] + release_time[11:]

    release_time = datetime.datetime.strptime(release_time_str, time_format)
    outdated_time = datetime.datetime.now()

    # TODO 动态超过设定期限，删除动态
    if release_time + datetime.timedelta(days=int(outdated_time_days)) < outdated_time:
        logger.info("过期")
        return True
    else:
        logger.info("未过期")
        return False

def unfollow_by_dynamic_id(bro, chains, dynamic_id):
    """
    取消关注
    :param bro:
    :param chains:
    :param dynamic_id:
    :return:
    """
    if unfollow == "false":
        return

    url = 'https://t.bilibili.com/' + dynamic_id
    bro.get(url)
    sleep(3)

    # 移动到头像
    touxiang = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div')
    sleep(3)
    chains.move_to_element(touxiang).perform()
    sleep(3)

    # 点击关注
    follow = bro.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div[1]')
    follow_text = follow.get_attribute('innerText')
    logger.info(follow_text)
    sleep(2)
    if "已关注" in follow_text:
        chains.click(follow).perform()
        logger.info(f"通过动态{dynamic_id}取关成功!")


def do_dynamic_delete(bro, chains, index):
    """
    delete dynamic
    :param bro:
    :param chains:
    :param index:
    :return:
    """

    try:
        # 找到三个点按钮
        dyn_more_btn = bro.find_element(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(index) +
                                        ']/div/div/div[2]/div[4]/div')
        sleep(2)
        chains.click(dyn_more_btn).perform()
        sleep(2)

        # 找到删除按钮
        delete_btn = bro.find_element(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(index) +
                                        ']/div/div/div[2]/div[4]/div/div/div[2]/div[2]')
        sleep(2)
        chains.click(delete_btn).perform()
        sleep(2)

        # 确认删除
        confirm_btn = bro.find_element_by_class_name("bili-modal__footer").find_elements(By.XPATH, '*')[0]
        sleep(2)
        chains.click(confirm_btn).perform()
        sleep(2)

        logger.info("删除动态成功")

    except Exception as e:
        logger.info(f"删除动态失败：{e}")
