from fingerprint_recognition import *
import os

def fingerprint_Matcher(fingerprint1, fingerprint2):
    fp1 = Recognition(fingerprint1)
    fp1.analyze()
    fp2 = Recognition(fingerprint2)
    fp2.analyze()
    
    tf1 , tm1, tls1 = fp1.fingerprint , fp1.valid_minutiae , fp1.local_structures
    tf2 , tm2, tls2 = fp2.fingerprint , fp2.valid_minutiae , fp2.local_structures
    
    dists = np.sqrt(np.sum((tls1[:,np.newaxis,:] - tls2)**2, -1))
    dists /= (np.sqrt(np.sum(tls1**2, 1))[:,np.newaxis] + np.sqrt(np.sum(tls2**2, 1)))
    num_p = 5 
    pairs = np.unravel_index(np.argpartition(dists, num_p, None)[:num_p], dists.shape)
    score = 1 - np.mean(dists[pairs[0], pairs[1]]) 
    print(f'Comparison score: {score:.2f}')
    cv.imshow("dsf", draw_match_pairs(tf1, tm1, tls1, tf2, tm2, tls2, fp1.ref_cell_coords, pairs,len(pairs[0])-1 , False) ) 
    # cv.imwrite(file, sample)
    cv.waitKey()
    if score > 0.85:
        print("Matched!")
        return score , True
    else:
        print("Unmatched!")
        return score , False


# fingerprint_Matcher('SOCOFing/Altered/Altered-Hard/151__M_Right_index_finger_Obl.BMP', 'SOCOFing/Real/151__M_Right_index_finger.BMP')

real_files = os.listdir("SOCOFing/Real")
real_files.sort(key=lambda f: int(f.split('__')[0]))
altered_easy_files =  os.listdir("SOCOFing/Altered/Altered-Easy")
altered_easy_files.sort(key=lambda f: int(f.split('__')[0]))
print("========================CREATING FINGERPRINT SEQUENCE PASSWORD ==========================")
entered_user = int(input("Enter user_id from range of 1 to 600 : "))
# print(Entered_user)
user_fp_data = real_files[(entered_user-1)*10:(entered_user-1)*10+10]
# print(user_fp_data)
# print(len(user_fp_data))
print("SCAN THE FINGER TO CREATE OF SEQUENCE PASSWORD")
i = 1
print("Given user fingerprint are following :")
for finger in user_fp_data :
	print(i , " " ,finger.split(".")[0] , "\n")
	i = i+1

fingerprint_sequence = [ user_fp_data[int(x)-1] for x in input("\nEnter the fingerprint respective no ").split()]
print("Entered finger sequence : " ,fingerprint_sequence)

print("========================AUTHENTICATION==========================")
print("Enter the Finger print sequence password to access")
print("SCAN THE FINGER ONE BY ONE AND THE SCANNING BY APPENDING $ AT LAST")
scanned_finger = []

end = False
while not end :
	user = int(input("Enter user_id from range of 1 to 60 : "))
	# user = entered_user
	user_fp_data = real_files[(user-1)*10:(user-1)*10+10]
	print("Scan the finger" , '\n')
	i = 1
	print("Given user fingerprint are following :")
	for finger in user_fp_data :
		print(i , " " ,finger.split(".")[0] , "\n")
		i = i+1
	temp = input("\nEnter the fingerprint respective no ").split()
	for x in temp:
		if x != "$":
			scanned_finger.append( user_fp_data[int(x)-1] )
		else:
			end = True
			break
print(scanned_finger , "\n")

if len(fingerprint_sequence) != len(scanned_finger):
	print("Unmatched!")
else :
	sequence_match_score = []
	temp = True
	for i in range(len(fingerprint_sequence)):
		score , match_status = fingerprint_Matcher('SOCOFing/Real/' + fingerprint_sequence[i] , 'SOCOFing/Real/' +scanned_finger[i] )
		if match_status : 
			sequence_match_score.append(score)
		else : 
			print("Unmatched")
			temp = False
			break
	if len(sequence_match_score) == len(fingerprint_sequence) and temp :
		sequence_match_score = np.array(sequence_match_score)
		print("Score : " , sequence_match_score.mean())
		print("Matched")



