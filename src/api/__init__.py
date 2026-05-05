from fastapi import APIRouter

from api.users import router as users_router
from api.exhibits import router as exhibits_router
from api.expositions import router as exposition_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(exhibits_router)
main_router.include_router(exposition_router)


