from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class TransactionTypeEnum(str, Enum):
  Buy = "Buy"
  Sell = "Sell"


class TransactionBase(BaseModel):
  transaction_date: datetime = None
  settlement_date: datetime = None
  type: TransactionTypeEnum = TransactionTypeEnum.Buy
  price: float
  quantity: float

class TransactionCreate(TransactionBase):
  pass

class Transaction(TransactionBase):
  id: int
  stock_id: int
  
  class Config:
    orm_mode = True


class StockBase(BaseModel):
  name: str
  ticker: str

class StockCreate(StockBase):
  pass

class Stock(StockBase):
  id: int
  transactions: list[Transaction] = []

  class Config:
    orm_mode = True