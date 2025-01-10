from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.user.model import User
from app.schemas.users import UserCreate, UserUpdate, UserResponse
from app.database.user.service import UserService
from app.database.client.service import ClientService
from fastapi import HTTPException
from app.utils.logging import AppLogger
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError
from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from pwdlib.hashers.bcrypt import BcryptHasher

logger = AppLogger().get_logger()

class UserManagementService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)
        self.client_service = ClientService(db)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.hasher = BcryptHasher()

    async def create_user(self, user: UserCreate) -> User:
        api_user = UserCreate.model_validate(user)
        api_user.password = self.hash_password(api_user.password)
        # Create user
        db_user = User(**api_user.model_dump())
        date_now = datetime.now()
        current_user_id = 0
        db_user.created = date_now
        db_user.created_by = current_user_id
        db_user.updated = date_now
        db_user.updated_by = current_user_id
        
        # Save user
        return await db_user.save(self.db)
    
    async def update_current_user(self, user_id: int, user: User):
        try:
            db_user = await self.user_service.get_user_by_id(user_id)
            logger.info(f"db_user: {db_user}")
            logger.info(f"user client ID: {user.client_id}")
            db_client = await self.client_service.get_client_by_id(user.client_id)
            if not db_client:
                raise HTTPException(status_code=404, detail="Client not found")
            new_user = UserUpdate.model_validate(user)
            data = new_user.model_dump(exclude_none=True)
            
            if "password" in data:
                data["password"] = self.hash_password(data["password"])

            data["updated"] = datetime.now()
            data["updated_by"] = 0

            return await db_user.update(self.db, **data)
        except ValueError as e:
            # Handle validation errors
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError as e:
            # Handle duplicate key or constraint violations
            logger.error(f"IntegrityError: {e}")
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"IntegrityError: {e}"
            )
        except StatementError as e:
            # Handle JSON serialization errors and other statement errors
            logger.error(f"StatementError: {e}")
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data format: {str(e)}"
            )
        except SQLAlchemyError as e:
            # Handle any other database-related errors
            logger.error(f"Database error: {e}")
            await self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            # Handle any unexpected errors
            logger.error(f"Unexpected error: {e}")
            await self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

    async def login(self, username: str, password: str) -> User:
        user = await self.get_authenticated_user(self.db, username, password)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def hash_password(self, password: str):
        return self.hasher.hash(password)

    async def get_authenticated_user(self, db: AsyncSession, username: str, password_clear: str):
        query = select(User).filter(User.username == username)
        logger.info(f"query: {query}")
        result = await db.exec(query)
        user = result.first()

        if not user:
            return False
        if not self.hasher.verify(password_clear, user.password):
            return False
        user.last_login = datetime.now()
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserResponse(**user.__dict__)

