from fastapi import Depends, APIRouter, status
from fastapi.responses import JSONResponse

from ..models.City import *
from ..models.Country import *
from ..models.Message import Message

from ..services.GeolocationServices import GeolocationServices

from typing import List

router = APIRouter(prefix="/geolocation")


@router.post("/city/", responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_201_CREATED: {"model": Message}
})
async def add_city(city: City, service: GeolocationServices = Depends()):
    try:
        await service.add_city(city)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"content": "add city"})
    except ValueError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "country is not found"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "add city error"})


@router.post("/country/", responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_201_CREATED: {"model": Message}
})
async def add_country(country: Country, service: GeolocationServices = Depends()):
    try:
        await service.add_country(country)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"content": "add country"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "add country error"})


@router.get("/city/{id_city}", response_model=CityGet, responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_404_NOT_FOUND: {"model": Message}
})
async def get_city(id_city: int, service: GeolocationServices = Depends()):
    try:
        return await service.get_city(id_city)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"content": "city is not found"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "get city error"})


@router.get("/country/{id_country}", response_model=CountryGet, responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_404_NOT_FOUND: {"model": Message}
})
async def get_country(id_country: int, service: GeolocationServices = Depends()):
    try:
        return await service.get_country(id_country)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"content": "country is not found"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "country city error"})


@router.get("/city/all/{id_country}", response_model=List[CityGet], responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_404_NOT_FOUND: {"model": Message}
})
async def get_all_city(id_country: int, service: GeolocationServices = Depends()):
    try:
        return await service.get_all_city(id_country)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"content": "cities is not found"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "get all city error"})


@router.get("/country/all/", response_model=List[CityGet], responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_404_NOT_FOUND: {"model": Message}
})
async def get_all_country(service: GeolocationServices = Depends()):
    try:
        return await service.get_all_country()
    except ValueError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"content": "countries is not found"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"content": "get all country error"})