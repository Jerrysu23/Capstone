from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# Import all library dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



# Import all route related funcitions, routers, etc.
from backend.routes.user.users import users_router
from backend.routes.ai.helper import helper_router
from backend.routes.user.auth import auth_router
from backend.routes.user.register import register_router
from backend.routes.job.saved_jobs import save_router
from backend.routes.job.applied_jobs import applications_router
from backend.routes.ai.resume_upload import resume_router
from backend.routes.job.jobs import jobs_router
from backend.routes.ai.CL_generator import cover_letter_router
from backend.database.database import EntityException
from backend.routes.user.auth import auth_router, DuplicateValueException
from backend.routes.calendar.calendar_events import calendar_router
from backend.routes.job.review import reviews_router  # Import the reviews_router

from backend.routes.job.jobs import initialize_locations

# Create the application FastAPI instance
app = FastAPI(
    title="JobQueryAPI",
    description="An API for scraping job listings, retreiving job listing information, user information, and much more. Serves as the backend for JobQuery.com",
    version="0.108.0"
)
# Global variable to store unique locations
unique_locations = []
unique_addresses = []

@app.on_event("startup")
def startup_event():
    initialize_locations()

# This basically sets things up so that our frontend host (when using "npm run dev")
# has permission to query our API for getting database information. Eventually, we
# will add our own hosting origin to this list (ie. jobquery.com)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "https://192.168.50.7:5173",
                   "https://jobquery.zachmediaserver.com",
                   "http://localhost:8000",
                   "http://127.0.0.1:8000",
                   "https://192.168.50.7:8000",
                   "https://jobquery-backend.zachmediaserver.com",
                   ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#include the routers for jobs and users
app.include_router(users_router)
app.include_router(jobs_router)
app.include_router(helper_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(save_router)
app.include_router(register_router)
app.include_router(save_router)
app.include_router(applications_router)
app.include_router(calendar_router)
app.include_router(cover_letter_router)
app.include_router(reviews_router)


@app.exception_handler(EntityException)
def handle_entity_not_found(
        _request: Request,
        exception: EntityException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": {
                "type": exception.exception_type,
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )


@app.exception_handler(DuplicateValueException)
def handle_duplicate_entity(
        _request: Request,
        exception: DuplicateValueException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": {
                "type": "duplicate_value",
                "entity_name": "User",
                "entity_field": exception.entity_field,
                "entity_value": exception.entity_value
            },
        },
    )
