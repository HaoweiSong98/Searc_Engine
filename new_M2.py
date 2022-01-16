import json
import time
from urllib.parse import urlparse
from tkinter import *

def stop_word():
    return ['', 'in', 'under', 'few', 'the', 'against', 'up', 'if', 'itself', 'have', "she's", 'her',
                  'your', 'but', 'into', 'was', "when's", 'about', 'how', 'same', "hasn't", 'all', 'than',
                  'there', 'should', 'for', "here's", 'these', "we've", "mustn't", "it's", "where's", 'at',
                  'whom', 'where', 'this', 'after', 'being', "hadn't", 'below', "didn't", 'during', 'only',
                  'am', 'had', "i'm", "shouldn't", 'on', 'such', 'those', 'which', 'then', 'so', "you'll",
                  "i'll", 'he', 'i', 'no', "aren't", "let's", 'why', 'cannot', 'to', 'because', 'myself',
                  "they'll", "we're", 'his', 'again', 'own', 'by', 'who', 'through', 'are', 'we', "we'll",
                  'before', 'yours', "you're", 'until', "she'll", 'more', 'further', "he's", 'could', "doesn't",
                  'himself', 'as', 'some', "you'd", "he'll", 'does', "couldn't", 'that', "they're", 'him', 'and',
                  'over', "don't", "that's", 'yourselves', 'ours\tourselves', 'were', 'when', 'hers', 'their',
                  'did', "she'd", 'its', "can't", 'theirs', 'between', 'doing', 'with', 'she', "i've", 'having',
                  'our', "we'd", 'been', 'from', 'a', "he'd", "wouldn't", "there's", 'while', "they'd", 'ought',
                  'would', "shan't", 'other', 'me', 'it', 'you', "they've", 'an', 'once', 'do', 'be', 'or', 'they',
                  "i'd", "haven't", 'any', 'too', "isn't", 'each', 'themselves', 'very', 'herself', 'what',
                  'yourself', "you've", 'here', "weren't", 'off', 'them', "why's", "wasn't", "what's", 'not',
                  'both', 'above', 'of', "won't", 'my', 'nor', 'is', 'out', 'down', 'has', "how's", "who's", 'most',
                  'will', 'may', 'can', 'ph', '2014', 'edu', 'says', 'one', '2014', 'news', 'new']




def get_user_word(user_input, m1_dict):
    BIG = open('final_BIG_file.json', 'r')

    words = user_input.lower()
    time_start = time.time()
    word_list = []
    for k in words.split():
        if k not in stop_word():
            word_list.append(k)
    # a b c   url in a and b and c
    result_url = dict()

    for word in word_list:
        if word_list.index(word) == 0:
            if word in m1_dict:
                seek_number = m1_dict[word]
                BIG.seek(seek_number)

                index_list = json.loads(
                    BIG.readline())  # [[22773, [-101.31867889479845, 51618]], [33621, [-100.86520872228778, 49088]]]

            for url_po in index_list:  # [22773, [-101.31867889479845, 51618]]

                result_url[url_po[0]] = [url_po[1]]
        else:

            if word in m1_dict:
                seek_number = m1_dict[word]
                BIG.seek(seek_number)
                index_list = json.loads(BIG.readline())

            for url_po in index_list:
                if url_po[0] in result_url:
                    result_url[url_po[0]].append(url_po[1])

    for check in result_url.items():
        # this part is and   because check all words in same url
        if len(check[1]) < len(word_list):
            result_url[check[0]] = None

    result_dict = dict()
    # print(result_url)

    for item in result_url.items():  # {22773: [[-101.31867889479845, 51618]], 33621: [[-100.86520872228778, 49088]]}

        if item[1] != None:
            if len(item[1]) == 1:  # [[-21.349462695698147, 2986]]
                result_dict[item[0]] = item[1][0][0]
            else:
                score = 0
                for doc in item[1]:  # [[-39.3684664355303, 629], [-32.104321471913345, 631]]
                    score += doc[0]
                result_dict[item[0]] = score

    time_end = time.time()  # 开始计时
    time_c = time_end - time_start  # 运行所花时间
    t = "time cost: " + str(time_c) + 's\n'
    answer.insert(INSERT, t)

    return result_dict





def get_me():

    answer.delete(1.0, END)
    f = open('final_seek_index.json', 'r')
    m1_dict = json.load(f)
    f1 = open("Doc_id_final.json", 'r')
    doc_id = json.load(f1)
    #print("Welcome to my engine!!!!!!!!!")

    entry_value = entry.get()
    #get_state = input('If you want to quit, enter "exit()", or enter other word to search: ')

    try:

        urls = get_user_word(entry_value, m1_dict)
        results = [k[0] for k in sorted(urls.items(), key=lambda item: item[1], reverse=True)]

        total_result = []
        try:

            for i in range(len(results)):

                f = open(doc_id[str(results[i])], 'r')
                result = json.load(f)
                parsed_url = urlparse(result['url'])
                if (parsed_url.netloc + parsed_url.path) not in total_result:
                    total_result.append(parsed_url.netloc + parsed_url.path)
                if len(total_result) == 5:

                    for i in range(5):
                        j = ''
                        j += 'Rank'+ str(i+1)+ ': '  + total_result[i]+ '\n'
                        answer.insert(INSERT, j)

                    break
            if len(total_result) == 0:
                answer.insert(INSERT, 'Error: Cannot Found Word!')

            if len(total_result) < 5:
                for i in range(5):
                    j = ''
                    j += 'Rank' + str(i + 1) + ': ' + total_result[i] + '\n'
                    answer.insert(INSERT, j)



        except IndexError:
            pass

    except UnboundLocalError:
        answer.insert(INSERT, 'Error: Cannot Found Word!')
        #print('Error: Cannot Found Word!')

    #print("Thanks for using!!!")


    #answer.insert(INSERT, "rank 1: .....")











if __name__ == '__main__':
    root = Tk()
    root.title('Welcome to my search engine')

    topframe = Frame(root)
    entry = Entry(topframe)
    entry.pack()
    button = Button(topframe, text="search", command=get_me)
    button.pack()
    topframe.pack(side=TOP)

    bottomframe = Frame(root)
    scroll = Scrollbar(bottomframe)
    scroll.pack(side=RIGHT, fill=Y)
    answer = Text(bottomframe, width=100, height=30, yscrollcommand=scroll.set, wrap=WORD)
    scroll.config(command=answer.yview)
    answer.pack()
    bottomframe.pack()

    root.mainloop()
    #run()