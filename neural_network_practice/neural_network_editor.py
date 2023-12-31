# -*- coding: utf-8 -*-
"""neural_network_editor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oAkQw6E42h0QuymR9jtdl69k8ltdip34

# ニューラルネット実装

1. データの特徴について確認します。（13問）
    - 各変数のデータ型、行列数、統計量を算出し、今回扱うデータの外観を把握します。
2. データを加工する方法について学習します。（7問）
    - 各変数をモデルに入れる形に整えます。（特徴量生成フェーズ）
3. ニューラルネットワークのモデリング方法について学習します。（19問）
    - ディープラーニングのモデリングと精度を上げるときのポイントについて学習します。
4. CNNについて学習します。（17問）
    - 画像データに対して相性の良いCNNモデルについて学習します。
5. RNNについて学習します。（15問）
    - 時系列、テキストデータ等に対して相性の良いRNNモデルについて学習します。

### 0. 事前準備

#### 0.1  必要なライブラリを読み込んで下さい。
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# 目的変数の加工処理で必要なライブラリ
from tensorflow.keras.utils import to_categorical

# Jupyter 上で図を表示するためのコマンド
# %matplotlib inline

# warningを表示させない
warnings.simplefilter('ignore')

"""#### 0.2 minstを読み込んで、学習データ（説明変数）、学習データ（目的変数）、検証データ（説明変数）、検証データ（目的変数）にデータを格納してください。"""

from keras.datasets import mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

"""### 1.データの特徴について確認します。

#### 1.1説明変数の学習データ（X_train）の レコード数を確認してください。
"""

len(X_train)

"""#### 1.2 目的変数の学習データ（y_train）レコード数を確認してください。"""

len(y_train)

"""#### 1.3（X_train）の行列数（各次元の要素数）を確認してください。"""

X_train.shape

"""#### 1.4 今回の学習データは3次元の性質を持っているようです。今度は正解データの性質を確認してみましょう。（y_train）の行列数を確認してください。"""

y_train.shape

"""#### 1.5 正解データは1次元です。X_trainの1番目（indexは0）のデータの中身を確認してみましょう。"""

X_train[0]

"""#### 1.6 同様にy_trainのデータの中身を確認してみましょう。"""

y_train

"""#### 1.7 y_trainの要素の集計を行いましょう。"""

pd.Series(y_train).value_counts().sort_index()

"""#### 1.8 目的変数は0～9までの数字が割り当てられているようです。説明変数と目的変数それぞれの学習データ、検証データの次元数を確認してみましょう。"""

print('X_train:',X_train.shape)
print('X_test:',X_test.shape)
print('y_train:',y_train.shape)
print('y_test:',y_test.shape)

"""#### 1.9 学習データは60000件、検証データは10000件、学習データの要素数は28×28、それに対して0～9の正解データが存在していることが分かりました。最初の学習データ（indexは0）を可視化してみましょう。※ヒント：「plt.imshow」を使用してください。"""

digit = X_train[0]
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()

"""#### 1.10 色の濃さはどのように表現されているのでしょうか。最初の学習データ（0番目）の最初の要素（0番目）を出力してください。"""

X_train[0][0]

"""#### 1.11 最初の学習データ（indexは0）の6番目の要素（indexは5）を出力してください。※画像と数字を比較して見てください。"""

X_train[0][5]

"""#### 1.12 最初の学習データ（indexは0）を転置させて、6番目の要素（indexは5）を出力してください。※画像と数字を比較して見てください。"""

X_train[0].T[5]

"""#### 1.13 学習データの構成は（60000,28,28）＝（枚数,横座標,縦座標）を表しており、数字が小さいと「白」、大きいと「黒」を表現しているようです。最後にtrain_xの最大値、最小値を確認してみましょう。"""

print(X_train.max())
print(X_train.min())

"""### 2.データの加工方法について学習します。

#### 2.1 kerasに入れる形にデータを整えていきましょう。まず、28×28の画像データ（X_train,X_test）を全て（60000枚）1次元化してください。
"""

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
print('X_train:', X_train.shape)
print('X_test:', X_test.shape)

