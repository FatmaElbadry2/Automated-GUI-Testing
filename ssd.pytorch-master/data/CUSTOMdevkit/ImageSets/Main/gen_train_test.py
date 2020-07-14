import os
import numpy as np

def generate_txt_files(path_to_toy_data):
    files = os.listdir(path_to_toy_data)
    train = open("train.txt", "w")
    # train_val = open("trainval.txt", "w")
    # val = open("val.txt", "w")

    size_train_set = int(len(files) * 1)
    # size_train_val_set = int(len(files) * 0.25)
    # size_val_set = int(len(files) * 0.25)

    train_files = np.random.choice(files, size=size_train_set, replace=False)
    for f in train_files:
        train.write(f.replace(".jpg", "").replace(".JPG", "") + "\n")
        files.remove(f)
    train.close()

    # train_val_files = np.random.choice(files, size=size_train_val_set, replace=False)
    # for f in train_val_files:
    #     train_val.write(f.replace(".jpg", "").replace(".JPG", "") + "\n")
    #     files.remove(f)
    # train_val.close()

    # val_files = np.random.choice(files, size=size_val_set, replace=False)
    # for f in val_files:
    #     val.write(f.replace(".jpg", "").replace(".JPG", "") + "\n")
    #     files.remove(f)
    # val.close()
    print(len(files))


if __name__ == "__main__":
    generate_txt_files("../../JPEGImages")