# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 09:14:47 2022

@author: RShinde
"""
# !/bin/
import configparser
import os
import calendar
import sys

# Keep the values as it is if configuration file is in default directory
config_file_location = "Config.ini"
config = configparser.RawConfigParser()
try:
    config.read_file(open(config_file_location))
except FileNotFoundError:
    print("[+] Please place Config.ini file in current location or check the value supplied to 'config_file_location' variable")
    sys.exit("[+] Exiting the code due to unavailability of config file")

'''
	Remove variable values from Config.ini file if you don't know its value or do not want a wordlist to be created
'''
print("[+] Importing the variables from {} file for password profiling".format(config_file_location))
nums = config.get("DEFAULT", "NUMS")
nums = nums.split(",")
spl_chars = config.get("DEFAULT", "SPECIAL_CHARS")
spl_chars = spl_chars.split(",")
# setting default values for minimum (0) and maximum (100) password lengths
try:
    password_min_length = int(config.get("DEFAULT", "PASSWORD_MIN_LENGTH"))
except ValueError:
    print("[+] Default value set for PASSWORD_MIN_LENGTH is 0")
    password_min_length = 0
try:
    password_max_length = int(config.get("DEFAULT", "PASSWORD_MAX_LENGTH"))
except ValueError:
    print("[+] Default value set for PASSWORD_MAX_LENGTH is 100")
    password_max_length = 100

first_name = config.get("Names", "FIRST_NAME")
middle_name = config.get("Names", "MIDDLE_NAME")
last_name = config.get("Names", "LAST_NAME")
father_name = config.get("Names", "FATHER_NAME")
mother_name = config.get("Names", "MOTHER_NAME")
pet_name = config.get("Names", "PET_NAME")

birth_year = config.get("Dates", "BIRTH_YEAR")
birth_month = config.get("Dates", "BIRTH_MONTH")
birth_day = config.get("Dates", "BIRTH_DAY")
birth_eve = config.get("Dates", "BIRTH_EVE")

phone_no = config.get("Contact", "PHONE_NO")

masked = bool(config.get("Flags", "MASKED"))
custom_signature = bool(config.get("Flags", "CUSTOM_SIGNATURES"))
password_starts_with = config.get("Flags", "PASSWORD_STARTS_WITH")

FLAG = True  # This flag is created for one time print functions
master_name = {first_name, middle_name, last_name, father_name, mother_name,
               pet_name}  # New custom names will keep getting added to it
# reference for masked ( munged ) passwords "https://en.wikipedia.org/wiki/Munged_password"
# reference for leet keywords "https://en.wikipedia.org/wiki/Leet"
mask_alphabets = {
    "1": "l",
    "a": "@",
    "A": "@",
    "b": "8",
    "c": "(",
    "e": "3",
    "E": "3",
    "f": "#",
    "g": "9",
    "h": "#",
    "i": "!",
    "l": "1",
    "o": "0",
    "s": "5",
    "S": "$",
    "T": "7"
}


# function which will help in patterning strings
def patternizing_strings(base_word="MaTheW"):
    p = ""  # initializing string for concatenated numbers
    for n in nums:
        wordlist.add(base_word + n)  # Mathew1...0
        p = p + n
        wordlist.add(base_word + p)  # Mathew123
        q = ""
        for s in spl_chars:
            wordlist.add(base_word + s)  # Mathew!...)
            q = q + s
            wordlist.add(base_word + q)  # Mathew!@#
            wordlist.add(base_word + p + q)  # Mathew123!@#
    # reinitializing the sequence for reverse password
    q = ""  # initializing string for concatenated special characters
    for s in spl_chars:
        q = q + s
        p = ""
        for n in nums:
            p = p + n
            wordlist.add(Name + q + p)


# Initializing a password set where identified patterns can be stored and unique ones will be eliminated during addition itself
wordlist = set()

'''
	Patterns would be created based on sequenced special chars <-followed by-> numbers and vice versa
	No swapping of special characters will be done for concatenation since that makes wordlist very lengthy for active attacks
'''
name_arr = [first_name, middle_name, last_name, father_name, mother_name, pet_name]
for name in name_arr:  # Assume name is MaTheW
    if name == "":
        continue  # Checking if the value is not null for wordlist creation
    # adding masked word first
    if masked:
        if FLAG:
            print("[+] Masking the alphabets with special characters")
            FLAG = False
        custom_name = ""
        for m_a in mask_alphabets.keys():
            if name.find(m_a) != -1:  # Checking if the alphabet is present or no
                Name = name.replace(m_a, mask_alphabets.get(m_a))
                wordlist.add(Name)
                patternizing_strings(base_word=Name)
                if custom_name == "":
                    custom_name = Name
                custom_name = custom_name.replace(m_a, mask_alphabets.get(m_a))
        patternizing_strings(
            base_word=custom_name)  # Replacing all the characters in the "Name" with special characters
        master_name.add(custom_name)
    # print("[+] Masking the alphabets with special characters for {} as {} with replacement of '{}' as '{}'".format(name,Name,m_a,mask_alphabets.get(m_a)))
    # pure brute force pattern generation
    Name = name.capitalize()
    wordlist.add(Name)  # Mathew
    patternizing_strings(base_word=Name)

'''
Custom signatures will be appended here
'''
if custom_signature:
    print("[+] Using custom signatures for generating passwords")
    # this will hold all the signature aided wordlists
    signatured_wordlist = [phone_no + "@123",
                           phone_no + "@" + birth_year,
                           calendar.month_name[int(birth_month)] + "@" + "123",
                           calendar.month_name[int(birth_month)] + "@" + "12345"]
    # day specific hits which would cover the birth 'day' also
    for day in list(calendar.day_name):
        signatured_wordlist.append(day + "@123")
        signatured_wordlist.append(day + "@12345")
    # name specific custom signature wordlist
    for name in master_name:
        if name == "":
            continue  # Checking if the value is not null for wordlist creation
        signatured_wordlist.append(name + "@" + phone_no[6:])  # name@2312 ( last 4 digits of phone)
        signatured_wordlist.append(name + "@123")  # name@123 ( Common pattern with name )

wordlist_name = "custom_wordlist.txt"
with open(wordlist_name, "w") as writer:
    wordlist = list(wordlist)
    wordlist.sort()
    if custom_signature:
        wordlist = signatured_wordlist + wordlist  # adding custom wordlist at the beginning since it holds highest the most custom password pattern
    print("[+] Generated {} potential passwords".format(len(wordlist)))
    counter = 0
    for word in wordlist:
        if len(word) in range(password_min_length, password_max_length + 1):
        	if password_starts_with == "":
	            writer.write(word)
	            writer.write("\n")
	            counter = counter + 1
	        elif word.startswith(password_starts_with):
	            writer.write(word)
	            writer.write("\n")
	            counter = counter + 1
	        else:
	        	wordlist.remove(word)
        else:
            wordlist.remove(word)
    print("[+] However, only {} potential passwords were written to file as per password lengths & flags submitted by you".format(
        str(counter)))
writer.close()
print("[+] Custom wordlist is created at {}{}{}".format(os.getcwd(), os.sep, wordlist_name))
