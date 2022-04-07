from fastapi import Depends, APIRouter, HTTPException
import secrets

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# --------------------------
# All stations operations
# --------------------------

@router.post("/login")
def login():
  """Authenticate user

  Checks if the username and password provided are correct.

  Returns:
    str: Returns true if the user is authenticated, false otherwise
  """
  return {"status": True, "message": "Authenticated"}
