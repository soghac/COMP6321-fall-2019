import os
import numpy as np
import pickle
import torch
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from PIL import Image
from torch.utils.data import Dataset

def load_CIFAR10(root='././datasets/'):
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    train_set = torchvision.datasets.CIFAR10(root=root,
                                             train=True,
                                             download=False,
                                             transform=transform)
    train_loader = torch.utils.data.DataLoader(train_set,
                                               batch_size=4,
                                               shuffle=True,
                                               num_workers=2)
    test_set = torchvision.datasets.CIFAR10(root=root,
                                            train=False,
                                            download=False,
                                            transform=transform)
    test_loader = torch.utils.data.DataLoader(test_set,
                                              batch_size=4,
                                              shuffle=False,
                                              num_workers=2)
    return train_loader, test_loader

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def train(self, epoch_num=2, batch_size=2000):
        if os.path.isfile('models/cifar_10/trained_model/Lenet_parameters.pkl'):
            self.load_state_dict(torch.load('models/cifar_10/trained_model/Lenet_parameters.pkl'))
        for epoch in range(epoch_num):  # loop over the dataset multiple times
            running_loss = 0.0
            for i, data in enumerate(train_loader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                # zero the parameter gradients
                optimizer.zero_grad()
                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                # print statistics
                running_loss += loss.item()
                if i % batch_size == batch_size-1:    # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' %
                        (epoch + 1, i + 1, running_loss / batch_size))
                    running_loss = 0.0
        torch.save(self.state_dict(), 'models/cifar_10/trained_model/Lenet_parameters.pkl')
        print('Finished Training')

    def test(self):
        self.load_state_dict(torch.load('models/cifar_10/trained_model/Lenet_parameters.pkl'))
        correct = 0
        total = 0
        with torch.no_grad():
            for data in test_loader:
                images, labels = data
                outputs = net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print('Accuracy of the network on the 10000 test images: %.2f %%' % (
            100 * correct / total))

if __name__ == "__main__":
    net = Net()
    train_loader, test_loader = load_CIFAR10()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    # net.train()
    net.test()