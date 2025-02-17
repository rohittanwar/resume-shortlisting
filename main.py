import json
import os
from typing import List
from fastapi import FastAPI, File, Form, Response, UploadFile
from fastapi.responses import FileResponse
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader

from app.criteria_service import CriteriaService
from app.models import CriteriaResponse
from app.resume_service import ResumeService
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()

app = FastAPI(
    title="Resume shortlisting app",
    description="",
    version="1.0.0",
)

load_dotenv()


@app.post(
    "/extract-criteria",
    response_model=CriteriaResponse,
    summary="Extract criteria from job description",
    description="Upload a job description PDF and get extracted criteria",
)
async def extract_criteria(
    file: UploadFile = File(..., description="Job description PDF or DOCX file"),
):
    criteria = await CriteriaService.extract_criteria(file)
    return {"criteria": criteria}


@app.post(
    "/score-resumes",
    summary="Score resumes against criteria",
    description="Upload multiple resumes and get scoring results in Excel format",
    response_description="CSV data containing resume scores for each candidate",
)
async def score_resumes(
    criteria: str = Form(..., description="List of criteria to score against"),
    files: List[UploadFile] = File(..., description="List of resume files (PDF/DOCX)"),
):
    criterias = json.loads(criteria)
    df = await ResumeService.score_resumes(criterias, files)
    csv_data = df.to_csv(index=False)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="data.csv"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
