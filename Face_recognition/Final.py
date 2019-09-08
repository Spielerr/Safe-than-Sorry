# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:18:42 2019

@author: manum
"""

import FraudDetection as fd
def isFace():
    TransactionAccountNo=int(input())
    FilePath="f3.xlsx"
    if fd.Fraud(TransactionAccountNo,FilePath):
        return True
    return False
    
print(isFace())   