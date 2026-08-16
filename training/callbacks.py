"""
PyTorch Lightning callbacks for Siamese training.

Includes:
  - Model checkpointing
  - Early stopping
  - Learning rate logging
  - ONNX export callback
"""

# TODO: Implement in Phase 4


class OnnxExportCallback:
    """Export model to ONNX at end of training."""

    def __init__(self, output_path: str = "checkpoints/siamese.onnx", opset: int = 17):
        self.output_path = output_path
        self.opset = opset

    def on_train_end(self, trainer, model):
        # TODO: Export model to ONNX
        raise NotImplementedError
