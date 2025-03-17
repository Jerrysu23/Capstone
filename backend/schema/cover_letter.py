# Model class the represents the schema of a cover letter. A cover letter is stored in our database in this
# format essentially.
#
# author: Preston Peck
# version: 2024-11-06

from pydantic import BaseModel
from typing import List, Optional

class CoverLetter(BaseModel):
    """
    Represents a cover letter model that is stored in the database.
    """
    cover_letter_id: str
    cover_letter_content: str
    job_id: str
    user_id: str 
    cl_file: bytes
    preview_image: Optional[str] = None  # Base64-encoded preview image that is shown in each dashboard card
    date_created: str


class CoverLetterList(BaseModel):
    """
    Represents a list of cover letters that are stored in the database (or returned from the DB).
    """

    cover_letters: List[CoverLetter]
    