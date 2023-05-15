# -*- coding: utf-8 -*-
"""veri_madenciliği.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14jNPBiOjds47alHN-KiNo2rS8kO2vxIu
"""

from google.colab import files
import pandas as pd
import io
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from sklearn import tree

uploaded = files.upload()

dosya_adlari = list(uploaded.keys())
dosya_adı = dosya_adlari[0]

veri = pd.read_csv(io.StringIO(uploaded[dosya_adı].decode('utf-8')),names=["sample_code_number",
                                                                           "clump_thickness","uniformity_of_cell_size",
                                                                           "uniformity_of_cell_shape","marginal_adhession",
                                                                           "single_epithelial_cell_size","bare_nuclei",
                                                                           "bland_chromatin",
                                                                           "normal_nucleoli",
                                                                           "mitoses","class"])
veri.head()

veri.dtypes

def is_non_numeric(x):
  return not x.isnumeric()

mask = veri["bare_nuclei"].apply(is_non_numeric)

data_numeric = veri[~mask]
data_numeric.head()

print(len(veri))
print(len(data_numeric))

print(data_numeric.dtypes)

data_input = data_numeric.drop(columns=["sample_code_number","class"])
data_output = data_numeric["class"]

data_input.head()

data_output.head()

data_output.unique()

data_output = data_output.replace({2: 0 , 4: 1})

data_output.unique()

data_output.head()


X , X_test , y , y_test = train_test_split(data_input,data_output,test_size = 0.33, random_state = 2)

X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.33, random_state = 2)

print(X_train.shape)
print(y_train.shape)

print(X_val.shape)
print(y_val.shape)

print(X_test.shape)
print(y_test.shape)


model = DecisionTreeClassifier(max_depth = 2,random_state = 2)

model.fit(X_train , y_train)


y_pred_train = model.predict(X_train)
y_pred_val = model.predict(X_val)

print(accuracy_score(y_train,y_pred_train))
print(accuracy_score(y_val,y_pred_val))

max_depth_values = [1,2,3,4,5,6,7,8]
train_accuracy_values = []
val_accuracy_values = []

for max_depth_val in max_depth_values:
  model = DecisionTreeClassifier(max_depth = max_depth_val,random_state = 2)
  model.fit(X_train , y_train)
  y_pred_train = model.predict(X_train)
  y_pred_val = model.predict(X_val)
  acc_train = accuracy_score(y_train,y_pred_train)
  acc_val = accuracy_score(y_val,y_pred_val)
  train_accuracy_values.append(acc_train)
  val_accuracy_values.append(acc_val)

train_accuracy_values

val_accuracy_values



plt.plot(max_depth_values,train_accuracy_values,label="acc train")
plt.plot(max_depth_values,val_accuracy_values,label="val train")
plt.legend()
plt.grid('x')
plt.xlabel('max_depth')
plt.ylabel('accuracy')
plt.title('Effect of max_depth on accuracy')
plt.show()

model_best = DecisionTreeClassifier(max_depth = 3,random_state = 2)
model_best.fit(X_train,y_train)

y_pred_test = model_best.predict(X_test)
print(accuracy_score(y_test,y_pred_test))



fig, ax = plt.subplots(figsize=(12, 8))
tree.plot_tree(model_best,
               feature_names=["sample_code_number",
                              "clump_thickness",
                              "uniformity_of_cell_size",
                              "uniformity_of_cell_shape",
                              "marginal_adhession",
                              "single_epithelial_cell_size",
                              "bare_nuclei",
                              "bland_chromatin",
                              "normal_nucleoli",
                              "mitoses",
                              ],
               class_names=["benign","malignant"],
               filled=True,
               ax=ax,
               fontsize=10,
               rounded=True,
               precision=2,
               )
plt.show()

model_best.feature_importances_

feature_names=[
                              "clump_thickness",
                              "uniformity_of_cell_size",
                              "uniformity_of_cell_shape",
                              "marginal_adhession",
                              "single_epithelial_cell_size",
                              "bare_nuclei",
                              "bland_chromatin",
                              "normal_nucleoli",
                              "mitoses",
                              ]
plt.bar(feature_names,model_best.feature_importances_)
plt.xlabel('features')
plt.xticks(rotation = 90)
plt.ylabel('importance')
plt.title("Feature İmportances")
plt.show()