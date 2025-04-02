from typing import Dict, Generic, List, Optional, Type, TypeVar, Union, Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base) # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Classe <Base> para repositórios com operações CRUD em comum
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Obtém um objeto pelo id
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 0) -> List[ModelType]:
        """
        Obtém uma lista de objetos
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Cria um novo objeto
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        Atualiza um objeto
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj


    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Deletar um Objeto
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        
        return obj