# -*- coding: utf-8 -*-
"""machine_learning_editor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mJ5HpMX3fIwNhEbbzCtTeLAEwyS8kvfw

# 機械学習実装

1. データの特徴について確認します。（6問）
    - 各変数のデータ型、行列数、統計量を算出し、今回扱うデータの外観を把握します。
2. データを加工する方法について学習します。（11問）
    - 各変数をモデルに入れる形に整えます。（特徴量生成フェーズ）
3. 特徴量の選別方法について学習します。（11問）
    - 各特徴量の詳細な特徴を把握し、目的変数との関連性を確認します。（特徴量評価フェーズ）
4. 学習データと検証データに分割することについて学習します。（3問）
    - 学習に使用したデータは検証に使用できません。モデリング前の下準備について把握します。
5. 決定木モデルについて学習します。（分類）（23問）
    - 決定木モデルを参考に機械学習のフローについて理解し、精度を算出することが目的です。
6. ロジスティック回帰について学習します。（分類）（8問）
    - ロジスティック回帰で精度を算出することが目的です。
7. ランダムフォレストについて学習します。（分類、回帰）（16問）
    - ランダムフォレストモデルで精度を算出することが目的です。
8. Kmeans法について学習します。（クラスタリング）（15問）
    - Kmeansで分類し、分類結果を次元削減して2次元で可視化します。

### 0. 事前準備
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Jupyter 上で図を表示するためのコマンド
# %matplotlib inline

# warningを表示させない
warnings.simplefilter('ignore')

"""#### 0.2  訓練データと検証データを分ける関数、精度評価を行う関数を読み込んで下さい。"""

# 必要な関数を読み込む
from sklearn.model_selection import train_test_split # 訓練データと検証データに分ける関数
from sklearn.metrics import confusion_matrix, accuracy_score # 混同行列, 予測正解率を求める関数

"""#### 0.3  今回使用する「タイタニック」データを読み込んで下さい。"""

# タイタニックデータを読み込む
titanic_data = pd.read_csv(filepath_or_buffer='https://wals.s3-ap-northeast-1.amazonaws.com/curriculum/ai/titanic3.csv',
                          sep=',', dtype={'pclass':'str'})

"""#### 0.4  今回使用する「タイタニック」データは以下のようなデータになっています。

- Pclass: 　乗客の階級、1が一番位が高い
- Survived: 　生存結果 (1: 生存, 0: 死亡)
- Name: 　乗客の名前
- Sex:　 性別
- Age: 　年齢
- SibSp: 　兄弟、配偶者の数
- Parch: 　両親、子供の数
- Ticket: 　チケット番号
- Fare: 　乗船料金
- Cabin: 　部屋番号
- Embarked: 　乗船した港　Cherbourg、Queenstown、Southamptonの3種類
- boat: 　乗ったボート（生きていた場合）
- body: 　身体識別番号
- home.dest: 　目的地

### 1. データの特徴について確認します。（6問）

#### 1.1 レコード数を確認してください。
"""

len(titanic_data)

"""#### 1.2 カラムの数を確認してください。"""

len(titanic_data.columns)

"""#### 1.3 上から5行データを確認してください。"""

titanic_data.head()

"""#### 1.4 各カラムのデータ型を確認してください。※objectデータは今後数値データに変更する必要があります。"""

titanic_data.dtypes

"""#### 1.5 各カラムの統計量を算出してください。※object以外"""

titanic_data.describe().round(1)

"""#### 1.6 objectデータが格納されているカラムの情報を出力してください。"""

titanic_data.describe(exclude=['number'])

"""### 2.データを加工する方法について学習します。（11問）

#### 2.1 object型のデータを削除し、削除されていることを確認してください。
"""

d_titanic_data = titanic_data.drop(['pclass','name','sex','ticket', 'cabin','embarked','boat','home.dest'], axis=1)
d_titanic_data

"""#### 2.2 各カラムの欠損値数を算出してください。(※object型のデータ除外後)"""

d_titanic_data.isnull().sum()

"""#### 2.3 欠損値は補完する必要があります。「age」の分布を確認して下さい。"""

plt.hist(d_titanic_data['age'])
plt.show()

