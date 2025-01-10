import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.auth import router as auth_router
from backend.routers.product import router as product_router

app = FastAPI(title='MusixShopBackend', docs_url='/api/docs', redoc_url=None)
app.include_router(auth_router)
app.include_router(product_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:63342', 'http://127.0.0.1:3000', 'http://127.0.0.1:5500'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/api/status')
async def server_status():
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
