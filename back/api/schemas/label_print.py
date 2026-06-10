from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LabelPrintRequest(BaseModel):
    lpn: str | None = None
    etq_id: str | None = Field(default=None, alias="etqId")
    zone: str | None = None
    requested_by: str | None = Field(default=None, alias="requestedBy")
    reprint_reason: str | None = Field(default=None, alias="reprintReason")

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def unwrap_legacy_request(cls, data: Any):
        if isinstance(data, dict) and "request" in data and isinstance(data["request"], dict):
            merged = dict(data["request"])
            for key, value in data.items():
                if key != "request":
                    merged[key] = value
            return merged
        return data

    @property
    def identifier(self) -> str:
        return self.lpn or self.etq_id or ""
