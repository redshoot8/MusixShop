import uvicorn
from fastapi import FastAPI
from backend.routers.auth import router as auth_router

app = FastAPI(title='MangaBackend', docs_url='/api/docs', redoc_url=None)
app.include_router(auth_router)


@app.get('/api/status')
async def server_status():
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
