import tensorflow as tf
import tensorflow.keras as keras
import os
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
  
  def analyse_emotion(self, path_to_user):
    preds_str = []
    interps = []

    #can edit this as necessary, for example remove disgust and apply softmax as necessary, if delete emotions,
    #adjust the index as necessary, alphabetical order is preserved due to how keras reads in directories
    # idx2emotion = {0:'angry', 1:'disgust', 2:'fear', 3:'happy', 4:'neutral', 5:'sad', 6:'surprise'}
    idx2emotion = {0:'negative', 1:'negative', 2:'negative', 3:'positive', 4:'neutral', 5:'negative', 6:'positive'}


    # overall_emotion = {'angry':0, 'disgust':0, 'fear':0, 'happy':0, 'neutral':0, 'sad':0, 'surprise':0}
    #get all the images in the path
    for item in os.listdir(path_to_user):
      cropped_img_path = os.path.join(path_to_user, item)
      if os.path.isfile(cropped_img_path):
        
        pred = self.get_emotion(cropped_img_path)
        #convert the predictions to indexes
        idx = np.argmax(pred)
        #delete emotions as necessary

        #run softmax function IF DELETE INDEX, ELSE NN output is already normalized
        #pred = np.exp(pred)/np.sum(pred)

        emotion = idx2emotion[idx]
        preds_str.append(emotion)

        #create the dictionary for the interps
        current_iteration = {}

        for i,score in enumerate(list(pred)):
          emotion = idx2emotion[i]
          current_iteration[emotion] = score
          # overall_emotion[emotion] += score
        
        interps.append(current_iteration)
      
    
    # overall_face_emotion = sorted(overall_emotion.items(), key=lambda x:x[1], reverse = True)[0][0]
        
    return preds_str, interps 
    



         
      

#intended usage of the class, note that the directory can be changed as per usage intention
# new_detector = EmotionDetector('trained_emotion.keras')

# print(new_detector.get_emotion('1.jpg'))