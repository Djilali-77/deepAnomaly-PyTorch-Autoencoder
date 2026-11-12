import torch
import torch.nn as nn
import torch.optim as optim

def train_autoencoder(model: nn.Module, dataloader, epochs: int, learning_rate: float):

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    model.train()

    for epoch in range(epochs):
        epoch_loss = 0.0

        for batch in dataloader:
            
            optimizer.zero_grad()
            reconstructed_x = model(batch)
            loss = criterion(reconstructed_x, batch)   
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss / len(dataloader):.6f}")

    return model