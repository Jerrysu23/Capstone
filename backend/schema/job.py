# This file is responsible for holding all the user schema that is returned by our backend FastAPI server, this
# file essentially defines what user "types" we can expect to be returned from the API.
#
# author: Preston Peck
# version: Sept. 3, 2024

from pydantic import BaseModel, Field
from typing import Optional, List

# schema that represents the structure of a job listing in our backend.
class Job(BaseModel):
    """Job schema that defines the structure of a job listing."""

    id: Optional[str] = Field(None, description="Unique identifier of this job on JobQuery's platform.") # i know this is optional which is bad practice, but it should always exist.
    saved_by: Optional[str] = Field(None, description="User who saved the job listing") # this is used for saved job listings, different users will have different listings.
    site: str = Field(..., description="Name of the site where the job was posted")
    job_url: str = Field(..., description="URL to the job listing on the site")
    job_url_direct: Optional[str] = Field(None, description="Direct URL to the job listing if available (on the companies site.)")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Location of the job")
    job_type: str = Field(..., description="Type of job (e.g., fulltime, parttime, internship, etc.)")
    date_posted: str = Field(..., description="Date the job was posted")
    salary_source: Optional[str] = Field(None, description="Source of the salary information")
    interval: Optional[str] = Field(None, description="Interval of the salary (e.g., hourly, yearly)")
    min_amount: Optional[float] = Field(None, description="The minimum amount the job pays.")
    max_amount: Optional[float] = Field(None, description="The maximum amount the job pays.")
    currency: Optional[str] = Field(None, description="Currency of the salary")
    is_remote: Optional[bool] = Field(None, description="Indicates if the job is remote")
    job_level: Optional[str] = Field(None, description="Job level (e.g., entry, senior)")
    job_function: Optional[str] = Field(None, description="Job function or department")
    company_industry: Optional[str] = Field(None, description="Industry of the company")
    listing_type: Optional[str] = Field(None, description="Type of listing")
    emails: Optional[str] = Field(None, description="Emails associated with the job listing")
    description: Optional[str] = Field(None, description="Job description")
    company_url: Optional[str] = Field(None, description="URL to the company's profile on the job site")
    company_url_direct: Optional[str] = Field(None, description="Direct URL to the company's website")
    company_addresses: Optional[str] = Field(None, description="Physical address of the company")
    company_num_employees: Optional[str] = Field(None, description="Number of employees in the company")
    company_revenue: Optional[str] = Field(None, description="Revenue of the company")
    company_description: Optional[str] = Field(None, description="Description of the company")
    logo_photo_url: Optional[str] = Field(None, description="URL to the company's logo")
    banner_photo_url: Optional[str] = Field(None, description="URL to the company's banner photo")
    ceo_name: Optional[str] = Field(None, description="Name of the CEO of the company")
    ceo_photo_url: Optional[str] = Field(None, description="URL to the CEO's photo")



# Schema that represents the response for a list of jobs (A list of jobs.)
class JobListResponse(BaseModel):
    jobs: List[Job] = Field(..., description="List of job listings")



class JobInsertDatabaseResponse(BaseModel):
    status: str = Field(..., description="Message indicating the status of anything inserted into any job databases.")
    scraped_jobs: Optional[List[Job]] = Field(None, description="List of job listings inserted into the database.")


class IsSavedResponse(BaseModel):
    is_saved_status: bool = Field(..., description="Indicates if the job is saved by the user.")