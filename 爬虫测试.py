import requests
from lxml import html
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
def main():
    #1.发送请求
    response=requests.get(TMDB_TOP_URL,timeout=60)
    #2.解析数据
    document=html.fromstring(response.text)
    movies=document.xpath("//[@id='page_1']/div/div/div[@class='w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-colors hover:border-gray-300']")
    for movie in movies:
        movie_list=movie.xpath("./div/div/a/@href")
        if movie_list:
            movie_info_url=TMDB_BASE_URL+movie_list[0]
            mov_response=requests.get(movie_info_url,timeout=60)
            movie_doc=html.fromstring(mov_response.content)
            movie_info=movie_doc.xpath("//[@id='original_header']/div[2]/section/div[3]/div/p")
            print(movie_info)
#3.遍历电影列表 获取电影详情
#4.保存数据为csv文件
if __name__=='__main__':
    main()