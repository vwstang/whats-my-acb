from sqlalchemy.orm import Session

from . import models, schemas

def get_stocks(db: Session):
  return db.query(models.Stock).all()

def get_stock(db: Session, stock_id: int):
  return db.query(models.Stock).filter(models.Stock.id == stock_id).first()

def get_stock_by_ticker(db: Session, ticker: str):
  return db.query(models.Stock).filter(models.Stock.ticker == ticker).first()

def create_stock(db: Session, stock: schemas.StockCreate):
  db_stock = models.Stock(name=stock.name, ticker=stock.ticker)
  db.add(db_stock)
  db.commit()
  db.refresh(db_stock)
  return db_stock

def get_transaction(db: Session, transaction_id: int):
  return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, stock_id: int):
  db_transaction = models.Transaction(**transaction.model_dump(), stock_id=stock_id)
  db.add(db_transaction)
  db.commit()
  db.refresh(db_transaction)
  return db_transaction

def delete_transaction(db: Session, transaction_id: int):
  db_transaction = db.get(models.Transaction, transaction_id)
  db.delete(db_transaction)
  db.commit()
  return True