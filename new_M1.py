import os
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import sys
import math

def get_filelist(dir):
    doct_id = 1
    filelist = []
    newDir = dir
    result_dict = dict()
    for s in os.listdir(dir):
        newDir=os.path.join(dir,s)
        filelist.append(newDir)
    for j in filelist:
        if os.path.isdir(j):
            for i in os.listdir(j):
                result_dict[doct_id] = (os.path.join(j,i))
                doct_id += 1
    json_result = json.dumps(result_dict)
    result_json = open('Doc_id_final.json', 'w')
    result_json.write(json_result)
    result_json.close()
    return result_dict

def tokenize(word_str):
    words_dict = dict()
    check_place = 0
    doc_word_num = len(re.split(r'[^a-zA-Z0-9]', word_str.lower()))
    for split_w in re.split(r'[^a-zA-Z0-9]', word_str.lower()):# O(N)
        check_place += 1
        if split_w != '':
            if split_w not in words_dict:
                words_dict[split_w] = [doc_word_num, check_place]# netest list, list[0] is the number of the words, list[1] is a list that contains all of this word's position in the content
            else:
                words_dict[split_w].append(check_place)

    return words_dict


def write_partialIndex(my_result, filename):


    sorted_list = [[k, v] for k, v in sorted(my_result.items())]
    result_json = open(filename,'w+')

    for i in sorted_list:
        json_result = json.dumps(i) + "\n"

        result_json.write(json_result)

    result_json.close()


def deal_Word(plist):


    dicts = defaultdict(list)
    for i in plist:
        if i != '':
            l = eval(i)
            dicts[l[0]]+= l[1]


    order_list = [[k, v] for k, v in sorted(dicts.items())]
    read_index = []
    for j in range(len(plist)):
        if plist[j] != '' and eval(plist[j])[0] == order_list[0][0]:
            read_index.append(j)


    return [order_list[0], read_index]


def merge_index():

    p1 = open('final_json_newM1_part1.json', 'r')
    p2 = open('final_json_newM1_part2.json', 'r')
    p3 = open('final_json_newM1_part3.json', 'r')

    Big_file = open('final_BIG_file.json', 'w')

    p1_line = p1.readline()
    p2_line = p2.readline()
    p3_line = p3.readline()

    seek_dict = dict()
    seek_index = open('final_seek_index.json', 'w')

    #remove empty


    infront = 0
    while p1_line!= '' and p2_line != '' and p3_line != '':

         combine_list = [p1_line, p2_line, p3_line]

         indexs = deal_Word(combine_list)
         for position_list in indexs[0][1]:
             position_list[1][0] = (1 + math.log((len(position_list[1]) - 1) / position_list[1][0])) * math.log(55393 / len(indexs[0][1]))  # tf-idf


         to_big =  str(indexs[0][1]) + '\n'

         Big_file.write(to_big)

         string = indexs[0][0]
         index = infront
         infront += len(to_big)
         seek_dict[string] = index


         if 0 in indexs[1]:
             p1_line = p1.readline()
         if 1 in indexs[1]:
             p2_line = p2.readline()
         if 2 in indexs[1]:
             p3_line = p3.readline()

    seek_result = json.dumps(seek_dict)
    seek_index.write(seek_result)
    seek_index.close()


if __name__ == "__main__":
    get_all_json = get_filelist('DEV')
    print(len(get_all_json))
    my_result = dict()
    check = 0
    for json_name in get_all_json.items():
        check += 1
        print(check)
        f = open(json_name[1],'r')
        result = json.load(f)
        soup = BeautifulSoup(result["content"], 'html.parser')
        total_tokens = tokenize(soup.get_text())
        for word_dict in total_tokens.items():
            if word_dict[0] not in my_result:

                my_result[word_dict[0]] = [ [json_name[0],word_dict[1]]]
            else:

                my_result[word_dict[0]].append([json_name[0],word_dict[1]])

        if check == 19000:
            write_partialIndex(my_result, 'final_json_newM1_part1.json')
            my_result.clear()

        elif check == 28000:
            write_partialIndex(my_result, 'final_json_newM1_part2.json')
            my_result.clear()




    write_partialIndex(my_result, 'final_json_newM1_part3.json')
    my_result.clear()
    merge_index()