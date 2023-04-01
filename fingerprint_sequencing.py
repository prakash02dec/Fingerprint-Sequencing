from fingerprint_recognition import *
import numpy as np
import cv2 as cv
import os

def debug_printout(x):
	print("Debug : " , x)

class Sequencing():
	real_fingerprint = os.listdir("SOCOFing/Real")
	real_fingerprint.sort(key=lambda f: int(f.split('__')[0]))
	
	altered_easy_fingerprint =  os.listdir("SOCOFing/Altered/Altered-Easy")
	altered_easy_fingerprint.sort(key=lambda f: int(f.split('__')[0]))
	
	altered_medium_fingerprint =  os.listdir("SOCOFing/Altered/Altered-Medium")
	altered_medium_fingerprint.sort(key=lambda f: int(f.split('__')[0]))
	
	altered_hard_fingerprint =  os.listdir("SOCOFing/Altered/Altered-Hard")
	altered_hard_fingerprint.sort(key=lambda f: int(f.split('__')[0]))
	
	def __init__(self, user_id):
		self.user_ID = user_id
		self.user_fingerprint = Sequencing.real_fingerprint[(self.user_ID-1)*10:(self.user_ID-1)*10+10]
		self.sequence = []

	def get_user_fingerprint(self,):
		print(f"User {self.user_ID} Stored fingerprint are following : ")
		for finger in self.user_fingerprint :
			print(" " ,finger.split(".")[0] , "\n")
	
	def get_sequence(self):
		print("Entered finger sequence : " ,self.sequence)

	def create_sequence(self):
		self.sequence = [ self.user_fingerprint[int(x)-1] for x in input(" Enter the User's Fingerprint's serial number in order which you want to Register as Sequence : ").split()]
		return True
	

	def authenticate_sequence(self , difficult ,):
		altered_user_fingerprint = []
		match difficult:
			case 0: # for debugging
				altered_user_fingerprint = Sequencing.real_fingerprint[(self.user_ID-1)*10:(self.user_ID-1)*10+10]  
			case 1:
				altered_user_fingerprint = Sequencing.altered_easy_fingerprint[(self.user_ID-1)*30:(self.user_ID-1)*30+30]
			case 2:
				altered_user_fingerprint = Sequencing.altered_medium_fingerprint[(self.user_ID-1)*30:(self.user_ID-1)*30+30]
			case 3:
				altered_user_fingerprint = Sequencing.altered_hard_fingerprint[(self.user_ID-1)*30:(self.user_ID-1)*30+30] 
		
		sequence = [ altered_user_fingerprint[int(x)-1] for x in input(" Enter the fingerprint'serial no of user in order which you want to register as Sequence : ").split()]
		
		if len(sequence) != len(self.sequence):
			print("Access Denied. Please try again")
			return False , 0
		
		matching_score = []
			
		for fingerprint in range(len(self.sequence)):
			
			altered_difficulty_folder_loc = {
										0 : "SOCOFing/Real/" ,  # for debuging
										1 : "SOCOFing/Altered/Altered-Easy/"  ,
										2 : "SOCOFing/Altered/Altered-Medium/" ,
										3 :	"SOCOFing/Altered/Altered-Hard/" ,
										}

			score , match_status , match_minutiae_image  = fingerprint_Matcher('SOCOFing/Real/' + self.sequence[fingerprint] , altered_difficulty_folder_loc[ difficult ] + sequence[fingerprint] )
			
			if match_status : 
				matching_score.append(score)
			else : 
				return False , np.array(matching_score).mean()
		
		return True , np.array(matching_score).mean()
		

def menu():
	print("=========================================================================================")
	print("========================CREATING FINGERPRINT SEQUENCE PASSWORD ==========================")
	user_id = int(input("Enter user_id within range from 1 to 600 : "))
	user = Sequencing(user_id)
	print("Scan the Fingers one by one in order to create Fingerprint Sequencing Password")
	user.get_user_fingerprint()
	user.create_sequence()

	print("=========================================================================================")
	print("======================================AUTHENTICATION=====================================")
	
	print("Enter the difficult")
	print("1. Easy")
	print("2. Medium")
	print("3 .Hard")
	difficult = int(input(" Choose : "))
	

	scanned_finger = []
	
	user_id = int(input("Enter user_id from range of 1 to 600 : "))
	while user.user_ID != user_id :
		user_id = int(input("Enter user_id from range of 1 to 600 : "))
    
	print("Scan the User's Fingerprint in the same Sequence order to Access System")
	user.get_user_fingerprint()
	
	access = user.authenticate_sequence(difficult)
	
	if access :
		print("Access Success")
	else :
		print("Access Denied")


menu()
# fingerprint_Matcher('SOCOFing/Altered/Altered-Hard/151__M_Right_index_finger_Obl.BMP', 'SOCOFing/Real/151__M_Right_index_finger.BMP')