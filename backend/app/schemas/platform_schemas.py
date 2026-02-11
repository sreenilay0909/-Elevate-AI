"""Schemas for platform data"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

def to_camel(string: str) -> str:
    """Convert snake_case to camelCase"""
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convert_dict_keys_to_camel(data: Any) -> Any:
    """Recursively convert all dictionary keys from snake_case to camelCase"""
    if isinstance(data, dict):
        return {to_camel(k): convert_dict_keys_to_camel(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_dict_keys_to_camel(item) for item in data]
    else:
        return data

class CamelModel(BaseModel):
    """Base model that converts snake_case to camelCase"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class PlatformDataResponse(CamelModel):
    """Response for platform data"""
    platform: str
    data: Dict[str, Any]
    last_updated: Optional[datetime] = None
    fetch_status: str = "success"
    error_message: Optional[str] = None

class FetchResponse(CamelModel):
    """Response for fetch operation"""
    platform: str
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    last_updated: Optional[datetime] = None

class FetchAllResponse(CamelModel):
    """Response for fetch all operation"""
    results: List[FetchResponse]
    total: int
    successful: int
    failed: int
