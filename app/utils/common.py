"This file contains common utility functions for the Flask application"
import ipaddress
import logging
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def paginate_query(model, filters=None, page=1, per_page=10):
    """paginate a query for a given model with optional filters.
    Args:
        model (obj): The SQLAlchemy model to query.
        filters (list, optional): A list of filter conditions to apply. Defaults to None.
        page (int, optional): The page number to retrieve. Defaults to 1.
        per_page (int, optional): The number of items per page. Defaults to 10.

    Returns:
        obj: The paginated result.
    """
    query = model.query
    if filters:
        for condition in filters:
            query = query.filter(condition)

    return query.paginate(page=page, per_page=per_page, error_out=False)

def validate_enum(value, enum_class):
    """Validate if a value is a valid member of an Enum class.

    Args:
        value (str): The value to validate.
        enum_class (Enum): The Enum class to check against.

    Returns:
        Enum: The corresponding Enum member if valid.

    Raises:
        ValueError: If the value is not a valid member of the Enum.
    """
    try:
        return enum_class(value)
    except ValueError:
        raise ValueError(f"Invalid value '{value}'. Valid values are: {[e.value for e in enum_class]}")



def safe_commit(session):
    """Safely commit a session, rolling back on failure.

    Args:
        session (Session): The SQLAlchemy session to commit.

    Returns:
        bool: True if commit was successful, False otherwise.
    """
    try:
        session.commit()
        return True

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Commit failed: {str(e)}")
        return False
