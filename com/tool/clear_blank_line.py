# -*- coding: utf-8 -*-
__author__ = 'yanghai'


def main(infile, outfile):
    infp = open(infile, "r")
    outfp = open(outfile, "w")
    lines = infp.readlines()
    i = 0
    for li in lines:
        if li.split():
            outfp.writelines(li)
           # i = i + 1
           # 每页50行
           # if (i %50) == 0:
           #     outfp.writelines('\n')

    infp.close()
    outfp.close()


main('a.txt', 'b.txt')