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
            alter_easy.remove(file)
        
        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == file_start , alter_medium ))
        for file in filess:
            os.remove("SOCOFing/Altered/Altered-Medium/" + file)
            print(file)
            alter_medium.remove(file)

        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == file_start , alter_hard ))
        for file in filess:
            os.remove("SOCOFing/Altered/Altered-Hard/" + file)
            print(file)
            alter_hard.remove(file)

# userID_deleted = ['2', '6', '9', '11', '13', '15', '16', '18', '19', '22', '30', '31', '33', '41', '43', '50', '59', '61', '63', '66', '69', '74', '76', '78', '80', '82', '84', '91', '96', '101', '107', '110', '114', '115', '117', '118', '119', '121', '122', '125', '127', '130', '135', '136', '138', '140', '141', '148', '154', '156', '160', '165', '173', '174', '176', '177', '178', '180', '183', '187', '190', '192', '200', '201', '204', '209', '212', '217', '221', '225', '226', '233', '239', '240', '243', '245', '248', '249', '251', '252', '257', '261', '263', '269', '271', '277', '284', '288', '290', '292', '293', '294', '296', '297', '300', '301', '303', '307', '312', '315', '325', '332', '334', '338', '345', '347', '349', '352', '365', '368', '369', '380', '384', '387', '389', '391', '406', '415', '418', '419', '421', '423', '427', '430', '434', '438', '443', '449', '452', '454', '457', '459', '461', '464', '467', '470', '473', '476', '478', '480', '483', '485', '490', '493', '500', '502', '506', '508', '511', '515', '521', '523', '526', '527', '529', '531', '534', '537', '539', '543', '545', '548', '551', '554', '562', '564', '566', '568', '569', '571', '574', '577', '578', '581', '587', '600']

last_user_ID = 600

for user_id in userID_deleted :
    while(str(last_user_ID) in userID_deleted):
        userID_deleted.remove(str(last_user_ID))
        last_user_ID -=1
    if str(last_user_ID) not in userID_deleted :
        
        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == str(last_user_ID) , files ))
        for file in filess:
            os.rename( "SOCOFing/Real/"+file  , "SOCOFing/Real/"+ str(user_id) + '__' + file.split('__')[1] )
        
        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == str(last_user_ID) , alter_easy ))
        for file in filess:
            os.rename( "SOCOFing/Altered/Altered-Easy/" + file  , "SOCOFing/Altered/Altered-Easy/" + str(user_id) + '__'+ file.split('__')[1] )

        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == str(last_user_ID) , alter_medium ))
        for file in filess:
            os.rename( "SOCOFing/Altered/Altered-Medium/" +file  , "SOCOFing/Altered/Altered-Medium/" + str(user_id) + '__' + file.split('__')[1] )

        filess =  list(filter(lambda fingerprint : fingerprint.split('__')[0] == str(last_user_ID) , alter_hard ))
        for file in filess:
            os.rename( "SOCOFing/Altered/Altered-Hard/" + file  , "SOCOFing/Altered/Altered-Hard/" + str(user_id) + '__' + file.split('__')[1] )

        last_user_ID -= 1


        
