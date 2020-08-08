import scrapy


link_list = []

class Crawler(scrapy.Spider) :
    name = "cz"
    start_urls = ["https://zingnews.vn/ra-mat-dich-vu-tikinow-giao-trong-ngay-ap-dung-hon-500000-san-pham-post1116204.html",]
    """ start_urls2 = ["https://zingnews.vn/",] """
    global link_list

    def parse(self, response):
        if response.status == 200 and response.css('meta[property="og:type"]::attr(content)').get() == "article":
            file = open("D:\PycharmProjects\Scrapy_Crawl_Websites\crawl\crawl\spiders\Output\Page_Info.txt", "a", encoding="utf-8")

        # print to file the link
            link = response.url
            file.write("link:  " + str(link) + "\n")
        # print to file the title
            title = response.css("h1.the-article-title::text").get()
            if title == "":
                title = response.css("h1.video-title a::attr(title)").get()
            file.write("title:  " + str(title) + "\n")
            yield {
                "title": response.css("h1.the-article-title::text").get()
            }
        # print to file the description
            des = response.css("p.the-article-summary::text").get()
            if des == "":
                des = response.css("p.video-summary::text").get()
            file.write("des:  " + str(des) + "\n")
            yield {
                "des": response.css("p.the-article-summary::text").get()
            }
        # print to file the published time
            published_time = response.css('meta[property="article:published_time"]::attr(content)').get()
            file.write("published_time:  " + str(published_time) + "\n")
        # print to file the tags
            tags = response.css('meta[property="article:tag"]::attr(content)').getall()
            file.write("tags:  ")
            for i in range(0, len(tags)):
                file.write(str(tags[i]) + " - ")
            file.write("\n")

        """ Spreading method 1
            Uses start_urls[] """
        next_page_lst = response.css("div.article-list.listing-layout.responsive a::attr(href)").getall()
        for next_page in next_page_lst:
            if next_page not in link_list and next_page is not None:
                link_list.append(next_page)
                yield response.follow(next_page, callback=self.parse)
            else:
                continue

        """ Spreading method 2. Uses start_urls2[] """
        #yield from response.follow_all(css = 'a[href^="https://zingnews.vn"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)


