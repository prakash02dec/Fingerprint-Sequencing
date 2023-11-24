
import PySimpleGUI as sg
import os
import shutil
from PIL import Image
from fingerprint_sequencing import *

sg.theme('BluePurple')
fingers = ["Left Index", "Left Little", "Left Middle", "Left Ring", "Left Thumb", 
           "Right Index", "Right Little", "Right Middle", "Right Ring", "Right Thumb"]
userID = 10000

def addtopw(listOfFingers,fingerprint_paths, Finger,Password):   
    """ Adds the filename of 'Finger' to list 'Password'""" 
    path = fingerprint_paths[listOfFingers.index(Finger)]
    filename = os.path.basename(path)                 
    Password.append(filename)

def addButtons(altered_fingerprint_paths):
    """ Adds the right column in the authentication window that displays the altered versions of the selected fingerprint """
    buttons = [[sg.Text("Select the suitable altered version: ")]]
    if altered_fingerprint_paths[0]!= ' ':
        CR_button = [sg.Button("Circular Rotated", image_filename = altered_fingerprint_paths[0], key = "CR")]
        buttons.append(CR_button)
    if altered_fingerprint_paths[1]!= ' ':
        Obl_button = [sg.Button("Oblique", image_filename = altered_fingerprint_paths[1], key = "Obl")]
        buttons.append(Obl_button)
    if altered_fingerprint_paths[2]!= ' ':
        Zcut_button = [sg.Button("Z - cut", image_filename = altered_fingerprint_paths[2], key = "Z")]
        buttons.append(Zcut_button)
    return buttons

def fingerprint(user_ID):
    """ Returns a list of fingerprint image paths based on the user's ID """
    real_fingerprint = os.listdir("SOCOFing/Real")
    real_fingerprint.sort(key=lambda fingerprint : int(fingerprint.split('__')[0]))
    user_fingerprint = list(filter(lambda fingerprint : int(fingerprint.split('__')[0]) == user_ID , real_fingerprint ))
    return user_fingerprint

def finger_image_paths(user_prints):
    """ Returns the paths of the images (both png and bmp) obtained from func 'fingerprint' """
    fingerprints = []
    fingerprints_bmp = []
    png_folder_name = "png_images"
    if not os.path.exists(png_folder_name):
        os.mkdir(png_folder_name)
    for i in range(len(user_prints)):
        bmp_directory_path = "SOCOFing/Real/"
        bmp_image_file_name = user_prints[i]
        bmp_image_file_path = os.path.join(bmp_directory_path, bmp_image_file_name)
        fingerprints_bmp.append(bmp_image_file_path)
        bmp_image = Image.open(bmp_image_file_path)
        png_image = bmp_image.convert('RGB')
        base_name, ext = os.path.splitext(bmp_image_file_name)
        png_image_file_name = base_name + ".png"
        png_file_path = os.path.join(png_folder_name, png_image_file_name)
        png_image.save(png_file_path)
        fingerprints.append(png_file_path)
    return fingerprints, fingerprints_bmp

def altered_finger_image_paths(bmp_fingerprints, index):
    """ Returns the path of the altered versions of the image clicked upon in both png and bmp """
    real_user_print = bmp_fingerprints[index]
    altered_paths_bmp = []
    altered_paths_png = []
    png_folder_name = "png_images"
    if not os.path.exists(png_folder_name):
        os.mkdir(png_folder_name)
    directory_path = "SOCOFing\Altered\Altered-Easy"
    file_name = os.path.basename(real_user_print)
    base_name = os.path.splitext(file_name)[0]
    CR_file_name = base_name + "_CR.BMP"
    Obl_file_name = base_name + "_Obl.BMP"
    Zcut_file_name = base_name + "_Zcut.BMP"
    file_names = [CR_file_name, Obl_file_name, Zcut_file_name]
    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if os.path.exists(file_path):
            altered_paths_bmp.append(file_path)
            bmp_image = Image.open(file_path)
            png_image = bmp_image.convert('RGB')
            base_name, ext = os.path.splitext(file_name)
            png_image_file_name = base_name + ".png"
            png_file_path = os.path.join(png_folder_name, png_image_file_name)
            png_image.save(png_file_path)
            altered_paths_png.append(png_file_path)
        else:
            altered_paths_bmp.append(' ')
            altered_paths_png.append(' ')
    return altered_paths_bmp, altered_paths_png

