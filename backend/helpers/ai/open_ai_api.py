# This class represents a simple API for contacting the OpenAI api. It will provide
# simple methods such as getting image or text responses. As of right now it is mostly
# used in our "Resume Helper" feature.
#
# @author: Preston Peck
# @version: 11/1/2024

import requests

# api_key = os.environ.get("OPENAI_API_KEY")
api_key = "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"

def get_resume_help_response(base_64_image, user_id):
    """
    This method gets an analysis of how to improve a resume using OpenAI's vision model.
    As of now, it only accepts a base64-encoded image.

    :param base_64_image: A base64-encoded image of the resume to analyze.
    :param user_id: The ID of the user requesting the analysis.
    :param api_key: The OpenAI API key for authorization.

    :return: A string of the response with suggestions on how to improve the submitted resume.
    """
    
    print(f"Analyzing uploaded resume for user {user_id}...\n")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Provide 3 SHORT suggestions to improve this resume referencing direct evidence from it. "
                                "Format each suggestion on its own line. Prefix each suggestion with 'Suggestion X: ...'. "
                                "After the 3 suggestions, add another line with a score out of 5. Only use full or half numbers! "
                                "Prefix with 'Score: '. (e.g., Score: 3.5/5) BE BRUTALLY HONEST WITH THIS SCORE! Do not add anything additional, just suggestions and score formatted as above. No prefix with 'results of ...' just Suggestion 1: ... <nextline> Suggestion 2: ... etc."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base_64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 250
    }

    # send the request to the OpenAI API, catch any errors if they occur
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None



def get_cover_letter_text_response(job_description, resume_text):
    """
    This method gets a response from the OpenAI API for generating a cover letter.

    :return: A string of the response with the generated cover letter text.
    """

    # TODO: USE OCR OR SOMETHING TO GET RESUME TEXT SO I CAN PASS THAT INTO THIS FIELD AS WELL.

    print("Generating cover letter...\n")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Please generate a short cover letter using the provided job description below.\n\n"
                    "This cover letter **MUST be in exact HTML format** as specified below but outputted as a normal string omitting things like HTML ''' at the beginning and ''' at the end. **Do NOT omit any tags, "
                    "and ensure every `<p>` tag is fully written with both opening `<p>` and closing `</p>` tags.**\n\n"
                    "**STRICTLY FOLLOW THIS FORMAT:**\n\n"
                    "'<h3>Cover Letter</h3>\n"
                    "<h3>John Doe</h3>\n"
                    "<h3>1234 Elm Street</h3>\n"
                    "<h3>Fake City, US, 12345</h3>\n"
                    "<p>Two paragaphs enclosed in paragraph tags like this, each paragaph should be 4 sentences..</p>\n"
                    "\n<h3>Best Regards,</h3>\n"
                    "<h3>John Doe</h3>'\n\n"
                    "**Do NOT include anything outside of the above HTML structure. Do NOT add any extra symbols or quotation marks. "
                    "Do NOT include incomplete tags like `<p`. Each `<p>` tag must be fully written as `<p> ... </p>`.**\n\n"
                    "This response must strictly match the above format without any deviations or missing tags. THE RETURNED STRING SHOULD NOT START WITH HTML ''' OR END WITH '''!!!\n\n"
                    "Here is the job description to reference:\n\n"
                    f"{job_description}"
                )
            }
        ],
        "max_tokens": 550
    }


    # send a request to the openAI  API
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while generating an API response from OpenAI: {e}")
        return None
    