# make a prediction for a new custom image.
from numpy import argmax
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import load_model

# load and prepare the image
def load_image(filename):
    # load the image
    img = load_img(filename, color_mode="grayscale", target_size=(28, 28))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img


# load an image and predict the class
def run_example(filename):
    # load the image
    img = load_image(filename)
    # load model
    model = load_model('final_model.h5')
    # predict the class
    predict_value = model.predict(img)
    digit = argmax(predict_value)
    print(digit)


# entry point, run the example
image_path = "./sample_image.png"
run_example(image_path)

import matplotlib.pyplot as plt
import matplotlib.image
image = matplotlib.image.imread(image_path)
plt.rcParams['figure.figsize'] = [2, 2]
plt.imshow(image, cmap='gray', vmin = 0, vmax = 255,interpolation='none')
plt.show()