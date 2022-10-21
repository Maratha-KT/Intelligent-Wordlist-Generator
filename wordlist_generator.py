# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 09:14:47 2022

@author: RShinde
"""
#!/bin/
import configparser

config = configparser.RawConfigParser()
config.read_file(open("Config.ini"))

'''
    Remove variable values from Config.ini file if you don't know its value or do not want a wordlist to be created
'''

nums = config.get("DEFAULT","NUMS")
nums = nums.split(",")
spl_chars = config.get("DEFAULT","SPECIAL_CHARS")
spl_chars = spl_chars.split(",")
password_min_length = int(config.get("DEFAULT","PASSWORD_MIN_LENGTH"))
password_max_length = int(config.get("DEFAULT","PASSWORD_MAX_LENGTH"))


first_name = config.get("Names","FIRST_NAME")
middle_name = config.get("Names","MIDDLE_NAME")
last_name = config.get("Names","LAST_NAME")
father_name = config.get("Names","FATHER_NAME")
mother_name = config.get("Names","MOTHER_NAME")
pet_name = config.get("Names","PET_NAME")

birth_year = config.get("Dates","BIRTH_YEAR")
birth_month = config.get("Dates","BIRTH_MONTH")
birth_day = config.get("Dates","BIRTH_DAY")
birth_eve = config.get("Dates","BIRTH_EVE")


#function which will help in paternizing strings
def patternizing_strings(base_word="MaTheW"):
    p = "" #initializing string for concatinated numbers
    for n in nums:
        wordlist.add(base_word + n) #Mathew1...0
        p = p + n
        wordlist.add(base_word + p) #Mathew123
        q = ""
        for s in spl_chars:
            wordlist.add(base_word + s) #Mathew!...)
            q = q + s
            wordlist.add(base_word + q) #Mathew!@#
            wordlist.add(base_word + p + q) #Mathew123!@#
    #reintializing the sequence for reverse password
    q = "" #initializing string for concatinated special characters
    for s in spl_chars:
        q = q + s
        p = ""
        for n in nums:
            p = p + n
            wordlist.add(Name + q + p)

#Initializing a password set where indentified patterns can be stored and unique ones will be eliminated during addition itself
wordlist = set()
'''
    Patterns would be created based on sequenced special chars <-followed by-> numberes and vice versa
    No swapping of special characters will be done for concatination as it involves more 
'''
name_arr = [first_name,middle_name,last_name,father_name,mother_name,pet_name]
for name in name_arr: #Assume name is MaTheW
    if name == "":
        continue                #Checking if the value is not null for wordlist creation
    Name = name.capitalize()
    wordlist.add(Name) #Mathew
    patternizing_strings(base_word=Name)
    
with open("custom_wordlist.txt","w") as writer:
    wordlist = list(wordlist)
    wordlist.sort()
    for word in wordlist:
        if len(word) in range(password_min_length,password_max_length + 1):
            writer.write(word)
            writer.write("\n")
writer.close()