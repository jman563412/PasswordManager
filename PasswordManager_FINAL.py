# Josh Talkington
# jt0190@unt.edu
# 9/25/2019
#
# This program stores passwords in a file 
# that is encrypted with a master password
#
# system packages: gcc libffi-devel python-devel openssl-devel
# python packages: pycryptodome 
# Tested on Fedora 30 with Python 2.7.16
#
# references:
#   1. https://stackoverflow.com/questions/19232011/convert-dictionary-to-bytes-and-back-again-python
#   2. https://www.pycryptodome.org/en/latest/src/examples.html
# 
# To run:
#	python pwMan.py Google.com
# 
# To reset:
# 	rm passwords
#
# Example Output:
# $ python pwMan.py Google.com
# 	Enter Master Password: pass
# 	No password database, creating....
# 	Loading database...
# 	No entry for  Google.com , creating new...
# 	New entry - enter password for Google.com: pass
# 	stored
# $ python pwMan.py Google.com
# 	Enter Master Password: pass
# 	Loading database...
# 	website:   Google.com
# 	password:  pass

# Updated 9 October 2019 by Peyton Pritchard
# Updated to Python 3.7.4



#The existing template comments have been left in the code to provide references and instructions on usage.
#A README is included in the .ZIP file for the project

#PROJECT PARTNERS:
#Benjamin Cobb
#Justin Dupuis




import random ##random and string imports for our random password generator to function.  
import string
import csv, os, sys, json
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

passwordFile = "passwords"
##The salt value should be set here.
salt = "snailKiller"
##The header of the file.
head = " ____               __  __\n"+"|  _ \ __ _ ___ ___|  \/  | __ _ _ __  \n" +"| |_) / _` / __/ __| |\/| |/ _` | '_ \ \n" +"|  __/ (_| \__ \__ \ |  | | (_| | | | |\n" +"|_|   \__,_|___/___/_|  |_|\__,_|_| |_|\n"



#reference 1
def dictToBytes(dict):
	return json.dumps(dict).encode('utf-8')
def bytesToDict(dict):
	return json.loads(dict.decode('utf-8'))

#reference 2
def encrypt(dict, k):
	##Define the encryption scheme here.
	cipher = AES.new(k, AES.MODE_EAX)
	##Encrypt the dictionary value here.
	ciphertext, tag = cipher.encrypt_and_digest(dict) 
	

	with open(passwordFile, 'wb') as outfile:
		[outfile.write(x) for x in (cipher.nonce, tag, ciphertext)]
def decrypt(k):
	with open(passwordFile, 'rb') as infile:
		nonce, tag, ciphertext = [ infile.read(x) for x in (16, 16, -1) ]
		##Define the encryption scheme here.
		cipher = AES.new(k, AES.MODE_EAX, nonce)
		##Decrypt the ciphertext here.
		data = cipher.decrypt_and_verify(ciphertext, tag)
		
	
		return data

def Main():

	print("\n\n")
	mpw = input("Enter Master Password: ")
	k   = PBKDF2(mpw, salt, dkLen=32) # derive key from password
	
	# check for password database file
	if not os.path.isfile(passwordFile):
		
		# create new passwords file
		print("No password database, creating....")
		newDict = dictToBytes({"": ""})
		encrypt(newDict, k)

	# check usage
	if len(sys.argv)  != 2:
		print("usage: python pwMan.py <website>")
		return
	else:

		# decrypt passwords file to dictionary
		try:
			print("Loading database...")
			pws = decrypt(k)
			pws = bytesToDict(pws)

		except Exception as e:
			print("Wrong password")
			return

		# print value for  website or add new value
		entry = sys.argv[1]
		if entry in pws:
			print("entry   : " + str(entry))
			print("password: " + str(pws[entry]))
		else:
			print("No entry for " + str(entry) + ", creating new...")
			print("Would you like to create a random password or use your own?")
			userRandom = input("Please enter 'y' or 'n'")
			if userRandom == 'y':
				##print("User has selected to create a random password")
				##create random password
				usernameDict = string.ascii_lowercase ##creates the dictionary for the password to use. All lowercase ascii chars in this program.
				randomPass = ''.join(random.choice(usernameDict) for i in range(8)) ##uses the random.choice function to pick 8 random letters from the dictionary.
				##print("random password = "+randomPass)
				pws[entry] = randomPass ##puts the password in the database and the next line calls the encrypt function to encrypt it. 
				encrypt( dictToBytes(pws), k)
				print("Stored")
			else:
				##users opts to input their own password. Same functionality as before except with simple inputs. 
				##print("User has chosen to create their own password")
				newPass = input("New entry - enter password for "+entry+": ")
				pws[entry] = newPass
				encrypt( dictToBytes(pws), k)
				print("Stored")


if __name__ == '__main__':
	print(str(head))
	Main()

