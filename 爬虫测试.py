import requests
from lxml import html
import re
import csv
#url
# target_url="https://www.tiobe.com/tiobe-index/"
# #发送请求 获取数据
# response=requests.get(target_url)
#解析数据
# doc=html.fromstring(response.text)
# th_list=doc.xpath("//table[@id='top20']/thead/tr/th/text()")
#解析表格
# tr_list=doc.xpath("//table[@id='top20']/tbody/tr")
# for tr in tr_list:
# td_list=tr.xpath("./td/text()")
# print(td_list)
TMDB_BASE_URL='https://www.themoviedb.org'
TMDB_TOP_URL='https://www.themoviedb.org/movie/top-rated'


def get_movie_info(movie_info_url):
    #1.发送请求获取电影数据
    response=requests.get(movie_info_url)
    #2.解析数据获取详情
    document=html.fromstring(response.text)
    movie_names=document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    movie_year=document.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()")
    movie_release_date = document.xpath(
        "//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()"
    )
    movie_score=document.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    #3.返回数据--字典
    movie_info={"电影名":movie_names[0].strip() if movie_names else "","上榜年份":movie_year[0].strip() if movie_year else "","上映时间":movie_release_date[0].strip() if movie_release_date else "","评分":movie_score[0].strip() if movie_score else ""}
    return movie_info
#
def save_all_movies(all_movies):
    pass


def main():
    #1.发送请求
    response=requests.get(TMDB_TOP_URL,timeout=60)
    #2.解析数据
    document=html.fromstring(response.text)
    movies=document.xpath("//*[@id='page_1']/div/div/div[@class='w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-colors hover:border-gray-300']")
    all_movies=[]
    for movie in movies:
        movie_list=movie.xpath("./div/div/a/@href")
        if movie_list:
            movie_info_url=TMDB_BASE_URL+movie_list[0]
            #发送请求
            movie_info=get_movie_info(movie_info_url)
            all_movies.append(movie_info)
            # movie_response=requests.get(movie_info_url,timeout=60)
            # movie_doc=html.fromstring(movie_response.content)
            # movie_info=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p")
    save_all_movies(all_movies)
#3.遍历电影列表 获取电影详情
#4.保存数据为csv文件
if __name__=='__main__':
    main()