"""#### 2.4 分布を確認すると20代が多いようです。欠損値には「age」の平均値を補完してみましょう。"""

mean = d_titanic_data['age'].mean()
d_titanic_data.update(d_titanic_data['age'].fillna(mean))

"""#### 2.5 「age」に欠損値が無くなったことを確認してください。"""

d_titanic_data['age'].isnull().sum()

"""#### 2.6 bodyの欠損値も補完する必要があります。「body」の分布を確認して下さい。"""

plt.hist(d_titanic_data['body'])
plt.show()

"""#### 2.7 欠損値が非常に多いです。欠損に意味を持たせるために、今存在しない値である「－1」を補完してみましょう。"""

null = -1
d_titanic_data['body'].fillna(null, inplace =True)

"""#### 2.8 bodyに欠損値が無くなったことを確認してください。"""

d_titanic_data['body'].isnull().sum()

"""#### 2.9 fareの欠損値も補完する必要があります。「fare」の分布を確認して下さい。"""

plt.hist(d_titanic_data['fare'])
plt.show()

"""#### 2.10 fareの欠損値は1件です。レコードを削除しても殆ど影響が無いので、削除してしまいましょう。1行減ったことを確認して下さい。"""

d_titanic_data = d_titanic_data.dropna()
d_titanic_data.shape

"""#### 2.11 欠損値が無くなったことを確認して下さい。"""

d_titanic_data.isnull().any()

"""### 3. 特徴量の選別方法について学習します。（11問）

#### 目的変数と説明変数の関連性の調査を行います。目的変数に対してどういう変数が影響力を持っているか、前もって調査しておくことは大切です。その方法について学んでいきましょう。今回の目的変数は「survived」です。生存：1、死亡：0となります。

#### 3.1 「sibsp」のユニーク値毎に、生存割合を算出して下さい。※小数点3桁で表示して下さい。
"""

d_titanic_data.groupby('sibsp').mean()['survived'].round(3)

"""#### 3.2 「parch」のユニーク値毎に、生存割合を算出してください。※小数点3桁で表示して下さい。"""

d_titanic_data.groupby('parch').mean()['survived'].round(3)

"""#### 3.3 「parch」のユニーク値毎に、生存の件数を出力する下記グラフを出力してください。"""

cross_tab_temp = pd.crosstab(d_titanic_data['parch'], d_titanic_data['survived'])
cross_tab_temp.plot.bar(stacked=True)

"""#### 3.4 「age」はユニーク数が多く、値をグルーピングする必要があります。値を「10」刻みでグループ化し、各グループ毎に生存割合を算出してください。"""

s_cut = pd.cut(d_titanic_data['age'], [0,10,20,30,40,50,60,70,80,90,100])
d_titanic_data.groupby(s_cut).mean()['survived'].round(3)

"""#### 3.5「3.4」の生存の件数グラフを出力してください。"""

cross_tab_tmp = pd.crosstab(s_cut, d_titanic_data['survived'])
cross_tab_tmp.plot.bar(stacked=True)

"""#### 3.6 「fare」はユニーク数が多く、値をグルーピングする必要があります。値を昇順にして上から順番に「件数ができるだけ均等になるよう」グループ化を行い、各グループ毎に生存割合を算出してください。※値に重複があるので、完全に均等にする必要はありません。"""

s_cut = pd.qcut(d_titanic_data['fare'],5)
d_titanic_data.groupby(s_cut).mean()['survived'].round(3)

"""#### 3.7「3.6」の生存の件数グラフを出力してください。"""

cross_tab_tmp = pd.crosstab(s_cut, d_titanic_data['survived'])
cross_tab_tmp.plot.bar(stacked=True)

"""#### 3.8 「body」はユニーク数が多く、値をグルーピングする必要があります。最大値と最小値の間を等間隔で5分割してください。"""

s_cut = pd.cut(d_titanic_data['body'],5)
d_titanic_data.groupby(s_cut).mean()['survived'].round(3)

"""#### 3.9「3.8」の生存の件数グラフを出力してください。"""

cross_tab_tmp = pd.crosstab(s_cut, d_titanic_data['survived'])
cross_tab_tmp.plot.bar(stacked=True)

"""#### 3.10 各変数間の相関係数を算出してください。"""

d_titanic_data.corr()

