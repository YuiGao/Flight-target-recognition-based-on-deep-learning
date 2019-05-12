import matplotlib.pyplot as plt
def show_train_history(train_history,train,validation,title):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title(title)
    plt.xlabel("Epoch")
    plt.ylabel(train)
    plt.legend(["train","validation"],loc="upper left")
    plt.show()