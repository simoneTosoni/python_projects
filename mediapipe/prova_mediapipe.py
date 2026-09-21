#! /bin/env/pyhton3

import mediapipe as mp
import cv2 as cv
import sys
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

if __name__ == '__main__':

    path: str = r'/home/simone/python/mediapipe/foto_persona_di_spalle.jpg'
    image = cv.imread(path,1)

    if image is None:
            sys.exit("Non posso aprire l'immagine")

    window = 'Originale'
    cv.namedWindow(window,cv.WINDOW_NORMAL)
    cv.imshow(window,image)
    #cv.waitKey(0)

    base_options = python.BaseOptions(model_asset_path='/home/simone/python/mediapipe/pose_landmarker_lite.task')
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=True)
    detector = vision.PoseLandmarker.create_from_options(options)

    image = mp.Image.create_from_file(path)

    detection_result = detector.detect(image)

    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    cv.namedWindow('Posa persona di spalle',cv.WINDOW_NORMAL)
    cv.imshow('Posa persona di spalle',cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))

    #segmentation_mask = detection_result.segmentation_masks[0].numpy_view()
    #visualized_mask = np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
    #cv.imshow('Ciao',visualized_mask)

    cv.waitKey(0)
    cv.destroyAllWindows()
