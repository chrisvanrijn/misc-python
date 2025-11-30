
from random import randbytes, randint

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms, modes


KEY_SIZE = 32 # 256 bits for AES256
NONCE_SIZE = 16 # block_size / 8


def xor_bytes(bs1: bytes, bs2: bytes):
	return bytes(b1 ^ b2 for (b1, b2) in zip(bs1, bs2, strict=True))


def decrypt_ecb(key: bytes, data: bytes):
	cipher = Cipher(algorithms.AES256(key), modes.ECB())
	decryptor = cipher.decryptor()

	return decryptor.update(data) + decryptor.finalize()


def get_nonce(key: bytes, encrypted: bytes, decrypted: bytes):
	# keystream
	ks = xor_bytes(encrypted, decrypted)

	len_ks = len(ks)
	if len_ks < NONCE_SIZE:
		# pad with zeros
		ks += b'\x00' * (NONCE_SIZE - len_ks)

	result = decrypt_ecb(key, ks)

	return result


def encrypt_gcm(key: bytes, iv: bytes, data: bytes):
	cipher = Cipher(algorithms.AES256(key), modes.GCM(iv))
	encryptor = cipher.encryptor()

	encrypted = encryptor.update(data) + encryptor.finalize()

	# return encrypted, encryptor.tag
	return encrypted


def decrypt_ctr(key: bytes, nonce: bytes, data: bytes):
	cipher = Cipher(algorithms.AES256(key), modes.CTR(nonce))
	decryptor = cipher.decryptor()

	decrypted = decryptor.update(data) + decryptor.finalize()

	return decrypted


def main():
	key = randbytes(KEY_SIZE)

	iv_gcm = randbytes(randint(8, 128)) # arbitrary (valid) size

	plaintext = randbytes(randint(0, 4096)) # arbitrary size

	ciphertext = encrypt_gcm(key, iv_gcm, plaintext)

	nonce_ctr = get_nonce(
		key,
		ciphertext[:NONCE_SIZE],
		plaintext[:NONCE_SIZE]
	)

	print(f'GCM IV: {iv_gcm.hex()}')
	print(f'CTR nonce: {nonce_ctr.hex()}')

	test_dec = decrypt_ctr(key, nonce_ctr, ciphertext)

	print(f'success: {plaintext == test_dec}')


main()

