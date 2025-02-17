from pydantic import BaseModel
from typing import Dict, List


class CriteriaResponse(BaseModel):
    criteria: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "criteria": [
                    "Must have certification XYZ",
                    "5+ years of experience in Python development",
                    "Strong background in Machine Learning",
                ]
            }
        }


class ScoreResponse(BaseModel):
    candidate_name: str
    score_criteria: list[str]
    score_values: list[int]
    reasoning: list[str]
