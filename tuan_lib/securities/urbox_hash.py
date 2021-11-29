# -*- coding: utf-8 -*-
import base64
import hashlib
import os
import re
from random import Random

from Crypto.Hash import SHA256, SHA1
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from loguru import logger

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

import OpenSSL

from tuan_lib.securities.config import URBOX_SECRET


class UrboxHash(object):

    @classmethod
    def encode(cls, data: str, key: str = URBOX_SECRET) -> str:
        md5_key = hashlib.md5(key.encode("utf-8")).hexdigest()[0:24]
        data_bytes = bytes(data.encode("utf-8"))
        cipher_txt = (base64.b64encode(data_bytes)).decode("utf-8").replace("=", "")
        cipher = DES3.new(md5_key, DES3.MODE_ECB)
        plain_txt = cipher.encrypt(pad(cipher_txt.encode("utf-8"), DES3.block_size))

        try:
            cipher_base64 = base64.b64encode(plain_txt, altchars="-_".encode("utf-8")).decode("utf-8")
        except Exception as e:
            logger.error(e)
            cipher_base64 = base64.b64encode(plain_txt).decode('utf-8')
            cipher_base64 = cipher_base64.replace('/', '_').replace('+', '-')

        txt = cipher_base64.replace("=", "")
        return txt

    @classmethod
    def decode(cls, data: str, key: str = URBOX_SECRET, is_base64: bool = True) -> str:
        md5_key = hashlib.md5(key.encode("utf-8")).hexdigest()[0:24]
        spacing = '=' * (-len(data) % 4)
        # spacing = "=" * (24 - len(data))
        data = "{data}{spacing}".format(data=data, spacing=spacing)

        try:
            cipher_txt = base64.b64decode(data, altchars="-_")
        except Exception as e:
            logger.error(e)
            data = data.replace('-', '+').replace('_', '/')
            cipher_txt = base64.b64decode(data)

        cipher = DES3.new(md5_key, DES3.MODE_ECB)
        cipher_decrypt = cipher.decrypt(cipher_txt)
        cipher_unpad = unpad(cipher_decrypt, DES3.block_size)
        cipher_unpad_txt = cipher_unpad.decode("utf-8")
        if is_base64 is True:
            cipher_unpad_txt = "{txt}=".format(txt=cipher_unpad_txt)
            bytes_cipher_unpad_txt = bytes(cipher_unpad_txt.encode("utf-8"))
            txt = base64.b64decode(bytes_cipher_unpad_txt + b'=' * (-len(bytes_cipher_unpad_txt) % 4)).decode(
                "utf-8")
        else:
            txt = cipher_unpad_txt
        return txt

    @classmethod
    def sha256(cls, text: str) -> str:
        text_bytes = text.encode('utf-8')
        return hashlib.sha256(text_bytes).hexdigest()

    @classmethod
    def b64encode(cls, text: str) -> str:
        text_bytes = text.encode('utf-8')
        return base64.b64encode(text_bytes).decode('utf-8')

    @classmethod
    def b64decode(cls, text: str) -> str:
        return base64.b64decode(text).decode('utf-8')

    class RSA(object):
        @classmethod
        def sha256_sign_from_file(cls, signature: str, file_path: str) -> str:
            private_key = open(file_path).read()
            return cls.sha256_sign(signature, private_key)

        @classmethod
        def sha256_sign(cls, signature: str, private_key: str) -> str:
            rsa_key = RSA.import_key(private_key)
            signature_bytes = signature.encode('utf-8')
            hash_message = SHA256.new(signature_bytes)
            signature_data = PKCS1_v1_5.new(rsa_key).sign(hash_message)
            return base64.b64encode(signature_data).decode('utf-8')

        @classmethod
        def sha256_verify_from_file(cls, signature: str, raw: str, file_path: str) -> bool:
            public_key = open(file_path).read()
            return cls.sha256_verify(signature, raw, public_key)

        @classmethod
        def sha256_verify(cls, signature: str, raw: str, public_key: str) -> bool:
            rsa_key = RSA.import_key(public_key)
            verifier = PKCS1_v1_5.new(rsa_key)
            raw_bytes = raw.encode('utf-8')
            hash_sha256 = SHA256.new(raw_bytes)
            try:
                verifier.verify(hash_sha256, base64.b64decode(signature))
                return True
            except Exception as e:
                logger.error(e)
                return False

        @classmethod
        def sha1_sign(cls, signature: str, private_key: str) -> str:
            rsa_key = RSA.import_key(private_key)
            signature_bytes = signature.encode('utf-8')
            hash_message = SHA1.new(signature_bytes)
            signature = PKCS1_v1_5.new(rsa_key).sign(hash_message)
            return base64.b64encode(signature).decode('utf-8')

        @classmethod
        def sha1_sign_from_file(cls, signature: str, file_path: str) -> str:
            private_key = open(file_path).read()
            return cls.sha1_sign(signature, private_key)

        @classmethod
        def sha1_verify(cls, signature: str, raw: str, public_key: str) -> bool:
            rsa_key = RSA.import_key(public_key)
            verifier = PKCS1_v1_5.new(rsa_key)
            raw_bytes = raw.encode('utf-8')
            hash_sha1 = SHA1.new(raw_bytes)
            try:
                verifier.verify(hash_sha1, base64.b64decode(signature))
                return True
            except Exception as e:
                logger.error(e)
                return False

        @classmethod
        def sha1_verify_from_file(cls, signature: str, raw: str, file_path: str) -> bool:
            public_key = open(file_path).read()
            return cls.sha1_verify(signature, raw, public_key)

        @classmethod
        def sha1_decode(cls, ciphertext, private_key):
            rsa_key = RSA.import_key(private_key)
            ciphertext_bytes = base64.b64decode(ciphertext)
            digest_size = SHA1.new(ciphertext_bytes).digest_size
            sentinel = Random.new().read(digest_size)
            raw = Cipher_PKCS1_v1_5.new(rsa_key).decrypt(ciphertext_bytes, sentinel)
            return raw.decode('utf-8')

    class VMGHash(object):
        @classmethod
        def decode(cls, data: str, key: str, iv: str) -> str:
            cipher = DES3.new(key.encode('utf-8'), DES3.MODE_CBC, iv.encode('utf-8'))
            content = base64.b64decode(data)
            cipher_decrypt = cipher.decrypt(content)
            try:
                plain_text = cipher_decrypt.decode('utf-8')
            except UnicodeDecodeError:
                plain_text = cipher_decrypt
            plain_text = re.sub('[^A-Za-z0-9]+', '', plain_text)
            return plain_text

    class VTC(object):
        @classmethod
        def verify(cls, text: str, b64signature: str, public_key: OpenSSL.crypto.PKey) -> bool:
            signature = base64.b64decode(b64signature)
            openssl_crypto_x509 = OpenSSL.crypto.X509()
            openssl_crypto_x509.set_pubkey(public_key)
            try:
                OpenSSL.crypto.verify(openssl_crypto_x509, signature, text, "sha256")
                return True
            except Exception as e:
                logger.error(e)
                return False

        @classmethod
        def verify_from_file(cls, text: str, b64signature: str, file_path: str) -> bool:
            public_key = open(file_path, 'rb').read()
            openssl_public_key = OpenSSL.crypto.load_publickey(OpenSSL.crypto.FILETYPE_PEM, public_key)
            return cls.verify(text, b64signature, openssl_public_key)

        @classmethod
        def sign(cls, text: str, private_key: OpenSSL.crypto.PKey) -> str:
            signature = OpenSSL.crypto.sign(private_key, text, "sha256")
            return base64.b64encode(signature).decode('utf-8')

        @classmethod
        def sign_from_file(cls, text: str, file_path: str) -> str:
            private_key = open(file_path, 'rb').read()
            openssl_private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, private_key)
            return cls.sign(text, openssl_private_key)
