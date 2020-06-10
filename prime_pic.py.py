from PIL import Image
import numpy as numpy
import matplotlib

from random import randrange
import argparse

DEFAULT_SIZE = 32
DEFAULT_THRESHOLD_VALUE = 200

# python prime_pic.py -f ~/Downloads/argentinosaurus.jpg -s 40
# https://www.agiliq.com/blog/2018/01/prime-number-binary-trex/

class PrimeBinaryImage:
	def __init__(self, image_name, image_size=DEFAULT_SIZE, threshold_value=DEFAULT_THRESHOLD_VALUE):
		self.image_name = image_name
		self.image_size = image_size
		self.threshold_value = threshold_value
		self.image_array = self.get_image_as_numpy_array()

	def get_image_as_numpy_array(self):
		img = Image.open(self.image_name)
		img = img.resize((self.image_size, self.image_size), Image.ANTIALIAS)
		img = img.convert("L")
		img_data = np.asarray(img)
		threshold_data = (img_data < self.threshold_value) * 1
		return threshold_data

	def bit_array_to_int(self):
		np.set_printoptions(linewidth=10000)
		np.set_printoptions(threshold=np.nan)
		return int(np.array2string(self.image_array.flatten())[1:-1].replace(" ", ""), 2)

	def get_integer_as_binary_square_string(self, number):
		padded_binary_string = "{0:b}".format(number).zfill(self.image_size**2)
		square = ""
		for i in range(self.image_size):
			k = i * self.image_size
			square += padded_binary_string[k:k + self.image_size].replace("", " ")[1: -1]
			square += "\n"
		return square

	def run(self):
		image_as_int = self.bit_array_to_int()
		prime_image_as_int = self.find_next_prime(image_as_int)
		print("A prime number with binary representation like your image")
		print("It looks like this")
		print(self.get_integer_as_binary_square_string(prime_image_as_int))

	@classmethod
	def find_next_prime(cls, number):
		"Given a number, find next prime number"
		number = number | 1 # ensure last bit is 1
		while (True):
			is_prime = cls.miller_rabin(number)
			if is_prime:
				break
			number += 2
		return number

	@classmethod
	def miller_rabin(cls, n, k=10):
		if n == 2:
			return True
		if not n & 1:
			return False


		def check(a, s, d, n):
			x = pow(a, d, n)
			if x == 1:
				return True
			for i in range(s - 1):
				if x == n - 1:
					return True
				x = pow(x, 2, n)
			return x == n - 1

		s = 0
		d = n - 1


		while d % 2 == 0:
			d >>= 1
			s += 1

		for i in range(k):
			a = randrange(2, n - 1)
			if not check(a, s, d, n):
				return False
		return True


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert images to a prime which matches the images')
	parser.add_argument('-f', '--file', help='Path to image file, use square images for best results.',
                        required=True)
    parser.add_argument('-s', '--size',
                        help='Width/Height of generated image/number', default=DEFAULT_SIZE, type=int,)
    parser.add_argument('-t', '--threshold',
                        help='Bits below this threshold are True', default=DEFAULT_THRESHOLD_VALUE, type=int,)
    args = parser.parse_args()
    args = parser.parse_args()
    prime_binary_image = PrimeBinaryImage(image_name=args.file, image_size=args.size, threshold_value=args.threshold)
    prime_binary_image.run()