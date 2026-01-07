"""Create a test user in the database."""
import asyncio
from models import User
from db import async_session


async def create_test_user():
    """Create a test user for testing."""
    async with async_session() as session:
        # Create test user
        user = User(
            id="test-user-123",
            email="test@example.com",
            name="Test User",
            hashed_password="hashed_password_here"  # Placeholder
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        print(f"Test user created:")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.name}")


if __name__ == "__main__":
    asyncio.run(create_test_user())
