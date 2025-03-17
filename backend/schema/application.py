# this file represents the schema of a "job application" in our backend database. A job application doesn't
# quite have the same variables a regular "job" schema so this is made to hold it's own variables.
#
# @author: Preston Peck
# @version: 9/23/2024


from pydantic import BaseModel, Field
from backend.schema.job import Job
from typing import Optional, List

class Application(BaseModel):
    id: str =  Field(None, description="Unique identifier of this job on JobQuery's platform.")
    job: Optional[Job] = Field(None, description="Job listing that the application is for.")
    title: Optional[str] = Field(None, description="Position of the job listing. Aka the title.")
    applied_to_by: Optional[str] = Field(None, description="User who applied to the job listing.")
    date_applied: Optional[str] = Field(None, description="Date the user applied to the job listing.")
    status: Optional[str] = Field(None, description="Status of the application (e.g., applied, interviewing, etc.)")
    notes: Optional[str] = Field(None, description="Notes about the application.")
    application_url: Optional[str] = Field(None, description="URL to the application on the job site. This is usually like a workday link or a link to the companies internal careers site.")
    recruiter_name: Optional[str] = Field(None, description="Name of the recruiter for this job.")
    interview_date: Optional[str] = Field(None, description="Date of the interview (if applicable).")
    additional_notes: Optional[str] = Field(None, description="Any additional notes about the job application.")



class ApplicationListResponse(BaseModel):
    applications: List[Application] = Field(..., description="List of job applications corresponding to user's id.")