from PIL import Image 
from numpy import asarray 
import matplotlib.pyplot as plt
import numpy as np

# img = Image.open('Sample.png') 
# img = Image.open('luna.jpg') 
# numpydata = asarray(img) 
# print(type(numpydata)) 
# print(numpydata.shape) 

# print(img.format) 
# print(img.size) 
# print(img.mode)

# numpydata[0:,0:,0].shape
# numpydata[0:,0:,1].shape
# numpydata[0:,0:,2].shape
# breakpoint()

# plt.plot(img)

img = np.array(Image.open('luna.jpg'))
plt.figure(figsize=(8,8)) # tamanho de visualização da imagem
plt.imshow(img)
plt.show()
