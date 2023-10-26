#All Libraries must be imported here to be exttracted by the Main file
import speech_recognition as sr
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import time
import subprocess
import pyttsx3
import json
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import librosa
from scipy.spatial import distance
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
import imaplib
import random
import numpy as np
import io
import string
from pydub import AudioSegment
import wave
import webrtcvad
import os
import re
import noisereduce as nr
import soundfile as sf
import scipy.signal
from email.parser import BytesParser
from email import policy
recognizer = sr.Recognizer()


