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
MOVIE_LIST_FILE='csv_data/movie_list.csv'
TMDB_BASE_URL='https://www.themoviedb.org'
TMDB_TOP_URL='https://www.themoviedb.org/movie/top-rated'
TMDB_FULL_URL='https://www.themoviedb.org/discover/movie/items'


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
    print(movie_info)
    return movie_info

def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE,'w',encoding='utf-8',newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["电影名","上榜年份","上映时间","评分"])
        writer.writeheader()
        writer.writerows(all_movies)


def main():
    all_movies = []
    for page_num in range(1,6):
        # 1.发送请求
        if page_num==1:
            response = requests.get(TMDB_TOP_URL, timeout=60)
        else:
            response = requests.post(TMDB_FULL_URL,data=f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-30&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated", timeout=60)

        # 2.解析数据
        document = html.fromstring(response.text)
        movies = document.xpath(
            f"//*[@id='page_{page_num}']/div/div/div[@class='w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-colors hover:border-gray-300']")

        for movie in movies:
            movie_list = movie.xpath("./div/div/a/@href")
            if movie_list:
                movie_info_url = TMDB_BASE_URL + movie_list[0]
                # 发送请求
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)
    save_all_movies(all_movies)
#3.遍历电影列表 获取电影详情
#4.保存数据为csv文件
if __name__=='__main__':
    main()