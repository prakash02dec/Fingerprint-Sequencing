import cv2 as cv


def fingerprint_Matcher(fingerprint1, fingerprint2):
    kp1 , kp2 , mp = None , None , None
    sample = cv.imread(fingerprint1)
    fingerprint_image = cv.imread(fingerprint2)
    sift = cv.SIFT_create()

    keypoints_1 , descriptors_1 = sift.detectAndCompute(sample , None)
    keypoints_2 , descriptors_2 = sift.detectAndCompute(fingerprint_image , None)

    matches = cv.FlannBasedMatcher({'algorithm':1 , 'trees' : 10} , {}).knnMatch(descriptors_1 , descriptors_2 ,k=2)

    match_points = []
 

    for p,q in matches:
        if p.distance <0.1 *q.distance:
            match_points.append(p)

    keypoints = 0
    if len(keypoints_1) < len(keypoints_2):
        keypoints = len(keypoints_1)
    else:
        keypoints = len(keypoints_2)

    score = len(match_points)/keypoints
    kp1 , kp2 , mp = keypoints_1 , keypoints_2 , match_points

    # print("SCORE: "+ str(score))

    result = cv.drawMatches(sample , kp1 , fingerprint_image , kp2 , mp ,None)
    result = cv.resize(result ,None , fx=4 , fy=4)
    if score > 0.70:
        # print("Matched!")
        return  score , True , result
    else:
        # print("Unmatched!")
        return  score , False , result