"""#### 3.11 「3.10」はこのままだと少し見辛いので、ヒートマップを作成してください。"""

d_titanic_data.corr().style.background_gradient(axis=None)

"""### 4. 学習データと検証データに分割する方法を学習します。（3問）

#### 先程のフェーズでは、全て数値データに変換し、今回予測する「生存」との関連性を評価しました。今フェーズはモデルの作成の為の最終準備です。未知のデータに対する予測値を算出したいので、学習に使用するデータと検証に使用するデータを分割し、擬似的に未知データを作り出します。

#### 4.1 決定木のライブラリをインポートして下さい。
"""

from sklearn import tree

"""#### 4.2 説明変数と目的変数を分けて、それぞれ「X」,「y」と言う変数名に格納し、カラム名を確認して下さい。"""

x = d_titanic_data.drop('survived', axis=1)
y = d_titanic_data['survived']
print(x.shape)
print(y.shape)

"""#### 4.3 説明変数、目的変数をそれぞれ学習データと検証データを7:3の割合で作成して下さい。変数名はX_train（説明変数の学習データ）, X_test（説明変数の検証データ）, y_train（目的変数の学習データ）, y_test（目的変数の検証データ）として下さい。その際インデックスのシャッフルはしないようにして、各変数の上5行を確認して下さい。"""

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.3, shuffle=False)
print(x_train.head())
print(x_test.head())
print(y_train.head())
print(y_test.head())

"""### 5. モデリング方法について学習します。（23問）

#### この章では、決定木モデルを例にして機械学習の一般的なフロー（パラメータチューニング、特徴量の追加、評価指標）を学習します。（モデルを作成するときはrandom_state=0を指定してください。）

#### 5.1 分類木を読み込んで、decision_treeと言う名前を付け、引数random_stateのみ「0」を指定し、下記のような決定木のパラメータ値を出力してください。※random_stateに数字を入れることで、結果を固定することができます。
"""

decision_tree = tree.DecisionTreeClassifier(random_state=0)
decision_tree

"""#### 5.2 fit関数を使い、学習データを使用して決定木を作成して下さい。※ここが「学習」と呼ばれる処理になります。"""

decision_tree =decision_tree.fit(x_train, y_train)
decision_tree

"""#### 5.3 「5.2」で決定木は作成できました。作成した決定木を用いて、新規データ（X_test）に対する予測値を出力してください。※ここが「予測」と呼ばれる処理になります。"""

y_pred = decision_tree.predict(x_test)
y_pred

"""#### 5.4 精度を確認していきましょう。学習データに使用しなかった「目的変数の検証データ（y_test）」を使用して、正解率を算出してください。"""

print(accuracy_score(y_test, y_pred))

"""#### 5.5 今回の結果の混合行列を出力してください。"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

"""#### 5.6 正解率は算出できましたが、まだまだ向上の余地がありそうです。「max_depth」を「4」に設定して正解率を算出し直しましょう。"""

decision_tree = tree.DecisionTreeClassifier(max_depth=4, random_state=0)
decision_tree = decision_tree.fit(x_train, y_train)
y_pred = decision_tree.predict(x_test)
print(accuracy_score(y_test, y_pred))

"""#### 5.7 やや正解率が向上したようです。混合行列も確認してみましょう。"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

"""#### 5.8 様々なパラメータを試す余地がありそうです。2～6までの順続きのリストを作成し、「min_samples_split_list」と名前を付けて下さい。"""

min_samples_split_list = range (2,7)
print(min_samples_split_list)

"""#### 5.9 for文を使用し、「5.8」で作成したリストの要素分、「min_samples_split」を試して下さい。※「min_samples_split」とは、分岐に必要な最小サンプル数のことです。過学習を抑制するために使用されます。"""

for min_samples_split in min_samples_split_list:
    decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split,random_state=0)
    decision_tree.fit(x_train, y_train)
    y_pred = decision_tree.predict(x_test)
    print(min_samples_split,accuracy_score(y_test, y_pred))

"""#### 5.10 大きな効果は確認できませんでした。他のパラメータも試してみましょう。0～0.1まで、0.02刻みのリストを作成し、「min_impurity_decrease_list」と名前を付けて下さい。"""