"""#### 2.2 ディープラーニングは正規化処理を施した方が適切な結果が出ることが多いです。28×28の画像データ（X_train,X_test）の最大値が1になるように正規化してください。"""

X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255
print('X_train:',X_train.max())
print('X_test:',X_test.min())

"""#### 2.3 目的変数の形を「0」、「1」だけで表す必要があります。整数値を2値クラスの配列に変換した上で、y_trainを上から5行表示してください。※ワンホットエンコーディング処理といいます。"""

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
y_train[:5]

"""#### 2.4 説明変数と目的変数の形式は整いました。それでは各ノードにおける「入力」と「出力」のイメージを理解していきましょう。下記の様な「2×3」の行列を作成して、「w」と言う変数に格納して下さい。同様に「3×1」の行列を作成し、「x」という変数に格納して下さい。"""

w = np.array([[1,2,3],[4,5,6]])
x = np.array([[1],[-2],[-3]])
print("----w-----")
print(w)
print("----x----")
print(x)

"""#### 2.5 「3個のデータ」である「x」に重み「w」をかけ合わせて「2個のデータ」を出力してみましょう。※行列演算を行います。ニューラルネットワークはデータに重みをかけ合わせて新たな数値を出力し、その数値を活性化関数で変換して出てきた値を次の層の入力とすることの繰り返しです。"""

np.dot(w, x)

"""#### 2.6 活性化関数のイメージを掴んでいきましょう。「2.5」で算出した行列に、活性化関数の一種である「シグモイド関数」をかけて値を算出して下さい。※値が0～1の間に収まる関数です。kerasでは引数で設定することができます。"""

z = np.dot(w,x)
1 / (1 + np.exp(-z))

"""#### 2.7 活性化関数のイメージを掴んでいきましょう。「2.5」で算出した行列に、活性化関数の一種である「relu」をかけて値を算出して下さい。※正の値はそのまま、負の値は「0」に変換する関数です。kerasでは引数で設定することができます。"""

z = np.dot(w, x)
np.maximum(0, z)

"""### 3.ニューラルネットワークのモデリング方法について学習します。※layerの名前、精度結果が一致している必要は無いです。また、モデリングの実行後、時間がかかる処理があります。

#### 3.1 Sequentialのクラスを読み込んでください。
"""

from keras.models import Sequential
print(Sequential)

"""#### 3.2 全結合レイヤーである「Dense」のクラスを読み込んで下さい。"""

from keras.layers import Dense
print(Dense)

"""#### 3.3 今回は「Sequentialモデル」を使用して、ニューラルネットワークを構築していきましょう。「784」件の入力を受け取り、「32」件の出力を返し、活性化関数が「シグモイド関数」の層を作成してください。※32件にしている理由は特にありません。"""

model = Sequential()
image_size = 784
model.add(Dense(32, activation='sigmoid', input_dim=image_size))
model.summary()

"""#### 3.4 「10」件の出力を返す、活性化関数がソフトマックス関数の出力層を追加し、サマリーを出力して下さい。"""

num_classes = 10
model.add(Dense(num_classes, activation='softmax'))
model.summary()

"""#### 3.5 学習方法をcompile関数で設定しましょう。最適化関数を「確率的勾配降下法（Stochastic gradient descent）」を選択して下さい。誤差関数を「categorical_crossentropy」で設定し、metricsは「正解率」を設定してみましょう。※何を目的として重みを更新するかを決定している部分になります。※確率的勾配降下法は難しい概念なので、本コンテンツでは説明しません。詳しく知りたい方は調べてみて下さい。"""

model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""#### 3.6 学習を実行しましょう。fit関数に学習データを当てはめて下さい。"""

history = model.fit(X_train, y_train)

"""#### 3.7 「3.6」の学習を、epochs「4」で設定して行って下さい。※epochsとは「一つの訓練データを何回繰り返して学習させるか」の数のことです。"""

