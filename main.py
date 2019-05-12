from read_data import get_data_label
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
from sklearn.metrics import precision_score,recall_score
from keras import regularizers
from keras.layers import LSTM
#读取数据和标签
data,label = get_data_label()
x_train,x_test,y_train,y_test = train_test_split(data,label,test_size=0.1,random_state=0)
#建立模型
model = Sequential()
#建立全连接层
model.add(Dense(128,activation="relu",kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.5))
model.add(Dense(64,activation="relu",kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.5))
model.add(Dense(32,activation="relu",kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.5))
#建立输出层
model.add(Dense(2,activation="softmax"))
#进行训练
model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
train_history = model.fit(x=x_train,y=y_train,validation_split=0.1,epochs=1000,batch_size=50,verbose=2)
scores = model.evaluate(x=x_test,y=y_test)
print("模型测试集准确率:",scores[1])