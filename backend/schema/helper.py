# File that has the schema for the helper responses for our AI resume helper.
#
# Author: Preston Peck
# Version: 9/9/2024

from pydantic import BaseModel
from typing import List

class ResumeHelperResponse (BaseModel):
    response: str
    response_id: str
    created_at: str = None

class UserResumePastResponses(BaseModel):
    responses: List[ResumeHelperResponse]