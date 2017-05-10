import pandas as pd

from sklearn.decomposition import PCA
from sklearn.feature_selection import chi2
from sklearn.metrics import mean_absolute_error, explained_variance_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SelectKBest
from sklearn.svm import SVC


class Predictifier():
    def __init__(self, config):
        self.config = config
        self.regressor = LinearRegression()

    def predict(self, charAsFloatArray):
        dataset = pd.read_csv('testdata/data.csv')
        X = dataset.iloc[:, 5:].values
        y = dataset.iloc[:, 0].values

        # Encoding categorical data
        # Encoding the Dependent Variable
        labelencoder_y = LabelEncoder()
        y = labelencoder_y.fit_transform(y)

        # feature extraction
        pca = PCA(n_components=1)
        skb = SelectKBest(score_func=chi2, k=1)
        featureUnion = FeatureUnion([('pca', pca), ('skb', skb)])
        fit = featureUnion.fit(X, y)

        # summarize scores
        y = fit.transform(X)

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Feature Scaling
        sc_X = StandardScaler()
        X_train = sc_X.fit_transform(X_train)
        X_test = sc_X.transform(X_test)

        # Linear Regression
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        y_pred = regressor.predict(X_test)
        print y_pred.shape

        print(mean_absolute_error(y_test, y_pred))
        print(explained_variance_score(y_test, y_pred))
        print(mean_squared_error(y_test, y_pred))
        print(r2_score(y_test, y_pred))

    def nastyPredict(self, soundAsCharArrays):
        dataset = pd.read_csv('testdata/data.csv')
        X = dataset.iloc[:, 5:].values
        y = dataset.iloc[:, 0].values

        # Encoding categorical data
        # Encoding the Dependent Variable
        labelencoder_y = LabelEncoder()
        y = labelencoder_y.fit_transform(y)

        clf = SVC()
        clf.fit(X, y)

        yhat = clf.predict(soundAsCharArrays)
        print map(lambda x : labelencoder_y.inverse_transform(int(x)), yhat)

def tryIt():
    dataset = pd.read_csv('testdata/data.csv')
    X = dataset.iloc[:, 5:].values
    y = dataset.iloc[:, 0].values

    # Encoding categorical data
    # Encoding the Dependent Variable
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)

    # feature extraction
    pca = PCA(n_components=1)
    skb = SelectKBest(score_func=chi2, k=1)
    featureUnion = FeatureUnion([('pca', pca), ('skb', skb)])
    fit = featureUnion.fit(X, y)

    # summarize scores
    y = fit.transform(X)

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Feature Scaling
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)

    # Linear Regression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    y_pred = regressor.predict(X_test)
    print map(int, y_pred[0])

    # Compare with the builtin predict
    print(regressor.predict(X))

    print(mean_absolute_error(y_test, y_pred))
    print(explained_variance_score(y_test, y_pred))
    print(mean_squared_error(y_test, y_pred))
    print(r2_score(y_test, y_pred))

if __name__ == "__main__":
    tryIt()