min_impurity_decrease_list = np.arange(0, 0.1, 0.02)
print(min_impurity_decrease_list)

"""#### 5.11 for文を使用し、「5.10」で作成したリストの要素分、「min_impurity_decrease」を試して下さい。※「min_impurity_decrease」とは、分岐をどこで止めるかの判断指標です。大きな値にすると、過学習が抑制されます。"""

for min_impurity_decrease in min_impurity_decrease_list:
     decision_tree = tree.DecisionTreeClassifier(min_impurity_decrease=min_impurity_decrease, random_state=0)
     decision_tree.fit(x_train, y_train)
     y_pred = decision_tree.predict(x_test)
     print(min_impurity_decrease, accuracy_score(y_test, y_pred))

"""#### 5.12 正解率は「min_impurity_decrease」が0.06以上で向上していることが確認できますが、本当にこれで大丈夫でしょうか。混合行列を確認してきましょう。"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

"""#### 5.13 全ての人に対し「0＝死亡」と予測してしまっているようです。正解率ではなく他の指標も確認してきましょう。適合率を算出して下さい。※適合率は生存と予測された人間のうち正解した人間の割合のことです。"""

from sklearn.metrics import precision_score
print(precision_score(y_test, y_pred))

"""#### 5.14 再現率を算出して下さい。※再現率は生存した人間のうち正解した人間の割合のことです。"""

from sklearn.metrics import recall_score
print(recall_score(y_test, y_pred))

"""#### 5.15 F値を算出して下さい。※F値（F1-measure）は適合率と再現率の調和平均のことです。"""

from sklearn.metrics import f1_score
print(f1_score(y_test, y_pred))

"""#### 5.16 生存していた人を評価する指標だと軒並み「0」になってしまうことが確認できました。正解率は分かりやすい指標ですが、今回のように「生存」と「死亡」の割合に差があるケースだと、間違った示唆を生み出してしまう可能性があります。それでは、「5.9」と「5.11」のリストの組み合わせ分、F値を算出して下さい。"""

for min_samples_split in min_samples_split_list:
     for min_impurity_decrease in min_impurity_decrease_list:
         decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease, random_state=0)
         decision_tree.fit(x_train, y_train)
         y_pred = decision_tree.predict(x_test)
         print(min_samples_split, min_impurity_decrease,f1_score(y_test, y_pred))

"""#### 5.17 「min_samples_split＝5」、「min_impurity_decrease=0.0」が一番F値が高いです。もう少しパラメータチューニングの幅を広げてみましょう。「min_samples_split＝5から10まで1刻み」、「min_impurity_decrease=0から0.02まで0.005刻み」のリストの組み合わせを試し、ベストのF値とその時に使用したパラメータを出力して下さい。"""

best_score = 0

min_samples_split_list = range(5,11)
min_impurity_decrease_list = np.arange(0, 0.025, 0.005)

for min_samples_split in min_samples_split_list:
     for min_impurity_decrease in min_impurity_decrease_list:
         decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease, random_state=0)
         decision_tree.fit(x_train, y_train)
         y_pred = decision_tree.predict(x_test)
         score = f1_score(y_test, y_pred)
         if score > best_score:
             best_score = score
             best_parameters = {'min_samples_split':min_samples_split, 'min_impurity_decrease':min_impurity_decrease, 'beat_score':best_score}
print(best_parameters)

"""#### 5.18 パラメータをうまく設定することで精度が向上することが分かりました。様々なパラメータを試すことで、データに合ったモデルを作成することができます。次は、特徴量の観点でも考えてみましょう。「3.8」,「3.9」より「body」はあまり良い情報を持っていないことが確認できます。この変数を削除してみて下さい。"""

x_train.drop('body', axis=1, inplace=True)
x_test.drop('body', axis=1, inplace=True)
print("x_train:",x_train.columns)
print("x_test:",x_test.columns)

"""#### 5.19 「5.17」の処理を回して、ベストスコアを確認して下さい。"""

best_score = 0

min_samples_split_list = range(5,11)
min_impurity_decrease_list = np.arange(0, 0.025, 0.005)

