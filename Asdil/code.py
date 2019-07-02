# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     code
   Description :
   Author :        Asdil
   date：          2018/12/13
-------------------------------------------------
   Change Activity:
                   2018/12/13:
-------------------------------------------------
"""
__author__ = 'Asdil'

import rsa
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class Code1():
    def __init__(self, pubkey, prikey):
        self.pubkey = pubkey
        self.prikey = prikey

    def encode(self, text):
        self.ciphertext = rsa.encrypt(text.encode(), self.pubkey)
        # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def decode(self, text):
        decrypt_text = rsa.decrypt(a2b_hex(text), self.prikey)
        return decrypt_text


def getkeys(length=256):
    assert isinstance(length, int)
    pubkey, prikey = rsa.newkeys(length)
    return pubkey, prikey


class Code2():
    def __init__(self, key, AES_LENGTH=16):
        self.key = key
        self.mode = AES.MODE_ECB
        self.cryptor = AES.new(self.pad_key(self.key).encode(), self.mode)
        assert isinstance(AES_LENGTH, int)
        self.AES_LENGTH = AES_LENGTH

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    # 加密内容需要长达16位字符，所以进行空格拼接
    def pad(self,text):
        while len(text) % self.AES_LENGTH != 0:
            text += ' '
        return text

    # 加密密钥需要长达16位字符，所以进行空格拼接
    def pad_key(self,key):
        while len(key) % self.AES_LENGTH != 0:
            key += ' '
        return key

    def encode(self, text):

        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        # 加密的字符需要转换为bytes
        # print(self.pad(text))
        self.ciphertext = self.cryptor.encrypt(self.pad(text).encode())
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

        # 解密后，去掉补足的空格用strip() 去掉

    def decode(self, text):
        plain_text = self.cryptor.decrypt(a2b_hex(text)).decode()
        return plain_text.rstrip(' ')

def hp():
    print('加密1: ')
    print('pubkey,prikey = getkeys()')
    print('rs_obj = Code1(pubkey,prikey)')
    print('text="hello"')
    print('ency_text = rs_obj.encode(text)')
    print('解密1')
    print('rs_obj = Code1(pubkey,prikey)')
    print('rs_obj.decode(ency_text)')
    print()
    print('加密2：')
    print('as_obj = Code2(密码)')
    print('e = pc.encode(txt)')
    print('pc.decode(e)')