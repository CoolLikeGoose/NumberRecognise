# this file needs only to test code
import time
import pickle
from tkinter import filedialog

data = [1, 2, 3, 4, 5, 6]

file_name = 'Number_train/2_15829798300000003.goose'

file = open(file_name, 'wb')
pickle.dump(data, file)
file.close()

file_name = filedialog.askopenfilena()
print(file_name)
file = open(file_name, 'rb')
matrix = pickle.load(file)
file.close()

print(matrix)