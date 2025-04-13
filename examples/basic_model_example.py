import torch
import torch.nn as nn
from src.models.model_manager import ModelManager

# Define a simple neural network
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 2)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def main():
    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Initialize model and model manager
    model = SimpleModel().to(device)  # Move model to GPU if available
    model_manager = ModelManager(device=device)
    
    # Create some dummy metadata
    metadata = {
        "name": "simple_model",
        "description": "A simple neural network example",
        "version": "1.0.0",
        "parameters": {
            "input_size": 10,
            "hidden_size": 5,
            "output_size": 2
        }
    }
    
    # Save the model
    success = model_manager.save_model(model, "simple_model", metadata)
    if success:
        print("Model saved successfully!")
    
    # List available models
    models = model_manager.list_models()
    print("Available models:", models)
    
    # Load the model
    loaded_model = model_manager.load_model("simple_model", SimpleModel)
    if loaded_model:
        print("Model loaded successfully!")
        
        # Test the loaded model
        test_input = torch.randn(1, 10).to(device)  # Move input to GPU if available
        output = loaded_model(test_input)
        print("Model output:", output)
        print("Output device:", output.device)

if __name__ == "__main__":
    main() 