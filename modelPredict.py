import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import librosa.display
import os
from settings import IMG_HEIGHT, IMG_WIDTH, KEY_LIST

def model_predict(model, detection_list):

    IMAGE_PATH = "temporaryChord.png"
    plt.axis('off')
    plt.ioff()
    images_list = []
    for img in detection_list:
        librosa.display.specshow(img, x_axis=None, y_axis=None)
        plt.savefig(IMAGE_PATH, bbox_inches='tight', pad_inches=0.0)
        image = tf.keras.preprocessing.image.load_img(
            IMAGE_PATH, target_size=(IMG_HEIGHT, IMG_WIDTH))
        image1 = tf.keras.preprocessing.image.img_to_array(image)
        images_list.append(image1)

    image1 = np.vstack(np.expand_dims(np.array(images_list), axis=0))
    del images_list
    image_tensor = tf.convert_to_tensor(image1, dtype=tf.int32)
    del image1
    predictions = np.argmax(model.predict(image_tensor), axis=-1)
    del image_tensor
    os.remove(IMAGE_PATH)

    predictions_list = []
    for x in predictions:
        predictions_list.append(str(KEY_LIST[int(x)]))

    return predictions_list