history = model.fit(X_train, y_train,epochs=4)

"""#### 3.8 学習を繰り返せば、精度が向上することが確認できます。「3.7」の学習を、batch_size=「100」で設定して行って下さい。※batchとは、訓練データをいくつかのかたまりに分割したものを指します。batch_sizeとはそのかたまりのサイズを指します。"""

history = model.fit(X_train, y_train,epochs=4, batch_size=100)

"""#### 3.9 学習速度が早くなっていることが確認できます。ディープラーニングは学習時間が非常にかかるので、データによっては速度を意識する必要があることを覚えておきましょう。学習データに対する結果を確認し、x軸に「epoch」、y軸に「accuracy」のグラフを作成して下さい。"""

plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['accuracy'])
plt.show()

"""#### 3.10 今度は検証データに対する評価結果を確認してみましょう。誤差と正解率を算出して下さい。"""

loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print('loss:',loss)
print('accuracy:',accuracy)

"""#### 3.11 「3.8」の条件と、中間層を「1つ」追加した時と「2つ」追加した時の「モデルサマリ」、「正解率推移」、「評価指標」を確認して下さい。※今までの処理を関数化するイメージです。中間層の入力数と出力数は「32」で設定しましょう。"""

image_size = 784
num_classes = 10
activation = 'sigmoid'

def create_model(layer_num,activation):
     model = Sequential()
     model.add(Dense(layer_num[0], activation=activation, input_shape=(image_size,)))

     for s in layer_num[1:]:
         model.add(Dense(units = s, activation=activation))

     model.add(Dense(units=num_classes, activation='softmax'))
     return model
def evaluate(model, batch_size=100, epochs=4):
     model.summary()
     model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
     history = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs)
     loss, accuracy = model.evaluate(X_test, y_test)

     plt.plot(history.history['accuracy'])
     plt.title('model accuracy')
     plt.ylabel('accuracy')
     plt.xlabel('epoch')
     plt.legend(['training'])
     plt.show()
     print('accuracy',accuracy)

for layers in range(1,4):
    model = create_model([32] * layers,activation)
    evaluate(model)

"""#### 3.12 層を増やせば増やすほど、学習データの精度が劣化していることが確認できました。次は「3.11」の「中間層を2層追加した状態」でエポック数を40回に設定し、学習データの精度の推移を確認して下さい。"""

model = create_model([32]* 3,'sigmoid')
evaluate(model,epochs=40)

"""#### 3.13 「3.12」の条件に加えてepochsを「10」で設定し、学習データと検証データの「誤差」の推移を確認してグラフを出力して下さい。※モデルを初期化する必要はないです。"""

history = model.fit(X_train,y_train,epochs=10, batch_size=100, validation_data=(X_test,y_test))

history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

epochs = range(1,len(loss_values) + 1)

