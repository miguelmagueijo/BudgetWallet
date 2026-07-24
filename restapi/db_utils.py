from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from db_models import BaseDbModel
from dependencies import DbSessionDependency


def generic_record_delete(db_session: DbSessionDependency, target: BaseDbModel | None, not_existing_msg: str):
    if target is None:
        raise HTTPException(status_code=404, detail=not_existing_msg)

    db_session.delete(target)
    db_session.commit()

def generic_record_patch(db_session: DbSessionDependency, target: BaseDbModel | None, data: BaseModel,
                          not_existing_msg: str):
    if target is None:
        raise HTTPException(status_code=404, detail=not_existing_msg)

    update_data = data.model_dump(exclude_unset=True)

    if len(update_data.keys()) == 0:
        return

    for key, value in update_data.items():
        setattr(target, key, value)

    db_session.add(target)
    db_session.commit()