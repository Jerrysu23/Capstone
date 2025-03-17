# This file has a lot of the helper functions that are used in our backend routes. This clears up some
# of the cluttered functions and makes the routes more readable. Some of these helpers are for transforming
# the data, balancing the data, etc.
#
# author: Preston Peck
# version: Sept. 4, 2024

from datetime import date
import uuid

def sanitize_job_listing_values(jobs) -> dict:
    """Converts the values in the jobs dataframe to a dictionary that can be added to the MongoDB collection.
    MongoDB does not like NaN values so we convert them to empty strings. We also convert the date values to date objects"""

    # fill in any N/A values, idk why tbh
    jobs = jobs.fillna("")

    # convert min and max to 0.0 if empty string
    for col in ['min_amount', 'max_amount']:
        jobs[col] = jobs[col].apply(lambda x: 0.0 if x == '' else float(x))

    # convert empty strings to False for is_remote column
    jobs['is_remote'] = jobs['is_remote'].apply(lambda x: False if x == '' else x)

    # convert dates to iso format to adhere to mongoDB guidelines
    jobs = jobs.map(lambda x: str(x.isoformat()) if isinstance(x, date) else x)

    # convert DataFrame to a list of dictionaries
    jobs_dict = jobs.to_dict(orient="records")

    # give each job listing it's own unique idenitity (uniquely identifies it with JobQuery and not with whatever is scraped)
    for job in jobs_dict:
        new_id = str(uuid.uuid4())
        job['id'] = new_id
        print(f"The ID, {new_id}, was assigned to the job {job['title']}.")

    return jobs_dict
