#!/uspeech_recognition/bin/env python3
"""
This is a demo for a voice biometrics application
"""

# ------------------------------------------------------------------------------------------------------------------------------------#
#                                                  Installing Packages Needed                                                         #
# ------------------------------------------------------------------------------------------------------------------------------------#


# This is used to dump the models into an object
import pickle
import datetime
import os                                               # For creating directories
import shutil 
import config
import pyttsx3
# import librosa  

                                       # For deleting directories
import io

# Imports the Google Cloud client library
# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types
# from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
import scipy.cluster
import scipy.io.wavfile
# For the speech detection alogrithms
import speech_recognition
# For the fuzzy matching algorithms
from fuzzywuzzy import fuzz
# For using the MFCC feature selection
from python_speech_features import mfcc
# For generating random words
from random_words import RandomWords
from sklearn import preprocessing
# For using the Gausian Mixture Models
from sklearn.mixture import GaussianMixture

from watson_developer_cloud import SpeechToTextV1

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/Downloads/My First Project-d521e1ec5329.json"
# Note: Is there a better way to do this?
# This is the file where the credentials are stored
import config

speech_to_text = SpeechToTextV1(
    iam_apikey=config.APIKEY,
    url=config.URL
)

from flask import Flask, render_template, request, jsonify, url_for, redirect, abort, session, json

PORT = 8080

# Global Variables
random_words = []
random_string = ""
username = ""
user_directory = "Users/Test"
filename = ""
filename_wav = ""
# initialisation 
class _TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()


    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()
# engine = pyttsx3.init() 

# #voice interaction
# def audio_int(num_samples=50):
#     """ Gets average audio intensity of your mic sound. You can use it to get
#         average intensities while you're talking and/or silent. The average
#         is the avg of the 20% largest intensities recorded.
#     """
        
#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
#               for x in range(num_samples)] 
#     values = sorted(values, reverse=True)
#     r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
#     print(" Average audio intensity is ", r)
#     stream.close()
#     p.terminate()
    
#     if r > THRESHOLD:
#         listen(0)
    
#     threading.Timer(SILENCE_LIMIT, audio_int).start()

# def listen(x):
#     r=rs.Recognizer()
#     if x == 0:
#         system('say Hi. How can I help?')
#     with rs.Microphone() as source:
#         audio=r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         y = process(text.lower())
#         return(y)
#     except:
#         if x == 1:
#             system('say Good Bye!')
#         else:
#             system('say I did not get that. Please say again.')
#             listen(1)

# # def process(text):
# #  #   ''''''''''''''''''''''''''''''''''''''''''''''''
# #  #   '''''''Your application goes here ''''''''''''''
# #  #   ''''''''''''''''''''''''''''''''''''''''''''''''
app = Flask(__name__)
@app.route('/')
@app.route('/home')


def home():
    tts3 = _TTS()
    tts3.start("Hi Welcome to Navigation help")
    del(tts3)
    tts4 = _TTS()
    tts4.start("press ee to enroll and aa to authenticate")
    del(tts4)    
    return render_template('main.html')



@app.route('/enroll', methods=["GET", "POST"])
def enroll():
    global username
    global user_directory

    if request.method == 'POST':
        data = request.get_json()

        username = data['username']
        password = data['password']
        repassword = data['repassword']

        user_directory = "Users/" + username + "/"

        # Create target directory & all intermediate directories if don't exists
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)
            print("[ * ] Directory ", username,  " Created ...")
        else:
            print("[ * ] Directory ", username,  " already exists ...")
            print("[ * ] Overwriting existing directory ...")
            shutil.rmtree(user_directory, ignore_errors=False, onerror=None)
            os.makedirs(user_directory)
            print("[ * ] Directory ", username,  " Created ...")

        return redirect(url_for('voice'))

    else:
        tts5 = _TTS()
        tts5.start("You can signup right now")
        del(tts5)
        return render_template('enroll.html')


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    global username
    global user_directory
    global filename

    user_exist = False

    if request.method == 'POST':

        data = request.get_json()
        print(data)

        user_directory = 'Models/'
        username = data['username']
        password = data['password']

        print("[ DEBUG ] : What is the user directory at auth : ", user_directory)
        print("os.fsencode(user_directory : ", os.fsencode(user_directory))
        directory = os.fsencode(user_directory)
        print("directory : ", os.listdir(directory)[1:])

        for file in os.listdir(directory):
            print("file : ", file)
            filename = os.fsdecode(file)
            if filename.startswith(username):
                print("filename : ", filename)
                user_exist = True
                break
            else:
                pass

        if user_exist:
            print("[ * ] The user profile exists ...")
            return "User exist"

        else:
            print("[ * ] The user profile does not exists ...")
            return "Doesn't exist"

    else:
        print('its coming here')
        tts6 = _TTS()
        tts6.start("You can authenticate yourself right now")
        del(tts6)
        return render_template('auth.html')


