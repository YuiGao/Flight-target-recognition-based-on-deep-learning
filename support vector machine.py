import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns;sns.set()
from sklearn.svm import SVC
from sklearn.datasets.samples_generator import make_blobs
from View import data_pca
from read_data import get_data_label
def plot_svc_decision_function(model,ax=None,plot_support=True):
    '''画二维SVC的决策函数'''
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    #创建评估模型的网络
    x = np.linspace(xlim[0],xlim[1],30)
    y = np.linspace(ylim[0],ylim[1],30)
    Y,X = np.meshgrid(y,x)
    xy = np.vstack([X.ravel(),Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)
    #画决策边界和边界
    ax.contour(X,Y,P,colors='k',levels=[-1,0,1],alpha=0.5,linestyles=['--','-','--'])
    #画支持向量
    if plot_support:
        ax.scatter(model.support_vectors_[:,0],model.support_vectors_[:,1],
                   s=300,linewidth=1,facecolors='none');
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        plt.show()


#data,label = get_data_label()
#data_3d = data_pca(data,3)
#data_2d = data_pca(data,2)
label_2d = np.concatenate((np.array([0]*100),np.array([1]*100)),axis=0)
X,y = make_blobs(n_samples=50,centers=2,random_state=0,cluster_std=0.60)
model = SVC(kernel="linear",C=1E10)
model.fit(X,y)
plt.scatter(X[:,0],X[:,1],c=y,s=50,cmap='autumn')
plot_svc_decision_function(model)

