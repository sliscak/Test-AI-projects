import torch
from torch import nn

class Net(nn.Module):
    def __init__(self, infeatures:int, capacity:int):
        super(Net, self).__init__()
        self.memory = nn.ParameterList([nn.Parameter(torch.rand(infeatures)) for i in range(capacity)])

    def forward(self, x):
        distances = torch.tensor([])
        for i in range(len(self.memory)):
            distance = torch.cosine_similarity(x, self.memory[i], dim=0)
            # print(distance)
            # print(distances)
            distances = torch.cat((distances, torch.unsqueeze(distance, dim=0)), dim=0)
        return distances

class Net2(nn.Module):
    def __init__(self, infeatures:int, capacity:int):
        super(Net2, self).__init__()
        self.memory = nn.ParameterList([nn.Parameter(torch.rand(infeatures)) for i in range(capacity)])

    def forward(self, x):
        distances = torch.tensor([])
        for i in range(len(self.memory)):
            distance = torch.cosine_similarity(x, self.memory[i], dim=0)
            # print(distance)
            # print(distances)
            distances = torch.cat((distances, torch.unsqueeze(distance, dim=0)), dim=0)
        attention = torch.softmax(distances, dim=0)
        return attention

class Net3(nn.Module):
    def __init__(self, infeatures:int, capacity:int):
        super(Net3, self).__init__()
        self.memory = nn.ParameterList([nn.Parameter(torch.rand(infeatures)) for i in range(capacity)])

    def forward(self, x):
        distances = torch.tensor([])
        for i in range(len(self.memory)):
            distance = torch.cosine_similarity(x, self.memory[i], dim=0)
            # print(distance)
            # print(distances)
            distances = torch.cat((distances, torch.unsqueeze(distance, dim=0)), dim=0)
        amax = torch.amax(distances, dim=0)
        mask = torch.zeros(distances, dtype=torch.double)
        mask[amax] = 1
        out = distances * mask
        return out