def retrieve_scored_images():
    pass

def window_start(users):   
    """ The primary menu """
    password = []
    entered_password = []
    layout = [[sg.Column(layout=[[sg.Button("Register User", size=(10, 2), button_color=("Black", "cyan"))],
                       [sg.Button("Authentication", size=(10, 2), button_color=("Black", "cyan"))],
                       [sg.Button("Update Sequence", size=(10, 2), button_color=("Black", "cyan"))],
                       [sg.Button("Close")],
                       [sg.Column([], key='-TEXT COLUMN-')]],
               element_justification="center")]]
    window = sg.Window("Fingerprint Sequencing Portal", layout, margins = (250, 80))
    while True:
        event, values = window.read()
        if event == "Register User":
            user = window_userID_registration(users)
            if user:
                user_prints = fingerprint(user.user_ID)
                fingerprint_images, bmp_fingerprint_images = finger_image_paths(user_prints)
                password = window_setPassword(fingerprint_images, bmp_fingerprint_images)
                user.sequence = password
                users.append(user)
            text = [[sg.Text(f'Your registration has been successfully completed. User ID: {user.user_ID}')]]
            column = window.Element('-TEXT COLUMN-')
            window.extend_layout(column, text)
        if event == "Authentication":
            user = window_userID_authentication(users) 
            if user:
                user_prints = fingerprint(user.user_ID)
                fingerprint_paths, bmp_fingerprint_images = finger_image_paths(user_prints)
                access, score = window_enterPassword(fingerprint_paths, bmp_fingerprint_images, user)
                if access:
                    window_resultsMatched(score)
                else:
                    window_resultsUnmatched(score)
        if event == "Update Sequence":
           user = window_userID_authentication(users)
           if user:
               user_prints = fingerprint(user.user_ID)
               fingerprint_paths, bmp_fingerprint_images = finger_image_paths(user_prints)
               access, score = window_enterPassword(fingerprint_paths, bmp_fingerprint_images, user)


        if event == sg.WIN_CLOSED or event =="Close":
            break
    #return password, entered_password

def window_userID_registration(users):         
    """The window to obtain the users' ID"""                                               
    layout = [[sg.Text("Enter your user ID, from 1 to 600: ", size = (40,2))], 
              [sg.InputText()],
              [sg.Button("OK"), sg.Button("Close")],
              [sg.Column([], key='-TEXT COLUMN-')]]
    window = sg.Window("User Registration Portal", layout, margins=(250,80))
    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            user = False
            break
        elif not is_valid_user_id(int(values[0])):
            text = [[sg.Text('The user ID entered is invalid')]]
            column = window.Element('-TEXT COLUMN-')
            window.extend_layout(column, text)
        elif is_user_exist(users,int(values[0])):   
            text = [[sg.Text('This user already exists')]]
            column = window.Element('-TEXT COLUMN-')
            window.extend_layout(column, text)
        else:                               
            if event == "OK":
                user = Sequencing(int(values[0]))
                break            
    window.close()    
    return user

