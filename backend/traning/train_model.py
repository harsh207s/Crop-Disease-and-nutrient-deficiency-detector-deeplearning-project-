import os
import argparse
import json
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

def build_model(num_classes, img_size):
    base = EfficientNetB0(include_top=False, weights="imagenet", input_shape=(img_size, img_size, 3))
    base.trainable = False

    x = layers.Input(shape=(img_size, img_size, 3))
    a = layers.Rescaling(1./255)(x)
    a = base(a, training=False)
    a = layers.GlobalAveragePooling2D()(a)
    a = layers.Dropout(0.3)(a)
    y = layers.Dense(num_classes, activation="softmax")(a)

    model = models.Model(x, y)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model, base

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--img", type=int, default=224)
    ap.add_argument("--out", default="model.h5")
    args = ap.parse_args()

    train = tf.keras.preprocessing.image_dataset_from_directory(
        args.data_dir, validation_split=0.2, subset="training",
        seed=42, image_size=(args.img, args.img), batch_size=args.batch
    )
    val = tf.keras.preprocessing.image_dataset_from_directory(
        args.data_dir, validation_split=0.2, subset="validation",
        seed=42, image_size=(args.img, args.img), batch_size=args.batch
    )

    model, base = build_model(len(train.class_names), args.img)

    callbacks = [
        EarlyStopping(patience=3, restore_best_weights=True),
        ReduceLROnPlateau(patience=2, factor=0.3),
        ModelCheckpoint("best.h5", save_best_only=True)
    ]

    model.fit(train, validation_data=val, epochs=args.epochs, callbacks=callbacks)
    model.save(args.out)

    with open("class_names.json", "w") as f:
        json.dump(train.class_names, f)

    print("✅ Training Complete")
    print("✅ Saved:", args.out)
