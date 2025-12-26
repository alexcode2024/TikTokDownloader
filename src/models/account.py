from pydantic import Field
from typing import Literal

from .base import APIModel


class Account(APIModel):
    sec_user_id: str
    tab: str = "post"
    earliest: str | float | int | None = None
    latest: str | float | int | None = None
    pages: int | None = None
    cursor: int = 0
    count: int = Field(
        18,
        gt=0,
    )
    max_count: int | None = Field(
        None,
        description="最大返回作品数量，None表示不限制"
    )
    sort: Literal[0, 1] = Field(
        0,
        description="排序方式：0=按发布日期倒序，1=按点赞数倒序"
    )


class AccountTiktok(Account):
    pass
