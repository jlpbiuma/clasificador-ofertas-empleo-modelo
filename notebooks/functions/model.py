from tensorflow import keras
import tensorflow as tf
import json
from sklearn.utils import shuffle
from datetime import datetime


def create_model(input_dim, num_classes):
    # Model Architecture
    model = keras.Sequential([
        keras.layers.Input(shape=input_dim),
        # keras.layers.Flatten(),
        # keras.layers.Dense(2048, activation='relu'),
        # keras.layers.Dense(1024, activation='relu'),
        keras.layers.Dense(300, activation='relu'),
        keras.layers.Dense(120, activation='relu'),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    # Compile the Model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def create_training_info(train_query, epochs, batch_size, validation_split, verbose):
    training_name = input("Nombre del entrenamiento: ")
    training_info = {
        "name": training_name,
        "table_name": input("Nombre de la tabla: "),
        "description": input("Descripción: "),
        "fecha_inicio": input("Fecha de inicio: "),
        "fecha_fin": input("Fecha de fin: "),
        "query": train_query,
        "training_parameters": {
            "epochs": epochs,
            "batch_size": batch_size,
            "validation_split": validation_split,
            "verbose": verbose
        },
        "fecha_entrenamiento": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    # Rewrite the JSON file model_info.json and add this new training in train array key
    with open('model_info.json', 'r') as json_file:
        model_info = json.load(json_file)
    model_info['train'].append(training_info)
    with open('model_info.json', 'w') as json_file:
        json.dump(model_info, json_file)
    return training_info


def model_train(model, train_query, vector_array, label_array, epochs=10, batch_size=32, validation_split=0.2, verbose=1, balance_data=False):
    # create_training_info(train_query, epochs, batch_size,
    #                      validation_split, verbose)
    callback_early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)
    history = model.fit(vector_array, label_array, epochs=epochs,
                        batch_size=batch_size, validation_split=validation_split, callbacks=[callback_early_stopping])
    return model, history


def backpropagation(epochs, model, learning_rate, vector_array, label_array):
    for epoch in range(epochs):
        with tf.GradientTape() as tape:
            predictions = model(vector_array)
            loss_value = tf.reduce_mean(
                keras.losses.sparse_categorical_crossentropy(
                    label_array, predictions)
            )
        gradients = tape.gradient(loss_value, model.trainable_variables)
        # Update weights and biases
        for param, gradient in zip(model.trainable_variables, gradients):
            param.assign_sub(learning_rate * gradient)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss_value.numpy()}")
    return model


def save_model(model, path_model):
    # Save the Model
    model.save(path_model)


def load_model(path_model):
    # Load the Model
    try:
        model = keras.models.load_model(path_model)
    except:
        model = None
    return model


def history_save(history, path_history):
    # Save the history to a JSON file
    history_data = {
        'accuracy': history.history['accuracy'],
        'val_accuracy': history.history['val_accuracy']
    }
    # Save the data to the JSON file
    with open(path_history, 'w') as json_file:
        json.dump(history_data, json_file)
        return history_data


def history_load(path_history):
    try:
        with open(path_history) as json_file:
            history_data = json.load(json_file)
    except:
        history_data = None
    return history_data
