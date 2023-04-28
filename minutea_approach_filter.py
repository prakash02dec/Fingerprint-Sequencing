import os
import fingerprint_recognition
import matplotlib

files = os.listdir("SOCOFing/Real/")
files.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))
alter_easy =  os.listdir("SOCOFing/Altered/Altered-Easy/")
alter_easy.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))

alter_medium =  os.listdir("SOCOFing/Altered/Altered-Medium/")
alter_medium.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))

alter_hard =  os.listdir("SOCOFing/Altered/Altered-Hard/")
alter_hard.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))

userID_deleted = []
for file in files:
    try:
        fingerprint_recognition.fingerprint_Matcher("SOCOFing/Real/" + file , "SOCOFing/Real/" + file)
        matplotlib.pyplot.close()
    except (ValueError , IndexError) as error:
        file_start = file.split('__')[0]
        userID_deleted.append(file_start)
        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == file_start , files ))
        
        for file in filess:
            os.remove("SOCOFing/Real/" + file)
            print(file)
            files.remove(file)
        
        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == file_start , alter_easy ))
        for file in filess:
            os.remove("SOCOFing/Altered/Altered-Easy/" + file)
            print(file)
        
        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == file_start , alter_medium ))
        for file in filess:
            os.remove("SOCOFing/Altered/Altered-Medium/" + file)
            print(file)

        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == file_start , alter_hard ))
        for file in filess:
            os.remove("SOCOFing/Altered/Altered-Hard/" + file)
            print(file)

total_user_ID = 600

# for user_id in userID_deleted :