@app.route('/vad', methods=['GET', 'POST'])
def vad():
    if request.method == 'POST':
        global random_words

        f = open('./static/audio/background_noise.wav', 'wb')
        f.write(request.data)
        f.close()

        background_noise = speech_recognition.AudioFile(
            './static/audio/background_noise.wav')
        with background_noise as source:
            speech_recognition.Recognizer().adjust_for_ambient_noise(source, duration=5)

        print("Voice activity detection complete ...")

        random_words = RandomWords().random_words(count=5)
        print(random_words)

        return "  ".join(random_words)

    else:
        background_noise = speech_recognition.AudioFile(
            './static/audio/background_noise.wav')
        with background_noise as source:
            speech_recognition.Recognizer().adjust_for_ambient_noise(source, duration=5)

        print("Voice activity detection complete ...")

        random_words = RandomWords().random_words(count=5)
        print(random_words)

        return "  ".join(random_words)


@app.route('/voice', methods=['GET', 'POST'])
def voice():
    
    global user_directory
    global filename_wav
   

    print("[ DEBUG ] : User directory at voice : ", user_directory)

    if request.method == 'POST':
        #    global random_string
        global random_words
        global username

        filename_wav = user_directory + "-".join(random_words) + '.wav'
        f = open(filename_wav, 'wb')
        f.write(request.data)
        f.close()

        with open(filename_wav, 'rb') as audio_file:
             recognised_words = speech_to_text.recognize(audio_file, content_type='audio/wav').get_result()

        print("*************************************************************************************")     
        print(recognised_words)
        print("*************************************************************************************")     

        # recognised_words = str(recognised_words['results'][0]['alternatives'][0]['transcript'])
        

        # print("IBM Speech to Text thinks you said : " + recognised_words)
        # print("IBM Fuzzy partial score : " + str(fuzz.partial_ratio(random_words, recognised_words)))
        # print("IBM Fuzzy score : " + str(fuzz.ratio(random_words, recognised_words)))       

        if fuzz.ratio(random_words, recognised_words) < 5:
            print(
                "\nThe words you have spoken aren't entirely correct. Please try again ...")
         
            return "pass"
        else:
            pass

        return "pass"

    else:
       
        return render_template('voice.html')
    # tts12 = _TTS()
    # tts12.start("You can now provide your voice print and background noice. please follow the instructions to continue")
    # del(tts12)

@app.route('/biometrics', methods=['GET', 'POST'])
def biometrics():
    global user_directory
    print("[ DEBUG ] : User directory is : ", user_directory)

    if request.method == 'POST':
        pass
    else:
        # MFCC
        print("Into the biometrics route.")

        directory = os.fsencode(user_directory)
        features = numpy.asarray(())

        for file in os.listdir(directory):
            filename_wav = os.fsdecode(file)
            if filename_wav.endswith(".wav"):
                print("[biometrics] : Reading audio files for processing ...")
                (rate, signal) = scipy.io.wavfile.read(user_directory + filename_wav)

                extracted_features = extract_features(rate, signal)

                if features.size == 0:
                    features = extracted_features
                else:
                    features = numpy.vstack((features, extracted_features))

            else:
                continue

        # GaussianMixture Model
        print("[ * ] Building Gaussian Mixture Model ...")

        gmm = GaussianMixture(n_components=32,
                            max_iter=200,
                            covariance_type='diag',
                            n_init=3)

        gmm.fit(features)
        print("[ * ] Modeling completed for user :" + username +
            " with data point = " + str(features.shape))

        # dumping the trained gaussian model
        # picklefile = path.split("-")[0]+".gmm"
        print("[ * ] Saving model object ...")
        pickle.dump(gmm, open("Models/" + str(username) +
                            ".gmm", "wb"), protocol=None)
        print("[ * ] Object has been successfully written to Models/" +
            username + ".gmm ...")
        print("\n\n[ * ] User has been successfully enrolled ...")

        features = numpy.asarray(())
        tts2 = _TTS()
        tts2.start("User has been successfully enrolled")
        del(tts2)
        return "User has been successfully enrolled ...!!"