plt.plot(epochs, loss_values, 'bo', label='training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.show()

"""#### 3.14「学習データ」、「検証データ」共に、誤差が減少していることが分かります。複雑なモデルには、沢山の学習が必要なようです。今度は中間層無しで入力数を[32, 64, 128, 256]と変更したときの。学習データの精度を確認してみましょう。"""

for nodes in [32,64,128,256]:
     model = create_model([nodes], 'sigmoid')
     evaluate(model)
     print()

"""#### 3.15 入力数を増やした結果、層を増やした結果より効果が得られました。モデルは複雑になり過ぎず、簡単になり過ぎず、様々な条件を試行して、良いバランスを目指す必要があります。活性化関数を「relu」に変更し、その他は「3.11」の条件で精度を確認してみて下さい。"""

image_size = 784
num_classes = 10
activation = 'relu'

for layers in range(1,4):
     model = create_model([32] * layers,activation)
     evaluate(model)

"""#### 3.16 活性化関数は「sigmoid」ではなく「relu」を使用した方が、一般的には良い精度が得られることが多いです。compileの最適化関数も変更してみましょう。「sgd」から「rmsprop」に変更して精度を確認して下さい。※データによって「最適なモデル」の条件は異なります。様々な観点で試行していくことが重要です。"""

image_size =784
num_classes = 10
activation = 'relu'
model.compile(optimizer='rmsprop',
               loss ='categorical_crossentropy',
               metrics = ['accuracy'])

for layers in range(1,4):
    model = create_model([32] * layers,activation)
    evaluate(model)

"""#### 3.17 約90%程度正解率があるようです。「3.16」で作成したモデルで（X_test[0]）に対して予測結果を出力してみましょう。"""

model.predict(X_test)[0]

"""#### 3.18 配列のままだと少し分かりづらいので、結果をグラフ化してみましょう。"""

pd.Series(model.predict(X_test)[0]).plot()

"""#### 3.19 「7」と言う予測結果が出ています。「1.9」の方法で実際のデータの結果を確認してみましょう。"""

digit = X_test[0].reshape(28,28)
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()

"""### 4.CNNについて学習します。

#### 4.1 Sequentialのクラスを読み込み、modelという変数に格納して下さい。※先程作成したモデルが初期化されます。
"""

from keras import layers
from keras import models
model = models.Sequential()
model

"""#### 4.2 CNNの入力は画像の形式のまま扱う必要があります。X_trainとX_testの形状を画像の形式に変更して下さい。"""

X_train =  X_train.reshape((60000, 28,28,1))
X_test = X_test.reshape((10000,28,28,1))
print('X_train:',X_train.shape)
print('X_test:',X_test.shape)

"""#### 4.3 CNNを構築していきましょう。先ずは活性化関数を「relu」に設定してコンボリューション層を追加し、summaryを出力して下さい。※ヒント：output shapeの形からストライド（移動する幅）の数を推定しましょう。"""

model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)))
model.summary()

"""#### 4.4 CNNはコンボリューション層とプーリング層を交互に組み合わせます。プーリング層を追加し、summaryを出力して下さい。※ヒント：output shapeの形からpool_sizeの数を推定しましょう。"""

model.add(layers.MaxPooling2D(2,2))
model.summary()

"""#### 4.5 「4.3」と同じ要領でコンボリューション層を追加しましょう。"""

model.add(layers.Conv2D(32,(3,3),activation='relu'))
model.summary()

"""#### 4.6 コンボリューション層とプーリング層の出力が3次元であることが分かります。また画像のサイズ（高さ、幅）は層を経るにつれて、縮小していることが分かります。次の手順は3次元の出力をDense層に入力することですが、その前に1次元に変換する必要があります。1次元に変換する「変換層」を追加し、summaryの内容を確認して下さい。"""

model.add(layers.Flatten())
model.summary()

"""#### 4.7 Dense層を追加した後、ソフトマックス関数を用いて、出力層を追加して下さい。"""

model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(10,activation='softmax'))
model.summary()

"""#### 4.8 「3.5」の条件でcompileを設定し、epochsは「4」、batch_sizeは「100」に設定して学習を行って下さい。"""

model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train,y_train,epochs=4,batch_size=100)

"""#### 4.9 CNNを使用することでかなりの高精度が実現できました。画像データは良い特徴量を内部で作り出せるCNNが適しています。最後に最適化手法の「rmsprop」を「4.8」と同様の条件で学習を行って下さい。※モデルは初期化して下さい。"""

from keras import layers
from keras import models
model = models.Sequential()
model.add(layers.Conv2D(32,(3,3),activation='relu', input_shape=(28,28,1)))
model.add(layers.MaxPooling2D(2,2))
model.add(layers.Conv2D(32,(3,3),activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32,activation='relu'))
model.add(layers.Dense(10,activation='softmax'))
model.summary()

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train,y_train,epochs=4,batch_size=100)

"""#### 4.10 学習データに対して約99%程度正解率があるようです。「4.9」で作成したモデルで（X_test[0]）に対して予測結果を出力してみましょう。※「3.17」と数字を比較して見て下さい。"""

