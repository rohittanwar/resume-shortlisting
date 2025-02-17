from fastapi import UploadFile
import instructor
from litellm import acompletion, completion
import litellm
from llama_cloud_services import LlamaParse
from app.models import CriteriaResponse

litellm._turn_on_debug()


class CriteriaService:
    @staticmethod
    async def extract_criteria(file: UploadFile) -> list[str]:
        file_data = file.file.read()

        parser = LlamaParse(result_type="markdown")

        documents = parser.load_data(file_data, {"file_name": "jd.docx"})
        jd_content = "".join(document.text for document in documents)
        client = instructor.from_litellm(acompletion)
        criteria = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert document analyzer. You will be provided with content from a job description file and you have to extract key ranking criteria from it. 
                    Identify key ranking criteria such as skills, certifications, experience, and qualifications.

                    Return the structured JSON response as below -
                    {{
                        criteria = [
                            "Must have certification XYZ",
                            "5+ years of experience in Python development",
                            "Strong background in Machine Learning",
                        ]
                    }}
                    """,
                },
                {
                    "role": "user",
                    "content": f"""The job description content is {jd_content}
                    """,
                },
            ],
            max_tokens=1024,
            response_model=CriteriaResponse,
        )

        return criteria.criteria
