from pydantic import BaseModel

from backend.app.schemas.risk_zone import RiskZoneRead
from backend.app.schemas.village import VillageRead
from backend.app.schemas.road_segment import RoadSegmentRead
from backend.app.schemas.risk_assessment import RiskAssessmentRead


class GISMapDataRead(BaseModel):
    risk_zone: RiskZoneRead
    latest_risk_assessment: RiskAssessmentRead | None = None
    villages: list[VillageRead]
    road_segments: list[RoadSegmentRead]

    village_count: int
    road_segment_count: int
    blocked_road_count: int