for min_samples_split in min_samples_split_list:
     for min_impurity_decrease in min_impurity_decrease_list:
         decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease, random_state=0)
         decision_tree.fit(x_train, y_train)
         y_pred = decision_tree.predict(x_test)
         score = f1_score(y_test, y_pred)
         if score > best_score:
             best_score = score
             best_parameters = {'min_samples_split':min_samples_split, 'min_impurity_decrease':min_impurity_decrease, 'beat_score':best_score}
print(best_parameters)

"""#### 5.20 変数追加も考えてみましょう。カテゴリデータの「sex」に関して下記グラフを作成して下さい。"""

cross_tab_tmp = pd.crosstab(titanic_data['sex'], d_titanic_data["survived"])
cross_tab_tmp.plot.bar(stacked=True)

"""#### 5.21 「sex」の変数は予測に寄与する可能性がありそうです。X_trainとX_testの変数にtitanic_dataからsexを追加して下さい。インデックスを変えないように注意して下さい。"""

x_train['sex'] = titanic_data['sex'][:914]
x_test['sex'] = titanic_data['sex'][915:]
print("x_train:", x_train.columns)
print("x_test:", x_test.columns)

"""#### 5.22 「sex」はカテゴリ変数なので、maleを0、femaleを1に変更し、数字に変わっていることを確認して下さい。"""

x_train['sex'] = np.where(x_train['sex']=='female',1,0)
x_test['sex'] = np.where(x_test['sex']=='female',1,0)
print(x_train['sex'].head())
print(x_test['sex'].head())

"""#### 5.23「5.17」の処理を回して、ベストスコアを確認して下さい。"""

best_score = 0

min_samples_split_list = range(5,11)
min_impurity_decrease_list = np.arange(0, 0.025, 0.005)

for min_samples_split in min_samples_split_list:
     for min_impurity_decrease in min_impurity_decrease_list:
         decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease, random_state=0)
         decision_tree.fit(x_train, y_train)
         y_pred = decision_tree.predict(x_test)
         score = f1_score(y_test, y_pred)
         if score > best_score:
             best_score = score
             best_parameters = {'min_samples_split':min_samples_split, 'min_impurity_decrease':min_impurity_decrease, 'beat_score':best_score}
print(best_parameters)

"""### 6. ロジスティック回帰の方法について学習します。（8問）

#### モデルを作成するときはrandom_state=0を指定してください。

#### 6.1 ロジスティック回帰のライブラリをインストールして下さい。
"""

from sklearn.linear_model import LogisticRegression

"""#### 6.2 ロジスティック回帰を読み込んで、「logistic_regression」と言う変数名に設定して下さい。その上で引数random_stateのみ「0」を指定し、下記のようなロジスティック回帰のパラメータ値を出力してください。※random_stateに数字を入れることで、結果を固定することができます。"""

logistic_regression = LogisticRegression(random_state=0)
logistic_regression

"""#### 6.3 fit関数を使い、学習データを使用して、ロジスティック回帰の学習を行って下さい。"""

logistic_regression = logistic_regression.fit(x_train, y_train)
logistic_regression

"""#### 6.4 作成したモデルを用いて、新規データ（X_test）に対する予測値を出力してください。※ここが「予測」と呼ばれる処理になります。"""

y_pred = logistic_regression.predict(x_test)
y_pred

"""#### 6.5 混合行列を算出して下さい。"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

"""#### 6.6 F値を算出して下さい。"""

from sklearn.metrics import f1_score
print(f1_score(y_test, y_pred))

"""#### 6.7 ロジスティック回帰の主要パラメータである正則化項を変更してみましょう。下記の様なリストを作成し、C_listと言う変数名に格納して下さい。"""

C_list =[10**i for i in range(-5, 6)]
C_list

"""#### 6.8 C_listの各値をパラメーター「C」に設定した際の精度を全て確認して下さい。"""

for C in C_list:
     logistic_regression = LogisticRegression(random_state=0,C=C)
     logistic_regression.fit(x_train, y_train)
     y_pred = logistic_regression.predict(x_test)
     print(C,f1_score(y_test, y_pred))

