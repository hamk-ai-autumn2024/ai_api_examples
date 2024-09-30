from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
import json

class Athlete(BaseModel):
    last_name: str
    first_name: str
    nationality: str
    record_time: float

class AthleteFormat(BaseModel):
    athletes: list[Athlete]

main_model_schema = AthleteFormat.model_json_schema()  # (1)!
print(json.dumps(main_model_schema, indent=2))  # (2)!
