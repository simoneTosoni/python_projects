#! /bin/env/python3

import mediapipe as mp
import cv2
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import sys
import graphviz
import pydot

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red

def visualize(
    image,
    detection_result
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

  return image

if __name__ == '__main__':

    base_options = python.BaseOptions(model_asset_path='/home/simone/python/mediapipe/efficientdet_lite0.tflite')
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
    detector = vision.ObjectDetector.create_from_options(options)


    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Non è possibile acquisire video dalla telecamera')
        exit()

    while True:
        ret, frame = cap.read() # cattura un frame
        if not ret:
            print("Non riesco ad acquisire nulla")
            break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        detection_result = detector.detect(mp_image)

        image_copy = np.copy(mp_image.numpy_view())
        annotated_image = visualize(image_copy, detection_result)
        rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        cv2.namedWindow('objects',cv2.WINDOW_NORMAL)
        cv2.imshow('objects',rgb_annotated_image)

        #cv2.imshow('image',frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