"""### 7. ランダムフォレストの方法について学習します。（16問）

#### ランダムフォレストは機械学習のアルゴリズムのひとつで、決定木を統合させて汎化能力を向上させる、アンサンブル学習アルゴリズムです。分類（判別）・回帰（予測）どちらも使用することができます。アンサンブル学習は精度が高くなる傾向にあります。（モデルを作成するときはrandom_state=0を指定してください。）

#### 7.1 ランダムフォレスト（分類木）のライブラリをインストールして下さい。
"""

from sklearn.ensemble import RandomForestClassifier

"""#### 7.2 ランダムフォレストを読み込んで、「random_forest」と言う変数名に設定して下さい。その上で引数random_stateのみ「0」を指定し、下記のようなランダムフォレストのパラメータ値を出力してください。※random_stateに数字を入れることで、結果を固定することができます。"""

random_forest = RandomForestClassifier(random_state=0)
random_forest

"""#### 7.3 fit関数を使い、学習データを使用して、ランダムフォレストの学習を行って下さい。"""

random_forest = random_forest.fit(x_train, y_train)
random_forest

"""#### 7.4 作成したモデルを用いて、新規データ（X_test）に対する予測値を出力してください。※ここが「予測」と呼ばれる処理になります。"""

y_pred = random_forest.predict(x_test)
y_pred

"""#### 7.5 混合行列を算出して下さい。"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

"""#### 7.6 F値を算出して下さい。"""

from sklearn.metrics import f1_score
print(f1_score(y_test, y_pred))

"""#### 7.7 デフォルト設定だとF値があまり良くないです。ランダムフォレストの主要パラメータであるn_estimotrs（木の数）、max_depth（木の深さ）、max_features（分岐に用いる説明変数の数を設定）を変更して見ましょう。下記のようなリストを作成して下さい。"""

n_estimators_list = [5,10,100,300]
print(n_estimators_list)
max_depth_list = [2,3,4]
print(max_depth_list)
max_feature_list = [2,3,5]
print(max_feature_list)

"""#### 7.8 上記リストの組み合わせをパラメータとして設定し、ベストパラメータとその時のF値を算出して下さい。"""

best_score = 0

for n_estimators in n_estimators_list:
     for max_depth in max_depth_list:
         for max_features in max_feature_list:
             random_forest = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, max_features=max_features, random_state=0)
             random_forest.fit(x_train, y_train)
             y_pred = random_forest.predict(x_test)
             score = f1_score(y_test, y_pred)
             if score > best_score:
                 best_score = score
                 best_parameters = {'n_estimators':n_estimators, 'max_depth':max_depth, 'max_features':max_features, 'best_score':best_score}
print(best_parameters)

"""#### 7.9 「7.8」の結果の通りランダムフォレストの様な「アンサンブル学習」はパラメータを確りチューニングする必要がありますが、精度が高くなる傾向にあります。最後にベストパラメータ時の変数需要度を算出して下さい。"""

random_forest = RandomForestClassifier(n_estimators=10, max_depth=3, max_features=2, random_state=0)
random_forest.fit(x_train, y_train)
features = x_train.columns
importances = random_forest.feature_importances_
indices = np.argsort(importances)
plt.barh(range(len(indices)), importances[indices])
plt.yticks(range(len(indices)), features[indices])
plt.show()

"""#### 7.10 目的変数が量的変数の場合（回帰）を確認していきましょう。目的変数を「fare」に変更し、説明変数から削除して下さい。「age」,「sibsp」,「parch」,「sex」から「fare」を予測するモデルを作成することになります。"""

y_train = x_train['fare']
y_test = x_test['fare']
x_train.drop('fare',axis=1,inplace=True)
x_test.drop('fare',axis=1,inplace=True)
print('x_train:',x_train.columns)
print('x_test:',x_test.columns)
print('y_train:',y_train.head())
print('y_test:',y_test.head())

"""#### 7.11 ランダムフォレスト（回帰木）のライブラリをインストールして下さい。"""

from sklearn.ensemble import RandomForestRegressor

"""#### 7.12 ランダムフォレスト（回帰木）を読み込んで、「random_forest」と言う変数名に設定して下さい。その上で引数random_stateのみ「0」を指定し、下記のようなランダムフォレストのパラメータ値を出力してください。※random_stateに数字を入れることで、結果を固定することができます。"""

random_forest = RandomForestRegressor(random_state=0)
random_forest

