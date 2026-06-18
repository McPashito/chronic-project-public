from fastapi import FastAPI
from app.api.routes import glucose_records_routes
from app.api.routes import auth_routes
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import users_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://chronic-project-public.vercel.app",
        "https://chronic-project-frontend.vercel.app",
        "https://chronic-project-frontend-git-main-mcpashitos-projects.vercel.app",
        "https://chronic-project-frontend-pvwgs1ofy-mcpashitos-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(glucose_records_routes.router)
app.include_router(auth_routes.router)
app.include_router(users_routes.router)


@app.get("/")
def read_root():
    return {"message": "Hola Amigo"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
