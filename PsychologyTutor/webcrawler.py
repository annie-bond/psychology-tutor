import requests
from bs4 import BeautifulSoup

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # extract paragraphs
    paragraphs = soup.find_all("p")
    text = "\n".join([p.get_text() for p in paragraphs])
    return text

def crawl():
    target_url = "https://psychologyalevel.com/aqa-psychology-revision-notes/"
    max_crawl = 50
    urls_to_visit = [target_url]
    webpages_text_string = ""
    crawl_count = 0

    while urls_to_visit and crawl_count < max_crawl:
        # get the current page to visit from the list:
        current_url = urls_to_visit.pop()

        # request the target url:
        response = requests.get(current_url)
        response.raise_for_status()
        # parse html:
        soup = BeautifulSoup(response.text, "html.parser")

        # get all the links:
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element["href"]

            # convert relative urls to absolute:
            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(target_url, url)
            else:
                absolute_url = url

            # make sure crawled url belongs to the target website, hasn't been visited, and isn't a jump link:
            if (
                absolute_url.startswith(target_url)
                and absolute_url not in urls_to_visit
                and not absolute_url.__contains__("#")
            ):
                urls_to_visit.append(absolute_url)
                webpage_text = scrape(absolute_url)

                # filter out lines of text preceding images:
                filtered_lines = [line for line in webpage_text.splitlines() if not line.rstrip().endswith(":")]
                webpage_text = "\n".join(filtered_lines)
                webpages_text_string = webpages_text_string + " " + webpage_text

            crawl_count += 1

    print(webpages_text_string)
    print(urls_to_visit)
    return webpages_text_string