import numpy as np
import PIL 
import tensorflow as tf

class EmotionDetector:

  def __init__(self, trained_model_path):
    self.model = tf.keras.models.load_model(trained_model_path)


  #Should be the path to a cropped face, majority of the image should be face if not not likely to work well,
  #(can easily be changed to batch of images if necessary)
  def get_emotion(self, path_to_cropped_face):
    pil_image = PIL.Image.open(path_to_cropped_face).convert('L')

    #reshape the pil image
    pil_image = pil_image.resize((48,48))

    #convert to numpy array
    to_model = np.array(pil_image).reshape((1,48,48,1))

    #return the softmax output, in the following order: 1. Angry, 2. Disgust, 3. Fear, 4. Happy, 5. Neutral, 6. Sad
    #7.Surprise

    #For now, extract the 1d array of emotion probabilities as per the order above, can be changed as necessary if
    #input is batch
    pred = self.model(to_model).numpy()[0]

    return pred
  

#intended usage of the class, note that the directory can be changed as per usage intention
new_detector = EmotionDetector('trained_emotion.keras')

print(new_detector.get_emotion('1.jpg'))