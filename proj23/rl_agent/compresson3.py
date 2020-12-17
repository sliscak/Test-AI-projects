import streamlit as st
import numpy as np
import pandas as pd
import torch
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import os
# import kornia
from PIL import Image
from time import sleep
from collections import deque
import model
from tqdm import tqdm

def load_img(path:str="image.jpg"):
    image = Image.open(path)
    image = image.resize((64, 64))
    # normalize
    img = np.array(image) / 255
    # img = torch.tensor(img)
    return img



x = st.slider('X', min_value=0.0, max_value=1.0, step=0.1)
y = st.slider('Y', min_value=0.0, max_value=1.0, step=0.1)


image = load_img('image.jpg')
st.image(caption='ORIG:', image=image, width=100)

keys = image.shape[0] * image.shape[1]
x_max = image.shape[0]
y_max = image.shape[1]

# net = model.NeuralDictionaryV5Double(in_features=2, out_features=3, capacity=5000)
# net = model.NeuralDictionaryV5SDouble(in_features=2, out_features=3, capacity=500)
# net = model.NeuralDictionaryV5XDouble(in_features=2, out_features=3, capacity=500)
# net = model.NeuralD3(in_features=2, out_features=3, capacity=500)
net = model.Ann(in_features=2, out_features=3, capacity=500)
net_opt = optim.AdamW(net.parameters(), lr=0.005)
criterion = nn.MSELoss()

loss_ph = st.empty()

loss = None
# for i in tqdm(range(10), desc='LEARNING'):
while (loss is None) or loss >= 160:
    net_opt.zero_grad()
    loss = torch.zeros(1, dtype=torch.double)
    for col in range(y_max):
        for row in range(x_max):
            key = torch.tensor([row/x_max, col/y_max])
            value = torch.tensor(image[(row, col)])
            out = net(key)
            loss += criterion(out, value.detach())
            # net.update(key=key, value=value)
    loss.backward()
    net_opt.step()
    loss_ph.write(f'LOSS: {loss.detach()}')

pixel = net(torch.tensor([x, y])).detach().unsqueeze(0).numpy()
# pixel = np.expand_dims(image[(0,0)], axis=0)
st.write(f'Pixel shape: {pixel.shape}')
st.image(caption='pixel', image=pixel, width=100)

new_image = np.zeros((x_max, y_max, 3), dtype=np.float)
with torch.no_grad():
    for col in tqdm(range(y_max), desc='Reconstructing the image'):
        for row in range(x_max):
            key = torch.tensor([row/x_max, col/y_max])
            pixel = net(key).unsqueeze(0).numpy()
            orig_pixel = image[(row, col)]
            new_image[(row, col)] = pixel
            print(f'O: {orig_pixel}\tN: {pixel}\t K: {key}')

st.image(caption='image', image=new_image, width=100)