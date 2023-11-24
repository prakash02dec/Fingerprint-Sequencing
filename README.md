
# Fingerprint-Sequencing

In this project, we propose a method for generating a series of fingerprints using minutiae detection approach for authentication purposes. The system captures multiple fingerprints of the user over time and generates a sequence of minutiae-based features to enhance the security of the authentication process. The proposed method uses preprocessing techniques to enhance the quality of the fingerprint images and then applies the minutiae extraction algorithm to extract minutiae features. We also use a technique to remove false minutiae to improve the accuracy of the system. The generated sequence of minutiaebased features is stored in a secure database for authentication purposes. During the
authentication process, the system captures multiple fingerprints of the user and generates a sequence of minutiae-based features, which is compared to the stored sequence for authentication. The proposed system offers a robust and secure authentication mechanism by using multiple fingerprints and generating a sequence of minutiae-based features. This approach is expected to improve the accuracy and reliability of fingerprint authentication systems, making them more suitable for use in high-security applications. Overall, our proposed method shows promising results in generating a sequence of fingerprints for authentication purposes, and further research can be conducted to improve the performance and usability of the system


## Installation

Requirements: Python 3.9

```bash
pip install pysimpleGUI
pip install opencv-contrib-python
```

## Setup
1. Clone the project on your PC.
2. Download the Socofing Fingerprint Database from Kaggle [datasets](https://www.kaggle.com/datasets/ruizgara/socofing).
3. Install required libraries from the Installation section.
4. Run the following commands in the terminal:
```bash
  python dataset_filter.py
```
This will clean and remove fingerprints that are not properly taken. It will take around 10 minutes.
5. Now run on terminal
```bash
   python GUI_integrated.py
```

## Screenshots

![Screenshot1](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001428.png)

![Screenshot2](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001458.png)

![Screenshot3](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001524.png)

![Screenshot4](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001547.png)

![Screenshot5](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001601.png)

![Screenshot6](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001707.png)

![Screenshot7](https://github.com/prakash02dec/Fingerprint-Sequencing/blob/main/img/Screenshot%202023-05-09%20001741.png)

