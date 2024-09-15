# main.py
from fastapi import FastAPI, status, Query, Path, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from schemas import NewTrip, SavedTrip, TripPrice
from storage import storage

app = FastAPI(
    title='Travel Agency',
    description='Manage travel offers for trips to resorts in Ukraine and the world.',
    version='1.0.0'
)

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', include_in_schema=False)
def index(request: Request, q: str = Form(default='')):
    trips = storage.get_trips(limit=10, q=q)
    context = {
        'request': request,
        'page_title': 'All Trips',
        'trips': trips
    }
    return templates.TemplateResponse('index.html', context=context)


@app.get('/trip/{trip_id}', include_in_schema=False)
def trip_detail(request: Request, trip_id: int):
    trip = storage.get_trip(trip_id)
    context = {
        'request': request,
        'page_title': f'Trip to {trip.destination}',
        'trip': trip
    }
    return templates.TemplateResponse('details.html', context=context)

# CRUD API

@app.post('/api/trip/', description='Create a new trip', status_code=status.HTTP_201_CREATED, tags=['API', 'Trip'])
def add_trip(new_trip: NewTrip) -> SavedTrip:
    return storage.create_trip(new_trip)

@app.get('/api/trip/', tags=['API', 'Trip'])
def get_trips(limit: int = Query(default=10, gt=0), q: str = '') -> list[SavedTrip]:
    return storage.get_trips(limit=limit, q=q)

@app.get('/api/trip/{trip_id}', tags=['API', 'Trip'])
def get_trip(trip_id: int = Path(ge=1)) -> SavedTrip:
    return storage.get_trip(trip_id)

@app.patch('/api/trip/{trip_id}', tags=['API', 'Trip'])
def update_trip_price(new_price: TripPrice, trip_id: int = Path(ge=1)) -> SavedTrip:
    return storage.update_trip_price(trip_id, new_price=new_price.price)

@app.delete('/api/trip/{trip_id}', tags=['API', 'Trip'])
def delete_trip(trip_id: int = Path(ge=1)) -> dict:
    storage.delete_trip(trip_id)
    return {"message": f"Trip {trip_id} deleted"}


