import aiohttp_cors
import json
from models import Car
from aiohttp import web
from mongoengine.errors import InvalidQueryError

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods='*'
        )
})
routes = web.RouteTableDef()


@routes.get('/cars')
async def create_car(request):
    document = [json.loads(obj.to_json()) for obj in Car.objects(**{k: v for k, v in request.rel_url.query.items() if v})]
    return web.json_response({'items': document}, status=200)


@routes.get(r'/cars/{vin:\w+}')
async def get_car(request):
    car = Car.objects(VIN=request.match_info['vin'])
    return web.json_response({'item': json.loads(car.to_json())}, status=200)


@routes.post('/cars/')
async def cars_list(request):
    try:
        result = Car(**await request.json())
        result.save()
        return web.json_response({'msg': 'Saved'}, status=201)
    except Exception as e:
        return web.json_response({'msg': str(e)}, status=400)


@routes.put(r'/cars/{vin:\w+}')
async def update_car(request):
    car_data = await request.json()
    try:
        if car_data.get('VIN'):
            raise InvalidQueryError('Field VIN is Unchanged')
        Car.objects(VIN=request.match_info['vin']).update(**car_data)
        return web.json_response({'msg': 'Car updated'}, status=201)
    except Exception as e:
        return web.json_response({'msg': str(e)}, status=400)


@routes.delete(r'/cars/{vin:\w+}')
async def delete(request):
    try:
        car = Car.objects(VIN=request.match_info['vin'])
        if not car.delete():
            raise InvalidQueryError('Unknown car with this VIN')
        return web.json_response({'msg': 'Car deleted'}, status=204)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)


app.add_routes(routes)
[cors.add(rout) for rout in list(app.router.routes())]
web.run_app(app, host='127.0.0.1', port=5000)
