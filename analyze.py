import numpy as np
import pandas as pd
import cv2 as cv 
from skimage import io
from PIL import Image 
import imutils

# Load image and apply thresholding
def load_image(filename):
  image = cv.imread(filename)
  image = imutils.resize(image, width=400)
  image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  image_gray = cv.medianBlur(image_gray, 15)

  #ret, thresh = cv.threshold(image_gray, 170, 255, cv.THRESH_BINARY)
  thresh = cv.adaptiveThreshold(image_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 13, 2)

  return image_gray, thresh

# Get contours from the prepared thresholded image
def find_contours(thresh):
  # Use Canny edge detector
  edges = cv.Canny(thresh, 100, 200, 5)

  # Use morphology transforms to clean up
  kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (17,17))
  #dilated = cv.dilate(edges, kernel)
  dilated = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

  # Find contours in image
  contours, hierarchy = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

  # Find biggest contour
  areas = [cv.contourArea(c) for c in contours]
  max_index = np.argmax(areas)
  cnt = contours[max_index]

  # Display output
  image_contours = np.zeros(edges.shape, dtype='uint8')
  cv.drawContours(image_contours, contours, -1, (0,255,0), 2)
  return cnt

# Create a geometric simplification of the shape
def approx_shape(image, cnt):
  approx_curve = cv.approxPolyDP(cnt, 12, True)
  image_contours = np.zeros(image.shape, dtype='uint8')
  cv.drawContours(image_contours, [approx_curve], -1, (255,0,0), 2)
  return approx_curve

def analyze(filename1, filename2):
  image_gray1, thresh1 = load_image(filename1)
  image_gray2, thresh2 = load_image(filename2)
  cnt1 = find_contours(thresh1)
  cnt2 = find_contours(thresh2)
  shape1 = approx_shape(thresh1, cnt1)
  shape2 = approx_shape(thresh2, cnt2)
  difference = cv.matchShapes(shape1, shape2, 1, 0.0)
  print("Match difference " + str(difference))
  return difference < 2