@app.route("/verify", methods=['GET'])
def verify():
    global username
    global filename
    global user_directory
    global filename_wav

    print("[ DEBUG ] : user directory : " , user_directory)
    print("[ DEBUG ] : filename : " , filename)
    print("[ DEBUG ] : filename_wav : " , filename_wav)

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                   LTSD and MFCC                                                     #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    # (rate, signal) = scipy.io.wavfile.read(audio.get_wav_data())
    (rate, signal) = scipy.io.wavfile.read(filename_wav)

    extracted_features = extract_features(rate, signal)

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                          Loading the Gaussian Models                                                #
    # ------------------------------------------------------------------------------------------------------------------------------------#
    

    gmm_models = [os.path.join(user_directory, user)
                  for user in os.listdir(user_directory)
                  if user.endswith('.gmm')]

    # print("GMM Models : " + str(gmm_models))

    # Load the Gaussian user Models
    models = [pickle.load(open(user, 'rb')) for user in gmm_models]

    user_list = [user.split("/")[-1].split(".gmm")[0]
                 for user in gmm_models]

    log_likelihood = numpy.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        scores = numpy.array(gmm.score(extracted_features))
        log_likelihood[i] = scores.sum()

    print("Log liklihood : " + str(log_likelihood))

    identified_user = numpy.argmax(log_likelihood)

    print("[ * ] Identified User : " + str(identified_user) +
          " - " + user_list[identified_user])

    auth_message = ""

    if user_list[identified_user] == username:
        
  
        # testing 
        # engine.say("You have been authenticated") 
        
        print("[ * ] You have been authenticated!")
        auth_message = "success"
        # engine.runAndWait() 
        tts = _TTS()
        tts.start("You have been authenticated")
        del(tts)
    else:
         # testing 
        # engine.say("Sorry you have not been authenticated") 
         
        print("[ * ] Sorry you have not been authenticated")
        auth_message = "fail"
        # engine.runAndWait()
        tts1 = _TTS()
        tts1.start("Sorry you have not been authenticated")
        del(tts1)
    return auth_message


def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix
    (https://appliedmachinelearning.blog/2017/11/14/spoken-speaker-identification-based-on-gaussian-mixture-models-python-implementation/)"""

    print("[Delta] : Calculating delta")

    rows, cols = array.shape
    deltas = numpy.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows - 1:
                second = rows - 1
            else:
                second = i+j
            index.append((second, first))
            j += 1
        deltas[i] = (array[index[0][0]]-array[index[0][1]] +
                     (2 * (array[index[1][0]]-array[index[1][1]]))) / 10
    return deltas


def extract_features(rate, signal):
    print("[extract_features] : Exctracting featureses ...")

    mfcc_feat = mfcc(signal,
                     rate,
                     winlen=0.020,  # remove if not requred
                     preemph=0.95,
                     numcep=20,
                     nfft=1024,
                     ceplifter=15,
                     highfreq=6000,
                     nfilt=55,

                     appendEnergy=False)

    mfcc_feat = preprocessing.scale(mfcc_feat)

    delta_feat = calculate_delta(mfcc_feat)

    combined_features = numpy.hstack((mfcc_feat, delta_feat))

    return combined_features


if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0', port=PORT, debug=True)
