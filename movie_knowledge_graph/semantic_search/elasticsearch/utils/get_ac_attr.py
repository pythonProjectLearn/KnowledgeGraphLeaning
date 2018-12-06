#!/usr/bin/env python
# coding=utf-8
"""
属性同义词扩展
为了支持对同一类问题的不同询问方式，我们采用同意属性映射来扩展属性，当遇到同义属性时，我们将其映射到数据集中的属性

ahocorasick实现快速的关键字匹配
"""
import ahocorasick
import pickle
from collections import defaultdict


def dump_ac_attr_dict(attr_mapping_file='../data/attr_mapping.txt', out_path='../data/attr_ac.pkl'):
    A = ahocorasick.Automaton()
    f = open(attr_mapping_file)
    i = 0    
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != "": 
                A.add_word(p,(i,p))
                i += 1
    A.make_automaton()
    pickle.dump(A,open(out_path,'wb'))

if __name__ == '__main__':
    dump_ac_attr_dict()
