from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import product as product_schema
from backend.database.crud import product as product_crud
from backend.database.database import get_db

router = APIRouter(prefix='/api/product', tags=['product'])


@router.get('/id/{product_id}', response_model=product_schema.Product)
async def get_product(product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        product = await product_crud.get_product_by_id(session, product_id)
        return product
    except Exception as e:
        return {'error': str(e)}


@router.get('/all', response_model=List[product_schema.Product])
async def get_all_products(session: AsyncSession = Depends(get_db)):
    try:
        all_products = await product_crud.get_all_products(session)
        return all_products
    except Exception as e:
        return {'error': str(e)}


@router.post('/', response_model=product_schema.Product)
async def create_product(product: product_schema.ProductCreate, session: AsyncSession = Depends(get_db)):
    try:
        created_product = await product_crud.create_product(session, product)
        return created_product
    except Exception as e:
        return {'error': str(e)}


@router.put('/{product_id}', response_model=dict)
async def update_product(product_id: int, product: product_schema.ProductUpdate, session: AsyncSession = Depends(get_db)):
    try:
        await product_crud.update_product(session, product_id, product)
        return {'status': 'success', 'message': 'Product updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete('/{product_id}', response_model=dict)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        await product_crud.delete_product(session, product_id)
        return {'status': 'success', 'message': 'Product deleted successfully'}
    except Exception as e:
        return {'error': str(e)}
