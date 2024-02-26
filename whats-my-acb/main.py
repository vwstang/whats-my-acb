from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import services, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stock", response_model=list[schemas.Stock])
def read_root(db: Session = Depends(get_db)):
    return services.get_stocks(db=db)

@app.get("/stock/{stock_ticker}", response_model=schemas.Stock)
def read_stock(stock_ticker: str, db: Session = Depends(get_db)):
    return services.get_stock_by_ticker(db, ticker=stock_ticker)

@app.post("/stock", response_model=schemas.Stock)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    db_stock = services.get_stock_by_ticker(db, ticker=stock.ticker)
    if db_stock:
        raise HTTPException(status_code=409, detail="Ticker has already been created!")
    return services.create_stock(db=db, stock=stock)

@app.post("/stock/{stock_ticker}/transaction", response_model=schemas.Transaction)
def create_stock_transaction(stock_ticker: str, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    stock = services.get_stock_by_ticker(db, ticker=stock_ticker)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found!")
    return services.create_transaction(db, transaction, stock.id)

@app.delete("/transaction/{transaction_id}")
def delete_stock_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = services.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found!")
    services.delete_transaction(db, transaction_id)
    return {"ok": True}
