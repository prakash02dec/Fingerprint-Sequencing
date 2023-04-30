from fingerprint_recognition import *
# from cnn_based import *
# from ml_based import *
import numpy as np
import cv2 as cv
import os

def debug_printout(x):
	print("Debug : " , x)

# input exceptional handling
def __input (string):
	x = 0
	while True:
		try:
			x = int(input(string).strip())
			break
		except ValueError:
			print (" Invalid!, Enter only digit.")
			continue
	return x

class Sequencing():
	real_fingerprint = os.listdir("SOCOFing/Real")
	real_fingerprint.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))
	
	altered_easy_fingerprint =  os.listdir("SOCOFing/Altered/Altered-Easy")
	altered_easy_fingerprint.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))
	
	altered_medium_fingerprint =  os.listdir("SOCOFing/Altered/Altered-Medium")
	altered_medium_fingerprint.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))
	
	altered_hard_fingerprint =  os.listdir("SOCOFing/Altered/Altered-Hard")
	altered_hard_fingerprint.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))
	
	def __init__(self, user_id):
		self.user_ID = user_id
		self.user_fingerprint = list(filter(lambda fingerprint : int(fingerprint.split('__')[0]) == self.user_ID , Sequencing.real_fingerprint ))
		self.sequence = []

	def print_fingerprint(self , fingerprint):
		print(f"User {self.user_ID} Stored fingerprint are following : ")
		i=1
		for finger in fingerprint :
			print(f"{i}." ,finger.split(".")[0] )
			i = i+1

	def get_user_fingerprint(self,):
		return self.user_fingerprint
	
	# def get_altered_user_fingerprint(self , difficult):
	# 	match difficult:
	# 		case 0: # for debugging
	# 			fingerprints = list(filter(lambda fingerprint : int(fingerprint.split('__')[0]) == self.user_ID , Sequencing.real_fingerprint ))
	# 			return fingerprints
	# 		case 1:
	# 			fingerprints = list(filter(lambda fingerprint : int(fingerprint.split('__')[0]) == self.user_ID , Sequencing.altered_easy_fingerprint ))
	# 		case 2:
	# 			fingerprints = list(filter(lambda fingerprint : int(fingerprint.split('__')[0]) == self.user_ID , Sequencing.altered_medium_fingerprint))
	# 		case 3:
	# 			fingerprints = list(filter(lambda fingerprint : int(fingerprint.split('__')[0]) == self.user_ID , Sequencing.altered_hard_fingerprint ))
		

	# 	return fingerprints

	def get_altered_user_fingerprint(self, difficult):
		if difficult == 0: # for debugging
			fingerprints = list(filter(lambda fingerprint: int(fingerprint.split('__')[0]) == self.user_ID, Sequencing.real_fingerprint))
		elif difficult == 1:
			fingerprints = list(filter(lambda fingerprint: int(fingerprint.split('__')[0]) == self.user_ID, Sequencing.altered_easy_fingerprint))
		elif difficult == 2:
			fingerprints = list(filter(lambda fingerprint: int(fingerprint.split('__')[0]) == self.user_ID, Sequencing.altered_medium_fingerprint))
		elif difficult == 3:
			fingerprints = list(filter(lambda fingerprint: int(fingerprint.split('__')[0]) == self.user_ID, Sequencing.altered_hard_fingerprint))
		else:
			raise ValueError("Invalid difficulty level")

		return fingerprints

		

	def get_sequence(self):
		return self.sequence
	
	def create_sequence(self , fingers ):
		self.sequence = [ self.user_fingerprint[int(x)-1] for x in fingers ]
		return True


	def authenticate_sequence(self ,sequence , difficult=1):	
		if len(sequence) != len(self.sequence):
			return False , np.array([0])
		
		matching_score = []	
		os.mkdir('cache_match_images')
		for fingerprint in range(len(self.sequence)):
			
			altered_difficulty_folder_loc = {
										0 : "SOCOFing/Real/" ,  # for debuging
										1 : "SOCOFing/Altered/Altered-Easy/"  ,
										2 : "SOCOFing/Altered/Altered-Medium/" ,
										3 :	"SOCOFing/Altered/Altered-Hard/" ,
										}
			try:
				score , match_status , match_image  = fingerprint_Matcher('SOCOFing/Real/' + self.sequence[fingerprint] , altered_difficulty_folder_loc[ difficult ] + sequence[fingerprint] )
			except ValueError:
				cv.destroyAllWindows()
				return False , np.array([0])
			
			match_image = cv.putText(match_image , str(fingerprint+1) , (0,21) ,cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv.LINE_AA)

			# home_dir = os.path.expanduser('~')
			output_path = os.path.join( 'cache_match_images', f"match_finger{str(fingerprint+1)}.png")
			cv.imwrite(output_path, match_image)

			# cv.imshow("match_image" ,match_image)
			# cv.waitKey()

			matching_score.append(score)
			if not match_status : 
				return False , np.array(matching_score)
		
		return True , np.array(matching_score)

