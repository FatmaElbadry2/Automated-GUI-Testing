import numpy as np
import sys
import time
import webbrowser
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat
from PyQt5.QtWidgets import QApplication, QMainWindow
import logging
import re

# based on code from http://john.nachtimwald.com/2009/08/22/qplaintextedit-with-in-line-spell-check

from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.lib import translate
from openlp.core.lib.ui import create_action



