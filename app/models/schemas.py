from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TimeHorizon(str, Enum):
    SHORT = "short_term"
    MEDIUM = "medium_term"
    LONG = "long_term"


class EnvironmentalInput(BaseModel):
    soil_organic_carbon_pct: Optional[float] = Field(default=None, ge=0, le=100)
    soil_ph: Optional[float] = Field(default=None, ge=0, le=14)
    soil_moisture: Optional[str] = None
    rainfall: Optional[str] = None
    land_use_type: Optional[str] = None
    region_type: Optional[str] = None
    temperature_c: Optional[float] = Field(default=None, ge=-90, le=70)
    species_richness: Optional[str] = None
    deforestation_present: Optional[bool] = None
    pollution_present: Optional[bool] = None
    # Coordinates are retained for API compatibility, but are not presented
    # as spatial reasoning until a geospatial dataset is added.
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)

    def missing_required_fields(self) -> list[str]:
        required = {
            "soil_organic_carbon_pct": self.soil_organic_carbon_pct,
            "rainfall": self.rainfall,
            "land_use_type": self.land_use_type,
            "region_type": self.region_type,
        }
        return [name for name, value in required.items() if value is None]


class Recommendation(BaseModel):
    relationship_id: str
    action: str
    mechanism: str
    impacted_metrics: list[str]
    estimated_effect: Optional[str] = None
    time_horizon: TimeHorizon
    confidence: Optional[str] = None
    source: str


class ChatResponse(BaseModel):
    message: str
    clarifying_question: Optional[str] = None
    recommendations: list[Recommendation] = Field(default_factory=list)