# As we have only 600 people fingerprint database
def is_valid_user_id(user_id):
	if user_id > 0 and user_id <= 600 :
		return True
	return False

def find_user(users , user_id):
	for user in users:
		if user.user_ID == user_id :
			return user

def is_user_exist(users , user_id):
	if is_valid_user_id(user_id):
		for user in users:
			if user.user_ID == user_id :
				return True
	return False

def register_user(users):

	print("=========================================================================================")
	print("================================ REGISTRATION PORTAL ====================================")

	user_id = -1 
	while is_user_exist(users , user_id) or not is_valid_user_id(user_id):
		# user_id = int(input("Enter user_id within range from 1 to 600 : ").strip())
		user_id = __input("Enter user_id within range from 1 to 600 : ")
		if not is_valid_user_id(user_id):
			print("Invalid User ID")
		elif is_user_exist(users , user_id):
			print("Already exist")

	user = Sequencing(user_id)
	print("Scan the Fingers one by one in order to create Fingerprint Sequencing Password")
	user.print_fingerprint(user.get_user_fingerprint())
	print("Enter the User's Fingerprint's serial number in order which you want to Register as Sequence : ")
	fingers = input(" Input : ").split()

	user.create_sequence(fingers)
	users.append(user)

	print("Registration Successfull")

def authentication(users):
	print("=========================================================================================")
	print("================================ AUTHENTICATION PORTAL ==================================")
	
	print("Enter the difficult")
	print("1. Easy")
	print("2. Medium")
	print("3. Hard")
	# difficult = int(input(" Choose : ").strip())
	difficult = __input(" Choose : ")

	user_id = -1 
	
	while not is_user_exist(users , user_id) or not is_valid_user_id(user_id):
		# user_id = int(input("Enter user_id within range from 1 to 600 : ").strip())
		user_id = __input("Enter user_id within range from 1 to 600 : ")
		if not is_valid_user_id(user_id):
			print("Invalid User ID")
		elif not is_user_exist(users , user_id):
			print("Does not exist")
			return

	user = find_user(users , user_id)
    
	print("Scan the User's Fingerprint in the same Sequence order to Access System")
	user.print_fingerprint( user.get_altered_user_fingerprint(difficult) ) 
	scanned_fingers = [ user.get_altered_user_fingerprint(difficult)[int(x)-1] for x in input(" Enter the registered fingerprint's sequence  : ").split() ]

	access , score = user.authenticate_sequence( scanned_fingers , difficult)

	os.rmdir('cache_match_images')

	if access :
		print("Access Success")
		print(f"Overall Match Score : {score.mean()}")
	else :
		print("Access Denied. Please try again")

def update_sequence(users):
	print("=========================================================================================")
	print("=============================== SEQUENCE UPDATE PORTAL ==================================")
	
	user_id = -1 
	
	while not is_user_exist(users , user_id) or not is_valid_user_id(user_id):
		# user_id = int(input("Enter user_id within range from 1 to 600 : ").strip())
		user_id = __input("Enter user_id within range from 1 to 600 : ")
		if not is_valid_user_id(user_id):
			print("Invalid User ID")
		elif not is_user_exist(users , user_id):
			print("Does not exist")
			return

	user = find_user(users , user_id)
    
	print("Enter Previous Sequence")
	user.print_fingerprint( user.get_altered_user_fingerprint(difficult =1) ) 
	scanned_fingers = [ user.get_altered_user_fingerprint(difficult = 1)[int(x)-1] for x in input(" Enter the registered fingerprint's sequence  : ").split() ]
	
	access , score = user.authenticate_sequence(scanned_fingers)
	if not access :
		print("Wrong Previous Sequence")
		return
	else :
		print("Enter new Sequence")
		user.print_fingerprint(user.get_user_fingerprint())
		fingers = input(" Input : ").split()
		user.create_sequence(fingers)
		users.append(user)
		print("Update Successfull")


def menu(users):
	while True:
		
		print("=========================================================================================")
		print("============================ FINGERPRINT SEQUENCING PORTAL ==============================")
		print("Choose the option")
		print("1. Register user")
		print("2. Authentication")
		print("3. Update Sequence")
		print("4. Exit")
		
		# option = int(input(" Enter : ").strip())
		option = __input(" Enter : ")

		# match option :
		# 	case 1: 
		# 		register_user(users)
		# 	case 2:
		# 		authentication(users)
		# 	case 3:
		# 		update_sequence(users)
		# 	case 4:
		# 		exit()
		# 	case _:
		# 		print("Please choose a valid option from above")

		if option == 1:
			register_user(users)
		elif option == 2:
			authentication(users)
		elif option == 3:
			update_sequence(users)
		elif option == 4:
			exit()
		else:
			print("Please choose a valid option from above")


def main():
	users = []
	menu(users)
	# fingerprint_Matcher('SOCOFing/Altered/Altered-Hard/151__M_Right_index_finger_Obl.BMP', 'SOCOFing/Real/151__M_Right_index_finger.BMP')

if __name__ == '__main__':
	main()


