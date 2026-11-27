from flask import current_app, Blueprint, send_from_directory, request, jsonify
from http import HTTPStatus
from . import db
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from math import isfinite

bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/')
def index():
    return current_app.send_static_file('index.html'), HTTPStatus.OK

@bp.route('/about')
def about():
    return current_app.send_static_file('about.html'), HTTPStatus.OK

@bp.route('/sw.js')
def service_worker():
    return current_app.send_static_file('sw.js'), HTTPStatus.OK

@api_bp.route('/time', methods=('GET',))
def get_time():
    time_format = request.args.get('format', '24') + 'h'
    if time_format not in ('24h', '12h'):
        time_format = '24h'

    try:
        timezone = request.args['timezone']
        zone_info = ZoneInfo(timezone)
    except (KeyError, ValueError, ZoneInfoNotFoundError):
        return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR

    now = datetime.now(zone_info)
    formatted_time = now.strftime(
        '%H:%M:%S' if time_format == '24h' else '%I:%M:%S %p'
    )

    return jsonify({
        'time': formatted_time,
        'timezone': timezone,
        'format': time_format
    }), HTTPStatus.OK

@api_bp.route('/products', methods=('GET',))
def get_products():
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)

    if min_price is not None and (not isfinite(min_price) or min_price < 0.):
        return jsonify({'error': 'minPrice must be non-negative'}), HTTPStatus.BAD_REQUEST
    if max_price is not None and (not isfinite(max_price) or max_price < 0.):
        return jsonify({'error': 'maxPrice must be non-negative'}), HTTPStatus.BAD_REQUEST

    return jsonify(db.get_products(min_price, max_price)), HTTPStatus.OK

@api_bp.route('/products', methods=('POST',))
def add_product():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON body'}), HTTPStatus.BAD_REQUEST

    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')

    if not isinstance(name, str) or not name.strip():
        return jsonify({'error': 'Invalid name'}), HTTPStatus.BAD_REQUEST
    if not isinstance(price, (float, int)) or isinstance(price, bool) or not isfinite(price) or price < 0:
        return jsonify({'error': 'Invalid price'}), HTTPStatus.BAD_REQUEST
    if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
        return jsonify({'error': 'Invalid stock'}), HTTPStatus.BAD_REQUEST

    product_id = db.add_product(name, price, stock)
    return jsonify({
        'id': product_id,
        'name': name,
        'price': price,
        'stock': stock
    }), HTTPStatus.CREATED

@api_bp.route('/products/<int:product_id>', methods=('PATCH',))
def update_product_stock(product_id):
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON body'}), HTTPStatus.BAD_REQUEST

    if 'name' in data or 'price' in data:
        return jsonify({'error': 'Only the stock field can be updated'}), HTTPStatus.BAD_REQUEST

    stock = data.get('stock')
    if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
        return jsonify({'error': 'Invalid stock'}), HTTPStatus.BAD_REQUEST

    if not db.update_product_stock(product_id, stock):
        return jsonify({'error': 'Product not found'}), HTTPStatus.NOT_FOUND
    return '', HTTPStatus.NO_CONTENT

@api_bp.route('/products/<int:product_id>', methods=('DELETE',))
def delete_product(product_id):
    if not db.delete_product(product_id):
        return jsonify({'error': 'Product not found'}), HTTPStatus.NOT_FOUND
    return '', HTTPStatus.NO_CONTENT
