from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, require_admin
from app.models.user import User
from app.schemas.common import Response

router = APIRouter(prefix="/categories", tags=["资产分类管理"])


@router.get("/tree", response_model=Response)
def get_category_tree(db: SessionDep):
    from app.models.category import Category
    from sqlalchemy import select
    
    query = select(Category).order_by(Category.sort_order)
    categories = list(db.execute(query).scalars().all())
    
    def build_tree(parent_id: int = 0) -> list[dict]:
        result = []
        for cat in categories:
            if cat.parent_id == parent_id:
                node = {
                    "id": cat.id,
                    "name": cat.name,
                    "code": cat.code,
                    "parent_id": cat.parent_id,
                    "sort_order": cat.sort_order,
                    "status": cat.status,
                    "children": build_tree(cat.id),
                }
                result.append(node)
        return result
    
    return Response(data=build_tree())


@router.get("", response_model=Response)
def get_categories(
    db: SessionDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
):
    from app.models.category import Category
    from sqlalchemy import select, func
    
    skip = (page - 1) * page_size
    query = select(Category).order_by(Category.sort_order).offset(skip).limit(page_size)
    count_query = select(func.count(Category.id))
    
    total = db.execute(count_query).scalar_one()
    categories = list(db.execute(query).scalars().all())
    
    return Response(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": c.id,
                "name": c.name,
                "code": c.code,
                "parent_id": c.parent_id,
                "sort_order": c.sort_order,
                "status": c.status,
            }
            for c in categories
        ],
    })


@router.post("", response_model=Response)
def create_category(
    name: str,
    code: str,
    parent_id: int = 0,
    sort_order: int = 0,
    db: SessionDep = None,
    current_user: Annotated[User, Depends(require_admin)] = None,
):
    from app.models.category import Category
    
    cat = Category(
        name=name,
        code=code,
        parent_id=parent_id,
        sort_order=sort_order,
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    
    return Response(data={
        "id": cat.id,
        "name": cat.name,
        "code": cat.code,
        "parent_id": cat.parent_id,
        "sort_order": cat.sort_order,
    })


@router.put("/{cat_id}", response_model=Response)
def update_category(
    cat_id: int,
    name: str | None = None,
    code: str | None = None,
    parent_id: int | None = None,
    sort_order: int | None = None,
    status: int | None = None,
    db: SessionDep = None,
    current_user: Annotated[User, Depends(require_admin)] = None,
):
    from app.models.category import Category
    
    cat = db.get(Category, cat_id)
    if not cat:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    
    if name is not None:
        cat.name = name
    if code is not None:
        cat.code = code
    if parent_id is not None:
        cat.parent_id = parent_id
    if sort_order is not None:
        cat.sort_order = sort_order
    if status is not None:
        cat.status = status
    
    db.add(cat)
    db.commit()
    db.refresh(cat)
    
    return Response(data={
        "id": cat.id,
        "name": cat.name,
        "code": cat.code,
        "parent_id": cat.parent_id,
        "sort_order": cat.sort_order,
        "status": cat.status,
    })


@router.delete("/{cat_id}", response_model=Response)
def delete_category(
    cat_id: int,
    db: SessionDep,
    current_user: Annotated[User, Depends(require_admin)],
):
    from app.models.category import Category
    
    cat = db.get(Category, cat_id)
    if not cat:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    
    db.delete(cat)
    db.commit()
    
    return Response(message="删除成功")