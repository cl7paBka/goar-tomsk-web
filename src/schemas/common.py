from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
