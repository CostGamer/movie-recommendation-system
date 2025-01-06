from http import HTTPStatus
from typing import Any


def create_error_responses(
    error_responses: dict[int, dict[str, dict[str, Any]]]
) -> dict:
    responses = {}

    for status_code, examples in error_responses.items():
        description = HTTPStatus(status_code).phrase
        responses[status_code] = {
            "description": description,
            "content": {"application/json": {"examples": examples}},
        }

    return responses


register_user_exceptions = {
    409: {
        "email_already_exists_error": {
            "summary": "UserWithThisEmailExistsError",
            "value": {"detail": "This email already in the system"},
        },
    },
    400: {
        "registration_troubles_error": {
            "summary": "TroublesWithRegistrationError",
            "value": {"detail": "Some problems with insertion to db"},
        }
    },
}


login_user_exceptions = {
    404: {
        "invalid_username_or_password_error": {
            "summary": "UserWithThisEmailExistsError",
            "value": {"detail": "Email or password Not Found"},
        },
    },
}


register_user_responses = create_error_responses(register_user_exceptions)
login_user_responses = create_error_responses(login_user_exceptions)