"""#### 7.13 fit関数を使い、学習データを使用して、ランダムフォレストの学習を行って下さい。"""

random_forest = random_forest.fit(x_train, y_train)
random_forest

"""#### 7.14 作成したモデルを用いて、新規データ（X_test）に対する予測値を出力（上から50行）してください。※ここが「予測」と呼ばれる処理になります。"""

y_pred = random_forest.predict(x_test)
y_pred[:50]

"""#### 7.15 実測値と予測値の平均絶対誤差を出力して下さい。"""

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_pred, y_test)

"""#### 7.16 実測値と予測値の散布図を下記の形で出力して下さい。"""

plt.scatter(y_pred, y_test)
plt.title('Scatter Plot of Predict vs Test')
plt.xlabel('Pred')
plt.ylabel('Test')
plt.grid()
plt.show()

"""### 8. K-meansの方法について学習します。（15問）

#### K-means法は、非階層型クラスタリングのアルゴリズムです。クラスタの平均を用い、与えられたクラスタ数k個に分類することから、K-means法と呼ばれています。（モデルを作成するときはrandom_state=0を指定してください。）

#### 8.1 Kmeansを読み込んで下さい。
"""

from sklearn.cluster import KMeans

"""#### 8.2 object型データを削除して、上から5行出力して下さい。"""

titanic_data_except_object = titanic_data.select_dtypes(['int64', 'float64'])
titanic_data_except_object.head()

"""#### 8.3 全ての欠損値に0を埋めて下さい。欠損値がなくなったことを確認して下さい。"""

titanic_data_except_object = titanic_data_except_object.fillna(0)
titanic_data_except_object.isnull().sum()

"""#### 8.4 random_state=0を指定して、Kmeans法を実行して下さい。"""

kmeans_model = KMeans(n_clusters=4, random_state=0).fit(titanic_data_except_object)
kmeans_model

"""#### 8.5 分類結果を上から50人確認して下さい。"""

labels = kmeans_model.labels_
labels[0:50]

"""#### 8.6 cluster列を作成し、クラスタリング結果を格納して下さい。"""

titanic_data_except_object['cluster'] = labels
titanic_add_cluster = titanic_data_except_object
titanic_add_cluster.head()

"""#### 8.7 クラスタリング結果を確認していきましょう。それぞれのグループのサンプル数を出力して下さい。"""

titanic_add_cluster['cluster'].value_counts()

"""#### 8.8 グループ毎に各カラムの値の平均値を出力して下さい。"""

titanic_add_cluster.groupby('cluster').mean()

"""#### 8.9 「body」,「fare」,「survived」が特に分類に寄与しているようです。2次元プロットで可視化してみましょう。主成分分析のライブラリを読み込んで下さい。"""

from sklearn.decomposition import PCA

"""#### 8.10　PCAを読み込んで、「pca」と言う変数名に設定して下さい。その上で引数random_stateのみ「0」を指定し、下記のようなpcaのパラメータ値を出力してください。※random_stateに数字を入れることで、結果を固定することができます。"""

pca = PCA(random_state=0)
pca

"""#### 8.11 主成分分析を実行して下さい。"""

pca.fit(titanic_add_cluster)

"""#### 8.12 次元削減を実行し、featureと言う変数に格納して下さい。"""

feature = pca.transform(titanic_add_cluster)
feature

"""#### 8.13 1行目の主成分分析結果を出力して下さい。"""

feature[0,:]

"""#### 8.14 主成分分析を可視化します。各ラベルに{0:'#00FF00', 1:'#FF0000', 2:'#0000FF',  3:'#ffff00'}の色を付けて、リストを作成し、colorsと言う変数に格納して下さい。確認の為上から50行表示して下さい。"""

color_codes = {0:'#00ff00', 1:'#ff0000', 2:'#0000ff', 3:'#ffff00'}
colors = [color_codes[x] for x in labels]
colors[:50]

"""#### 8.15 第一主成分と第二主成分を下記のようにグループごとに色分けして出力して下さい。"""

plt.figure(figsize=(6, 6))
plt.scatter(feature[:, 0], feature[:, 1], color=colors)
plt.title('Principal Component Analysis')
plt.xlabel('First principal component')
plt.ylabel('Second principal component')
plt.show()
