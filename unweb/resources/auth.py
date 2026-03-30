"""Auth resource — register, login, me, profile, change-password endpoints."""
from __future__ import annotations
from typing import TYPE_CHECKING
from unweb.models import AuthToken, UserProfile

if TYPE_CHECKING:
    from unweb.client import UnWebClient


class AuthResource:
    def __init__(self, client: UnWebClient):
        self._client = client

    def register(self, email: str, password: str, first_name: str = "", last_name: str = "") -> AuthToken:
        """Register a new user."""
        data = self._client._request("POST", "/api/auth/register", json={"email": email, "password": password, "firstName": first_name, "lastName": last_name}, auth_mode="none")
        token = AuthToken(token=data.get("token", ""), user_id=data.get("userId", ""), email=data.get("email", ""))
        self._client._jwt_token = token.token
        return token

    def login(self, email: str, password: str) -> AuthToken:
        """Login and store JWT token."""
        data = self._client._request("POST", "/api/auth/login", json={"email": email, "password": password}, auth_mode="none")
        token = AuthToken(token=data.get("token", ""), user_id=data.get("userId", ""), email=data.get("email", ""))
        self._client._jwt_token = token.token
        return token

    def me(self) -> UserProfile:
        """Get current user profile (requires JWT)."""
        data = self._client._request("GET", "/api/auth/me", auth_mode="jwt")
        return UserProfile(id=data.get("id", ""), email=data.get("email", ""), first_name=data.get("firstName", ""), last_name=data.get("lastName", ""), role=data.get("role", ""))

    def update_profile(self, *, email: str | None = None, first_name: str | None = None, last_name: str | None = None) -> None:
        """Update user profile (requires JWT)."""
        body: dict = {}
        if email is not None: body["email"] = email
        if first_name is not None: body["firstName"] = first_name
        if last_name is not None: body["lastName"] = last_name
        self._client._request("PUT", "/api/auth/profile", json=body, auth_mode="jwt")

    def change_password(self, current_password: str, new_password: str) -> None:
        """Change password (requires JWT)."""
        self._client._request("POST", "/api/auth/change-password", json={"currentPassword": current_password, "newPassword": new_password}, auth_mode="jwt")
