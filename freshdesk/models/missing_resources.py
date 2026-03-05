from typing import List, Optional, Any, Dict
from datetime import datetime

from .base import FreshdeskModel

class ChannelAvailability(FreshdeskModel):
    category: str
    availability_status: str
    availability_updated_at: datetime

class AgentAvailability(FreshdeskModel):
    agent_id: int
    availability_status: str
    channel_availability: List[ChannelAvailability] = []
    availability_updated_at: datetime
    availability_control: str

class AdminGroup(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    type: str
    created_at: datetime
    updated_at: datetime
    agent_ids: List[int] = []
    allow_agents_to_change_availability: bool = False

class OmnichannelActivity(FreshdeskModel):
    id: Optional[str] = None
    description: str
    link: Optional[str] = None
    actor: Dict[str, Any]
    source: Dict[str, Any]
    object: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    contact: Dict[str, Any]
    created_at: Optional[datetime] = None

class ServiceTask(FreshdeskModel):
    id: int
    status: int
    type_id: int
    ticket_id: int
    created_at: datetime
    updated_at: datetime

class ServiceGroup(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
class FieldTechnician(FreshdeskModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
