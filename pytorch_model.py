import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from ml_pipeline import train_baselines

class PhysicsNet(nn.Module):
    def __init__(self):
        super(PhysicsNet, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),           
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 4)     
        )

    def forward(self, x):
        return self.network(x)

def prepare_tensors():
   
    print("Fetching data from ML Pipeline...")
    scaler, X_train, X_test, y_train, y_test = train_baselines()
    
   
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train.values)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test.values)
    
   
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    return train_loader, X_test_tensor, y_test_tensor


def train_model():

    train_loader, X_test_tensor, y_test_tensor = prepare_tensors()
    

    model = PhysicsNet()
    criterion = nn.MSELoss() 
    optimizer = optim.Adam(model.parameters(), lr=0.001) 
    
    epochs = 50 
    
    print("\nStarting Neural Network Training...")
    
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()            
            
            predictions = model(batch_X)     
            loss = criterion(predictions, batch_y) 
            
            loss.backward()                 
            optimizer.step()                
            
            epoch_loss += loss.item()
            
        
        if (epoch + 1) % 10 == 0:
            avg_loss = epoch_loss / len(train_loader)
            print(f"Epoch {epoch+1}/{epochs} | Training MSE: {avg_loss:.4f}")
            
    
    print("\nTaking the Final Exam (Testing on the 10,000 unseen collisions)...")
    model.eval() 
    
    with torch.no_grad():
        test_predictions = model(X_test_tensor)
        test_loss = criterion(test_predictions, y_test_tensor)
        
    print(f"Neural Network Final Test MSE: {test_loss.item():.4f}")
    
    return model

if __name__ == "__main__":
    trained_model = train_model()
    torch.save(trained_model.state_dict(), "physics_model.pth")
    print("Model saved successfully as physics_model.pth!")