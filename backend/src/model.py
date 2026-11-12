import torch
import torch.nn as nn

class DeepAnomalyAE(nn.Module):
    def __init__(self, input_dim: int):
        super(DeepAnomalyAE, self).__init__()
        
        # 1. Encoder Architecture
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU()        
        )
        
        # 2. Decoder Architecture
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):

        z = self.encoder(x)
        reconstructed_x = self.decoder(z)

        return reconstructed_x