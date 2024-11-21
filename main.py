from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import *
from fastapi.responses import RedirectResponse
app = FastAPI()

# Подключаем директорию с HTML-шаблонами
templates = Jinja2Templates(directory="templates")

# Если понадобятся статические файлы (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Список всех накладных
@app.get("/invoices", response_class=HTMLResponse)
def list_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    return templates.TemplateResponse("invoices.html", {"request": request, "invoices": invoices})

# Форма создания накладной
@app.get("/invoice-form", response_class=HTMLResponse)
def invoice_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Добавление новой накладной
@app.post("/invoice")
def create_invoice(
    company_name: str = Form(...),
    product_type: str = Form(...),
    unit_of_measurement: str = Form(...),
    price_per_unit: float = Form(...),
    # total_sum: float = Form(...),
    db: Session = Depends(get_db),
):
    total_sum = price_per_unit
    new_invoice = Invoice(
        company_name=company_name,
        product_type=product_type,
        unit_of_measurement=unit_of_measurement,
        price_per_unit=price_per_unit,
        total_sum=total_sum,
    )
    db.add(new_invoice)
    db.commit()
    return RedirectResponse("/invoices", status_code=303)

# Список всех приходных ордеров
@app.get("/incoming-orders", response_class=HTMLResponse)
def list_incoming_orders(request: Request, db: Session = Depends(get_db)):
    orders = db.query(IncomingOrder).all()
    return templates.TemplateResponse("incoming_orders.html", {"request": request, "orders": orders})

# Форма создания приходного ордера
@app.get("/incoming-order", response_class=HTMLResponse)
def incoming_order_form(request: Request):
    return templates.TemplateResponse("incoming_order.html", {"request": request})

# Добавление нового приходного ордера
@app.post("/incoming-order")
def create_incoming_order(
    company_name: str = Form(...),
    product_type: str = Form(...),
    storage: str = Form(...),
    registration_number: str = Form(...),
    unit_of_measurement: str = Form(...),
    price_per_unit: float = Form(...),
    total_sum: float = Form(...),
    
    chief_accountant: str = Form(None),
    cashier: str = Form(None),
    db: Session = Depends(get_db),
):
    # total_sum = price_per_unit
    new_order = IncomingOrder(
        company_name=company_name,
        product_type=product_type,
        storage=storage,
        registration_number=registration_number,
        unit_of_measurement=unit_of_measurement,
        price_per_unit=price_per_unit,
        total_sum=total_sum,

        chief_accountant=chief_accountant,
        cashier=cashier,
    )
    db.add(new_order)
    db.commit()
    return RedirectResponse("/incoming-orders", status_code=303)

# Подключение статических файлов (если нужно)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/directories", response_class=HTMLResponse)
def list_directories(request: Request, db: Session = Depends(get_db)):
    directories = db.query(Directory).all()
    return templates.TemplateResponse("directories.html", {"request": request, "directories": directories})

# Форма создания справочника
@app.get("/directory-form", response_class=HTMLResponse)
def directory_form(request: Request):
    return templates.TemplateResponse("directory_form.html", {"request": request})

# Добавление нового справочника
@app.post("/directory")
def create_directory(
    company_name: str = Form(...),
    product_type: str = Form(...),
    code: str = Form(...),
    storage_code: str = Form(...),
    responsible_person: str = Form(None),
    db: Session = Depends(get_db),
):
    new_directory = Directory(
        company_name=company_name,
        product_type=product_type,
        code=code,
        storage_code=storage_code,
        responsible_person=responsible_person,
    )
    db.add(new_directory)
    db.commit()
    return RedirectResponse("/directories", status_code=303)