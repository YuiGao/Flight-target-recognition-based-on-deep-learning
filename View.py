import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import axes3d
from read_data import get_data_label
from sklearn import decomposition
from read_data import data_size
from sklearn.datasets import make_blobs
def dataset_plot_2d():
    data,label = make_blobs(100,2,centers=2,random_state=2,cluster_std=1.5)
    x = data[:,0]*1000
    y1 = (data[:,1][:50]+6)*1000
    y2 = data[:,1][50:]*1000
    y = np.concatenate((y1,y2),axis=0)
    sns.set()
    for i in range(len(x)//2):
        plt.scatter(x[i],y[i],c="r",marker="o",s=30)
        plt.scatter(x[i+50],y[i+50],c="g",marker="^",s=30)
    plt.title("CA-UAV_2D")
    plt.legend(["CA","UAV"], loc="upper left")
    plt.savefig("fig_2d.png",dpi=500)
    plt.show()
def dataset_plot_3d():
    data,label = make_blobs(100,2,centers=2,random_state=2,cluster_std=1.5)
    x = data[:,0]*1000
    y1 = (data[:,1][:50]+6)*1000
    y2 = data[:,1][50:]*1000
    y = np.concatenate((y1,y2),axis=0)
    np.random.seed(2)
    z =(0.5*np.random.randn(100))*5000
    sns.set()
    fig = plt.figure()
    ax = plt.gca(projection="3d")
    ax.set_title("CA-UAV_3D")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    for i in range(len(x)//2):
        ax.scatter(x[i],y[i],z[i],c="r",marker="o",s=30)
        ax.scatter(x[i+50],y[i+50],z[i],c="g",marker="^",s=30)
    plt.legend(["CA","UAV"], loc="upper left")
    plt.savefig("fig_3d.png",dpi=500)
    plt.show()

def data_pca(data,n_components):
    pca = decomposition.PCA(n_components=n_components)
    pca.fit(data)
    pca_data = pca.transform(data)
    return pca_data
def plot_3d(data):
    fig = plt.figure()
    ax = plt.gca(projection="3d")
    ax.set_title("3D_curve")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    num = data_size//2
    for i in range(num):
        ax.scatter(data[i][0],data[i][1],data[i][2],color="r")
        ax.scatter(data[i+num][0],data[i+num][1],data[i+num][2],color="g")
    plt.legend(["UAV","CA"], ncol=2, loc="upper left")
    plt.savefig("fig_3d.png")
    plt.show()

def plot_2d(data):
    fig = plt.figure()
    ax = plt.axes()
    ax.set_title("2D_curve")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    for i in range(100):
        ax.scatter(data[i][0],data[i][1], color="r")
        ax.scatter(data[i+100][0],data[i+100][1],color="g")
    plt.legend(["UAV","CA"], ncol=2, loc="upper left")
    plt.savefig("fig_2d.png")
    plt.show()
if __name__ == "__main__":
    dataset_plot_2d()
    dataset_plot_3d()