from fastapi import UploadFile
from typing import List
import instructor
from litellm import acompletion
from llama_cloud_services import LlamaParse
import pandas as pd

from app.models import ScoreResponse


class ResumeService:
    @staticmethod
    async def score_resumes(criteria: list[str], files: List[UploadFile]) -> str:
        client = instructor.from_litellm(acompletion)

        df = pd.DataFrame(columns=["Candidate Name"] + criteria + ["Total Score"])
        for file in files:
            file_data = file.file.read()
            parser = LlamaParse(result_type="markdown")

            documents = parser.load_data(file_data, {"file_name": file.filename})
            resume_content = "".join(document.text for document in documents)

            evaluation = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert resume reviewer. You will be provided with a list of criteria for a job application and a resume. You have to evaluate the resume and provide a score out of 10 foor each of the criteria. Also, return the candidate's name from the resume.

                        Return the structured JSON response as below -
                        {{
                            candidate_name: "John Doe",
                            score_criteria: [
                                "Must have certification XYZ",
                                "5+ years of experience in Python development",
                                "Strong background in Machine Learning",
                            ],
                            score_values: [
                                4,5,9
                            ],
                            reasoning: [
                                "The candidate has certification in ABC, which is somewhat related to XYZ, thus a score of 4",
                                "The candidate only has 2.5 years of experience in Python development,thus a score of 5",
                                "The candidate has very strong hands-on machine learning experience at startups, thus a score of 9.",
                            ]
                        }}
                        DO NOT USE FUNCTION/TOOL CALLING. ONLY ANSWER WITH YOUR AVAILABLE INFORMATION.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""The criteria list is {criteria} and the resume content is {resume_content}
                        """,
                    },
                ],
                max_retries=0,
                max_tokens=1024,
                response_model=ScoreResponse,
            )

            scores = dict(zip(evaluation.score_criteria, evaluation.score_values))
            row_data = {
                "Candidate Name": evaluation.candidate_name,
                **scores,
                "Total Score": sum(evaluation.score_values),
            }
            df.loc[len(df)] = row_data

        return df