def window_userID_authentication(users):         
    """The window to obtain the users' ID"""                                               
    layout = [[sg.Text("Enter your user ID, from 1 to 600: ", size = (40,2))], 
              [sg.InputText()],
              [sg.Button("OK"), sg.Button("Close")],
              [sg.Column([], key='-TEXT COLUMN-')]]
    window = sg.Window("User Authentication Portal", layout, margins=(250,80))
    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            user = False
            break
        elif not is_valid_user_id(int(values[0])):
            text = [[sg.Text('The user ID entered is invalid')]]
            column = window.Element('-TEXT COLUMN-')
            window.extend_layout(column, text)
        elif not is_user_exist(users,int(values[0])):   
            text = [[sg.Text('This user does not exist')]]
            column = window.Element('-TEXT COLUMN-')
            window.extend_layout(column, text)
        else:                               
            if event == "OK":
                user = find_user(users,int(values[0]))
                break            
    window.close()    
    return user

def window_setPassword(userfingerprints, bmp_fingerprints):              
    """ The window to register password """                    
    seq = []
    left_col = [[sg.Text("Set the fingerprint sequence: ")],
              [sg.Button("Left Index", image_filename = userfingerprints[0]), 
               sg.Button("Left Little", image_filename = userfingerprints[1]), 
               sg.Button("Left Middle", image_filename = userfingerprints[2]), 
               sg.Button("Left Ring", image_filename = userfingerprints[3]), 
               sg.Button("Left Thumb", image_filename = userfingerprints[4])],
              [sg.Button("Right Index", image_filename = userfingerprints[5]), 
               sg.Button("Right Little", image_filename = userfingerprints[6]), 
               sg.Button("Right Middle", image_filename = userfingerprints[7]), 
               sg.Button("Right Ring", image_filename = userfingerprints[8]), 
               sg.Button("Right Thumb", image_filename = userfingerprints[9])], 
              [sg.Button("OK"), sg.Button("Cancel")]]
    right_col = [[sg.Text("Your entered sequence of fingerprints: ")]]
    layout = [[sg.Column(left_col, size=(600, 300), key = 'left_col'), sg.Column(right_col, key = "right_col", scrollable = True, vertical_scroll_only = True, s = (250,300))]]
    window = sg.Window("Registration Portal", layout)
    current_image_list = []
    current_text_list = []
    new_layout = []
    while True:
        event, values = window.read()
        new_layout.clear()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            seq.clear()
            break
        if event == "OK":
            break
        if event in fingers:
            col1 = window['right_col']
            addtopw(fingers, bmp_fingerprints, event, seq)
            new_layout = [[sg.Image(userfingerprints[fingers.index(event)])],
                          [(sg.Text(event))]]        
            window.extend_layout(col1, new_layout)
            window.visibility_changed()
            window['right_col'].contents_changed()
            continue 
    window.close()
    return seq
       
