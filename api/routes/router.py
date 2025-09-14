from fastapi import APIRouter
from typing import List

# Importando os routers dos diferentes módulos
from api.routes.main import router as main_router

# Criando um conjunto de routers
routes: List[APIRouter] = [
    main_router
]

