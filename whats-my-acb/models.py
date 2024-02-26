import enum
from sqlalchemy import Column, Integer, Float, String, Date, Enum, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .database import Base

class TransactionType(enum.Enum):
  Buy = "Buy"
  Sell = "Sell"
  # split = "Split"
  # reverse_split = "Reverse Split"

class Stock(Base):
  __tablename__ = "stock"

  id = Column(Integer, primary_key=True)
  name = Column(String)
  ticker = Column(String)

  transactions = relationship("Transaction", back_populates="stock")

# class Currency(Base):
#   __tablename__ = "currency"

#   id = Column(Integer, primary_key=True)
#   name = Column(String)
#   code = Column(String)

# class ForeignExchange(Base):
#   __tablename__ = "foreign_exchange"

#   id = Column(Integer, primary_key=True)
#   date = Column(Date)
#   from_id = Column(Integer, ForeignKey("currency.id"), ForeignKey)
#   to_id = Column(Integer, ForeignKey("currency.id"))
  


class Transaction(Base):
  __tablename__ = "transaction"

  id = Column(Integer, primary_key=True)
  transaction_date = Column(Date)
  settlement_date = Column(Date)
  type = Column(Enum(TransactionType))
  price = Column(Float)
  quantity = Column(Float)

  stock_id = Column(Integer, ForeignKey("stock.id"))
  stock = relationship("Stock", back_populates="transactions")
