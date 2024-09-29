import importlib
from pydantic import BaseModel

from src.common.dto.user import CustomerFilter, CustomerCreate, CustomerID
from src.common.dto.order import CreateOrderWithCustomerData


def rebuild_models() -> None:
    module = importlib.import_module(__name__)
    for model_name in set(__all__):
        model = getattr(module, model_name, None)
        if model and issubclass(model, BaseModel):
            model.model_rebuild()


__all__ = (
    "CustomerFilter",
    "CustomerCreate",
    "CustomerID",
    "CreateOrderWithCustomerData",
)

rebuild_models()
