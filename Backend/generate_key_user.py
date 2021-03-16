import random


chars = '+-/*!&$?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generator_key(length_key):
    password = ''
    for i in range(length_key):
        password += random.choice(chars)
    return password