model.predict(X_test)[0]

"""#### 4.11 配列のままだと少し分かりづらいので、結果をグラフ化してみましょう。※ディープラーニングより「7」の値が1に近く、確信度が上がっていることが分かります。（より自信を持って「1」ということができている。）"""

pd.Series(model.predict(X_test)[0]).plot()

"""#### 4.12 「7」と言う予測結果が出ています。「1.9」の方法で実際のデータの結果を確認してみましょう。"""

digit = X_test[0].reshape(28,28)
plt.imshow(digit,cmap=plt.cm.binary)
plt.show()

"""#### 4.13 コンボリューション層で行っている処理のイメージを掴んでみましょう。下記の様な5×5の乱数行列を作成して下さい。※seedを0で固定して下さい。"""

np.random.seed(seed=0)
img = np.random.random([5,5])
img

"""#### 4.14 コンボリューション層は画像データにカーネルをかけ合わせる（行列演算）を行うことで、畳み込まれた特徴を生成します。（特徴マップと言います）下記の様なカーネル（3×3の行列)を作成して下さい。※畳み込み操作を行う為のフィルタのことです。"""

a = np.array([[1,0,1],[0,1,0],[1,0,1]])
a

"""#### 4.15 「4.14」で作成したカーネルを「4.13」の疑似画像データにかけ合わせて（行列演算）下記の様な特徴マップを出力して下さい。"""

def conv2(X,k):
     x_row, x_col = X.shape
     k_row, k_col = k.shape
     ret_row, ret_col = x_row - k_row +1, x_col - k_col +1
     ret = np.empty((ret_row, ret_col))
     for y in range(ret_row):
         for x in range(ret_col):
             sub = X[y : y + k_row, x : x + k_col]
             ret[y,x] = np.sum(sub *k)
     return ret
conv2(img, a)

"""#### 4.16 プーリング層のイメージを掴んでみましょう。4.13と同じ、5×5の乱数行列を作成して下さい。※seedを0で固定して下さい。"""

np.random.seed(seed=0)
img = np.random.random([5,5])
img

"""#### 4.17 下記の様な2×2の少領域毎に、最大の値を選択し、4×4の正方行列を作成して下さい。※Pooling層は大抵、Convolutoin層の後に適用されます。役割としては入力データをより扱いやすい形に変形するために、情報を圧縮することが目的です。「max_pooling」と呼ばれる処理になります。"""

out = np.zeros((4,4),dtype=np.float32)

for y in range(out.shape[0]):
     for x in range(out.shape[1]):
         out[y,x] = np.max(img[y:y+2, x:x+2])
out

"""### 5. RNNについて学習します

#### 5.0 事前準備　下記コードを読み込んで下さい。
"""

# 頻度順位10000語までを指定
from keras.datasets import imdb
(X_train,y_train),(X_test,y_test) = imdb.load_data(num_words=10000)

# 元データのレビュー内容は例えば以下の様なデータが格納されています。
def decode_review(num):
    word_index = imdb.get_word_index()
    reversed_word_index = dict(
        [value, key] for (key, value) in word_index.items())

    decoded_review = ' '.join([reversed_word_index.get(i-3, '?') for i in X_train[num]])

    return decoded_review

decode_review(0)

"""#### 5.1 学習データ、検証データのデータ型を調べてみましょう。"""

print('X_train',X_train.shape)
print('y_train', y_train.shape)
print('x_test', X_test.shape)
print('y_test', y_test.shape)

"""#### 5.2 それぞれ25000行のデータが格納されている様です。学習データ「X_train[0]とX_train[1]」の中身を確認してみましょう。それぞれ「行数（単語数）」、「最大値」、「最小値」、「ユニーク数」を出力して下さい。"""

