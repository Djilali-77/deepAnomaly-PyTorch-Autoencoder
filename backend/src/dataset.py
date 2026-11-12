import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class UNSWDataset(Dataset):
    def __init__(self, data_array: np.ndarray):

        self.data = torch.tensor(data_array, dtype=torch.float32)

    def __len__(self):

        return self.data.shape[0]  

    def __getitem__(self, idx):

        return self.data[idx]

def create_dataloader(data_array: np.ndarray, batch_size: int, shuffle: bool = True) -> DataLoader:

    unsdataset = UNSWDataset(data_array)
    data = DataLoader(
        dataset=unsdataset,
        batch_size=batch_size,
        shuffle=shuffle,
    )
    return data