import pytest
import torch
import torch.nn as nn
import os
import shutil
from pathlib import Path
from src.models.model_manager import ModelManager

# Test model class
class TestModel(nn.Module):
    def __init__(self):
        super(TestModel, self).__init__()
        self.fc = nn.Linear(5, 2)
    
    def forward(self, x):
        return self.fc(x)

@pytest.fixture
def model_manager(tmp_path):
    # Create a temporary directory for testing
    storage_path = tmp_path / "models"
    return ModelManager(storage_path=str(storage_path))

@pytest.fixture
def test_model():
    return TestModel()

@pytest.fixture
def test_metadata():
    return {
        "name": "test_model",
        "description": "Test model for unit testing",
        "version": "1.0.0",
        "parameters": {
            "input_size": 5,
            "output_size": 2
        }
    }

def test_model_save_load(model_manager, test_model, test_metadata):
    # Test saving model
    success = model_manager.save_model(test_model, "test_model", test_metadata)
    assert success, "Model save failed"
    
    # Test loading model
    loaded_model = model_manager.load_model("test_model", TestModel)
    assert loaded_model is not None, "Model load failed"
    
    # Verify model structure
    assert isinstance(loaded_model, TestModel)
    assert loaded_model.fc.in_features == 5
    assert loaded_model.fc.out_features == 2

def test_model_metadata(model_manager, test_model, test_metadata):
    # Save model with metadata
    model_manager.save_model(test_model, "test_model", test_metadata)
    
    # Get metadata
    loaded_metadata = model_manager.get_model_metadata("test_model")
    assert loaded_metadata is not None, "Failed to load metadata"
    
    # Verify metadata content
    assert loaded_metadata["name"] == test_metadata["name"]
    assert loaded_metadata["description"] == test_metadata["description"]
    assert loaded_metadata["version"] == test_metadata["version"]

def test_list_models(model_manager, test_model, test_metadata):
    # Save multiple models
    model_manager.save_model(test_model, "model1", test_metadata)
    model_manager.save_model(test_model, "model2", test_metadata)
    
    # List models
    models = model_manager.list_models()
    assert len(models) == 2, "Incorrect number of models listed"
    assert "model1" in models, "Model1 not found in list"
    assert "model2" in models, "Model2 not found in list"

def test_gpu_support(model_manager, test_model, test_metadata):
    # Test GPU availability
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Move model to device
    test_model = test_model.to(device)
    
    # Save and load model
    model_manager.save_model(test_model, "gpu_model", test_metadata)
    loaded_model = model_manager.load_model("gpu_model", TestModel)
    
    # Verify device
    assert loaded_model is not None
    for param in loaded_model.parameters():
        # Check if both devices are CUDA devices, regardless of index
        assert (param.device.type == device.type and 
                param.device.type == "cuda"), "Model not on correct device"

def test_invalid_model_operations(model_manager):
    # Test loading non-existent model
    loaded_model = model_manager.load_model("non_existent", TestModel)
    assert loaded_model is None, "Should return None for non-existent model"
    
    # Test getting metadata for non-existent model
    metadata = model_manager.get_model_metadata("non_existent")
    assert metadata is None, "Should return None for non-existent model metadata" 