print('X_train[0]行数',len(X_train[0]))
print('X_train[0]最大値',np.array(X_train[0]).max())
print('X_train[0]最小値',np.array(X_train[0]).min())
print('X_train[0]ユニーク値',pd.Series(X_train[0]).nunique())
print('X_train[1]行数',len(X_train[1]))
print('X_train[1]最大値',np.array(X_train[1]).max())
print('X_train[1]最小値',np.array(X_train[1]).min())
print('X_train[1]ユニーク値',pd.Series(X_train[1]).nunique())

"""#### 5.3 同様に学習データ（y_train）の中身を確認してみましょう。「行数」、「最大値」、「最小値」、「ユニーク数」を出力して下さい。"""

print('行数',len(y_train))
print('最大値',np.array(y_train).max())
print('最小値',np.array(y_train).min())
print('ユニーク値',pd.Series(y_train).nunique())

"""#### 5.4 今回のデータは各レビューに対し、「0」か「1」の教師データが対応しているようです。そして、各レビュー内の単語に対し出現頻度の順位が数値として、各単語に割り当てられています。学習データの「行数」が異なるので揃えていきましょう。今回は「500」で設定して下さい。※ヒント：preprocessingのモジュールのsequenceを使用します。"""

from tensorflow.keras.preprocessing import sequence
X_train = sequence.pad_sequences(X_train,maxlen=500)
X_test = sequence.pad_sequences(X_test,maxlen=500)
print('X_train',X_train.shape)
print('X_test',X_test.shape)
print('X_train[0]', X_train[0])

"""#### 5.5 説明変数のサイズが揃い、準備は整いました。現在扱っている「テキストデータ」や「時系列データ等」、データの「順序」に意味があるデータに関しては、一般的なディープラーニングやCNNより、RNNのほうが適しています。それでは、RNNを実装してみましょう。layersクラスから「Embedding」、「SimpleRNN」を読み込んで下さい。"""

from keras.layers import Embedding,SimpleRNN
print(Embedding)
print(SimpleRNN)

"""#### 5.6 Sequentialのクラスを読み込み、modelという変数に格納して下さい。※モデルが初期化されます。"""

model = Sequential()
model

"""#### 5.7 Embedding層を追加して下さい。Embeddingとは単語や文を固定のベクトルに置き換える処理のことです。出力数は「10」を設定しましょう。※Embeddingは本来は特徴量エンジニアリングに分類されます。"""

model.add(Embedding(10000,10))
model.summary()

"""#### 5.8 RNN層を追加して下さい。"""

model.add(SimpleRNN(30))
model.summary()

"""#### 5.9 出力層を追加しましょう。活性化関数はシグモイドを設定して下さい。"""

model.add(Dense(1,activation='sigmoid'))
model.summary()

"""#### 5.10 compileの設定をしましょう。最適化関数を「rmsprop」を選択して下さい。誤差関数を「binary_crossentropy」で設定し、metricsは「正解率」を設定してみましょう。※何を目的として重みを更新指定行くかを決定している部分になります。"""

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['acc'])

"""#### 5.11 エポック数は「4」、バッチサイズは「100」、validation_splitを「0.2」に設定して学習を開始して下さい。"""

history = model.fit(X_train,y_train,epochs=4,batch_size=100,validation_split=0.2)

"""#### 5.12 「学習データ(acc)」、「検証データ(val_acc)」の精度をエポック毎にグラフを表示して下さい。"""

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']

epochs = range(len(acc))

plt.plot(epochs,acc,'bo',label='acc')
plt.plot(epochs,val_acc,'go',label='Val_acc')
plt.legend()
plt.show()

"""#### 5.13 学習データ・検証データに対して約80％以上の正解率があるようです。「5.12」で作成したモデルで（X_train[1]）に対して予測結果を出力してみましょう。"""

model.predict(X_train)[1]

"""#### 5.14 悪いレビューである可能性が高そうです。事前準備「5.0」を利用してレビュー内容を確認してみましょう。"""

decode_review(1)

"""#### 5.15 実際の正解データを確認していきましょう。y_train[1]のラベルを確認して下さい。"""

print('y_train[1]:',y_train[1])