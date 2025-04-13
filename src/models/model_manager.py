from typing import Optional, Dict, Any
import torch
from pathlib import Path
import json
import logging

class ModelManager:
    def __init__(self, storage_path: str = "models/", device: str = None):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Set device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        self.logger.info(f"Using device: {self.device}")

    def save_model(self, model: torch.nn.Module, model_name: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        try:
            model_path = self.storage_path / model_name
            model_path.mkdir(exist_ok=True)
            
            # Move model to CPU before saving
            model = model.to("cpu")
            
            # Save model weights
            torch.save(model.state_dict(), model_path / "weights.pt")
            
            # Save metadata
            if metadata:
                metadata["device"] = str(self.device)
                with open(model_path / "metadata.json", "w") as f:
                    json.dump(metadata, f)
            
            self.logger.info(f"Model {model_name} saved successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error saving model {model_name}: {str(e)}")
            return False

    def load_model(self, model_name: str, model_class: torch.nn.Module) -> Optional[torch.nn.Module]:
        try:
            model_path = self.storage_path / model_name
            if not model_path.exists():
                self.logger.error(f"Model {model_name} not found")
                return None
            
            # Load model weights
            model = model_class()
            model.load_state_dict(torch.load(model_path / "weights.pt"))
            
            # Move model to specified device
            model = model.to(self.device)
            
            self.logger.info(f"Model {model_name} loaded successfully to {self.device}")
            return model
        except Exception as e:
            self.logger.error(f"Error loading model {model_name}: {str(e)}")
            return None

    def get_model_metadata(self, model_name: str) -> Optional[Dict[str, Any]]:
        try:
            metadata_path = self.storage_path / model_name / "metadata.json"
            if not metadata_path.exists():
                return None
            
            with open(metadata_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading metadata for model {model_name}: {str(e)}")
            return None

    def list_models(self) -> list:
        try:
            return [d.name for d in self.storage_path.iterdir() if d.is_dir()]
        except Exception as e:
            self.logger.error(f"Error listing models: {str(e)}")
            return [] 