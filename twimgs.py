import os
import random
import re
import threading
import time
import requests

from twqr import scan_qr_code
from config import rawQuery, headers, cookies

http = requests.Session()
http.cookies.update(cookies)
http.headers.update(headers)

# 搜索关键词是群
http.params = {
    "variables": "{\"rawQuery\":\""+rawQuery+"\",\"count\":40,\"cursor\":\"\",\"querySource\":\"typed_query\",\"product\":\"Latest\"}",
    "features": "{\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"c9s_tweet_anatomy_moderator_badge_enabled\":true,\"tweetypie_unmention_optimization_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":true,\"tweet_awards_web_tipping_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"rweb_video_timestamps_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_media_download_video_enabled\":true,\"responsive_web_enhance_cards_enabled\":false}"
}


def getNew():
    res = http.get("https://twitter.com/i/api/graphql/fZK7JipRHWtiZsTodhsTfQ/SearchTimeline").text
    jpg_list = re.findall("https://pbs.twimg.com/media/[0-9a-zA-Z_-]{15}\.jpg", res)
    png_list = re.findall("https://pbs.twimg.com/media/[0-9a-zA-Z_-]{15}\.png", res)
    pic_list = jpg_list+png_list
    return pic_list


def nn(img):
    fileName = "./imgs/" + img.split("/")[-1]
    fileName2 = "./wximg/" + img.split("/")[-1]
    fileName2 = "./otherimg/" + img.split("/")[-1]
    fileBody = requests.get(img).content
    open(fileName, "wb").write(fileBody)
    time.sleep(1)
    scanRes = scan_qr_code(fileName)
    print(fileName, scanRes)
    if "weixin.qq.com" in scanRes:
        open(fileName2, "wb").write(fileBody)
    elif scanRes != "":
        open(fileName2, "wb").write(fileBody)


fileName = "./img.txt"
if not os.path.exists(fileName):
    open(fileName, "w").write("")


def mm():
    pic_list = getNew()
    # print(pic_list)

    for i in pic_list:
        if i not in open(fileName).read():
            open(fileName, "a").write(i + "\n")
            threading.Thread(target=nn, args=(i,)).start()
            time.sleep(0.1)


while 1:
    threading.Thread(target=mm).start()
    time.sleep(random.randint(60, 180))
