import re
from urllib.parse import urlparse

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]



def is_valid(url):
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]):
                return False
            else:
                if not re.match(r".*\.(css|js|bmp|gif|jpe?g|ico"+ r"|png|tiff?|mid|mp2|mp3|mp4"+ r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"+ r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"+ r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"+ r"|epub|dll|cnf|tgz|sha1"+ r"|thmx|mso|arff|rtf|jar|csv"+ r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", str(url)) and re.match(r".+\.ics\.uci\.edu\/.*"r"|.+\.informatics\.uci\.edu\/.*"r"|.+\.stat\.uci\.edu\/.*"r"|.+\.cs\.uci\.edu\/.*"r"|today\.uci\.edu/department/information_computer_sciences\/.*",str(url)):
                    return True

        except TypeError:
            print("TypeError for ", parsed)
            raise

def extract_next_links(url, resp):
    #url = 'https://evoke.ics.uci.edu/evoke-members-western-humanities-alliance-2013/#comment-48628'
    #防止这种重复的出现url = 'https://evoke.ics.uci.edu/evoke-members-western-humanities-alliance-2013/#comment-5555'
    parsed_url = urlparse(url)
    check_list = []
    check_list.append(parsed_url.netloc + parsed_url.path)
    page_soup = BeautifulSoup(resp, 'lxml')
    info_titles = page_soup.find_all("a")
    result_list = []
    
    for l in info_titles:
        try:
            parsed = urlparse(l['href'])
            new_link = parsed.netloc + parsed.path
            if new_link not in check_list:
                check_list.append(new_link)
                result_list.append(l['href'])
        except:
            pass
    return result_list