def window_enterPassword(userfingerprints, bmp_fingerprints, user):                                 
    """ The window for authentication """
    seq = []
    left_col = [[sg.Text("Your entered sequence of fingerprints: ")]]
    center_col = [[sg.Text("Enter the correct registered fingerprint sequence: ")],
                [sg.Text("Please choose the finger first, and then the alteration: ")],
                [sg.Button("Left Index", image_filename = userfingerprints[0]), 
                sg.Button("Left Little", image_filename = userfingerprints[1]), 
                sg.Button("Left Middle", image_filename = userfingerprints[2]), 
                sg.Button("Left Ring", image_filename = userfingerprints[3]), 
                sg.Button("Left Thumb", image_filename = userfingerprints[4])],
                [sg.Button("Right Index", image_filename = userfingerprints[5]), 
                sg.Button("Right Little", image_filename = userfingerprints[6]), 
                sg.Button("Right Middle", image_filename = userfingerprints[7]), 
                sg.Button("Right Ring", image_filename = userfingerprints[8]), 
                sg.Button("Right Thumb", image_filename = userfingerprints[9])],             
                [sg.Button("Submit"), sg.Button("Cancel")]]
    altered = [None, None, None]
    right_col = []
    layout = [[sg.Column(left_col, key = "left_col", size=(250, 500), scrollable = True, vertical_scroll_only = True), sg.Column(center_col, key = "center_col", size = (600,500)), sg.Column(right_col, key = "right_col")]]
    window = sg.Window("Authentication Portal", layout)
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            seq.clear()
            break
        if event == "Submit":
            access, score = user.authenticate_sequence(seq)
            break
            # window_fingerprintProcessing(bmp_fingerprints, seq)
        if event in fingers:
            altered_paths_bmp, altered_paths_png = altered_finger_image_paths(bmp_fingerprints,fingers.index(event))
            new_buttons = addButtons(altered_paths_png)
            column = window.Element('right_col')
            window.extend_layout(column, new_buttons)
            window['right_col'].update(visible = True)
            text1 = event
        if event.startswith('CR'):
            if (altered_paths_png[0]!=' '):
                col1 = window['left_col']
                new_layout = [[sg.Image(altered_paths_png[0])],
                            [(sg.Text(text1))]]        
                window.extend_layout(col1, new_layout)
                window.visibility_changed()
                window['left_col'].contents_changed()
                window['right_col'].update(visible=False)
                column = window['right_col']
                for child in column.Widget.winfo_children():
                    child.pack_forget()
                filename = os.path.basename(altered_paths_bmp[0])  
                seq.append(filename)
            continue
        if event.startswith("Obl"):
            if (altered_paths_png[1]!=' '):
                col1 = window['left_col']
                new_layout = [[sg.Image(altered_paths_png[1])],
                            [(sg.Text(text1))]]        
                window.extend_layout(col1, new_layout)
                window.visibility_changed()
                window['left_col'].contents_changed()
                window['right_col'].update(visible=False)
                column = window['right_col']
                for child in column.Widget.winfo_children():
                    child.pack_forget()
                filename = os.path.basename(altered_paths_bmp[1])  
                seq.append(filename)
            continue
        if event.startswith("Z"):
            if (altered_paths_png[2]!=' '):
                col1 = window['left_col']
                new_layout = [[sg.Image(altered_paths_png[2])],
                            [(sg.Text(text1))]]        
                window.extend_layout(col1, new_layout)
                window.visibility_changed()
                window['left_col'].contents_changed()
                window['right_col'].update(visible=False)
                column = window['right_col']
                for child in column.Widget.winfo_children():
                    child.pack_forget()
                filename = os.path.basename(altered_paths_bmp[2])  
                seq.append(filename)
            continue    
    window.close()
    return access, score

def window_updatePassword(userfingerprints):
    pass

def window_fingerprintProcessing(Enteredpassword, imagelist, scores):      
    """Will display the different images from backend"""
    images = []
    for i in range(len(imagelist)):
        images.append([sg.Image(imagelist[i])])
        images.append([sg.Text(scores[i])])
    final_score = np.mean(scores)
    Center_column = [[sg.Text("Matching Fingerprints...")],
                     [images],
                     [sg.Text(final_score, justification = "centre")]]          
    layout = [[sg.Column(Center_column, key = "center_col", size=(350, 350), scrollable = True, vertical_scroll_only = True)]]
    window = sg.Window("Fingerprint Matching", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def window_resultsMatched():
    """Need to get results from backend"""
    layout = [[sg.Text("FINGERPRINTS MATCHED")],
              [sg.Text("Successfully Authenticated")],
              [sg.Button("Close")]]
    window = sg.Window("Success", layout, margins=(150,80))
    while True: 
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
    window.close()

def window_resultsUnmatched():
    """Results from backend"""
    layout = [[sg.Text("FINGERPRINTS DO NOT MATCH")],
              [sg.Text("Authentication Failed")],
              [sg.Button("Close")]]
    window = sg.Window("Failure", layout, margins=(150,80))
    while True: 
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
    window.close()

def main():
    users= []   
    window_start(users) 
    # registered_password, entered_password = window_start(users)
    # print(registered_password)
    # print(entered_password)
    shutil.rmtree("png_images")

if __name__ == '__main__':
    main()
