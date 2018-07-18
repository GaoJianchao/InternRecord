#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/29 17:56
# @Author  : zql
# @Site    : 
# @File    : process_singer_song.py
# @Software: PyCharm
chn_min = ord(u'\u4E00')
chn_max = ord(u'\u9FA5')
def allEnglishLetters(name):
    for ch in name:
        if chn_min <= ord(ch) <= chn_max:
            return False
    return True
def process_space(name):
    return name.split(u' ')[0]
def one_step():
    f = open('singer.song.txt', 'w')
    cur = cur_up = pre = pre_up = next = next_up = ''
    song_singer_set = set()
    for line in open('singer_song.txt'):
        arrs = [process_space(s.decode('utf-8')) for s in line.strip().split('\t')]
        if len(arrs) < 2:
            continue
        if allEnglishLetters(arrs[0]):
            continue
        for name in arrs[1].split(u'|'):
            if name.strip() == '':
                continue
            if pre == '':
                pre = name
                pre_up = arrs[0]
                str_line = pre_up.encode('utf-8') + '\t' + pre.encode('utf-8')
                if str_line not in song_singer_set:
                    song_singer_set.add(str_line)
                    f.write(str_line + '\n')
                continue
            if next == '':
                next = name
                next_up = arrs[0]
                # f.write(arrs[0].encode('utf-8') + '\t' + pre.encode('utf-8') + '\n')
                continue
            cur = next
            cur_up = next_up
            next = name
            next_up = arrs[0]
            if cur == pre or cur == next:
                str_line = cur_up.encode('utf-8') + '\t' + cur.encode('utf-8')
                if str_line not in song_singer_set:
                    song_singer_set.add(str_line)
                    f.write(str_line + '\n')
    str_line = cur_up.encode('utf-8') + '\t' + cur.encode('utf-8')
    if str_line not in song_singer_set:
        song_singer_set.add(str_line)
        f.write(str_line + '\n')
    f.close()
def two_step():
    rank = 1
    score = 10
    pre = cur = ''
    fs = open('rank.value.txt', 'w')
    with open('singer.song.txt') as f:
        lines = f.readlines()
        for line in lines:
            arrs = line.strip().split('\t')
            if pre == '':
                pre = arrs[1]
                fs.write(line.strip() + '\t' + str(score) + '\n')#+ '\t' + str(rank)
                rank += 1
                score = max(score - 1, 1)
                continue
            cur = arrs[1]
            if cur == pre:
                fs.write(line.strip() + '\t' + str(score) + '\n')  # + '\t' + str(rank)
                pre = cur
                rank += 1
                score = max(score-1, 1)
            else:
                pre = cur
                rank = 1
                score = 10
                fs.write(line.strip() + '\t' + str(score) + '\n')  # + '\t' + str(rank)
                rank += 1
                score = max(score - 1, 1)
    f.close()
    fs.close()

if __name__ == '__main__':
    one_step()
    two_step()