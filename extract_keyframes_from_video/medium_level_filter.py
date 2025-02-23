import tensorflow as tf
from tensorflow.keras.applications import InceptionV3,MobileNet,MobileNetV2,EfficientNetB0,EfficientNetB1,EfficientNetB2,EfficientNetB3,EfficientNetB4,EfficientNetB5
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
import numpy as np
print(tf.config.list_physical_devices('GPU'))

def check_GPU():
    print(tf.config.list_physical_devices('GPU'))

def get_CNN_model(name = 'InceptionV3'):
    if name == 'InceptionV3':
        base_model = InceptionV3(weights='imagenet', include_top=False)
        input_shape = (299, 299, 3)
    elif name == 'MobileNet':
        base_model = MobileNet(weights='imagenet', include_top=False)
        input_shape = (224, 224, 3)
    elif name == 'MobileNetV2':
        base_model = MobileNetV2(weights='imagenet', include_top=False)
        input_shape = (224, 224, 3)
    elif name == 'EfficientNetB0':
        base_model = EfficientNetB0(weights='imagenet', include_top=False)
        input_shape = (224, 224, 3)
    elif name == 'EfficientNetB1':
        base_model = EfficientNetB1(weights='imagenet', include_top=False)
        input_shape = (240, 240, 3)
    elif name == 'EfficientNetB2':
        base_model = EfficientNetB2(weights='imagenet', include_top=False)
        input_shape = (260, 260, 3)
    elif name == 'EfficientNetB3':
        base_model = EfficientNetB3(weights='imagenet', include_top=False)
        input_shape = (300, 300, 3)
    elif name == 'EfficientNetB4':
        base_model = EfficientNetB4(weights='imagenet', include_top=False)
        input_shape = (380, 380, 3)
    elif name == 'EfficientNetB5':
        base_model = EfficientNetB5(weights='imagenet', include_top=False)
        input_shape = (456, 456, 3)
    else:
        print('Model not found')
        return None
    input_tensor = Input(shape=input_shape)
    base_output = base_model(input_tensor)
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()(base_output)
    embedding_model = Model(inputs=input_tensor, outputs=global_average_layer )
    embedding_model.compile(optimizer='adam', loss='categorical_crossentropy')
    return {'model':embedding_model, 'input_shape':input_shape}

def preprocess_input_images(images):
    images = tf.keras.applications.inception_v3.preprocess_input(images)
    return images

def get_CNN_embeddings(embedding_model, images,batch_size=64):
    model = embedding_model['model']
    input_shape = embedding_model['input_shape']
    images = tf.image.resize(images, [input_shape[0], input_shape[1]])
    preprocessed_data = preprocess_input_images(images)
    batches = np.array_split(preprocessed_data, len(preprocessed_data)//batch_size)
    embeddings = []
    for batch in batches:
        embeddings.append(model.predict(batch))
    embeddings = np.concatenate(embeddings,axis=0)
    return embeddings
