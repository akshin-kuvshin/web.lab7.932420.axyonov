from flask import Blueprint, send_from_directory, request, jsonify
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

bp = Blueprint('main', __name__)

STATIC_DIR = Path(__file__).parent / 'static'
INTERNAL_SERVER_ERROR_CODE = 500 # i'm going back to five-o-o...

@bp.route('/')
def index():
    return send_from_directory(
        STATIC_DIR,
        'index.html'
    )

@bp.route('/about')
def about():
    return send_from_directory(
        STATIC_DIR,
        'about.html'
    )

@bp.route('/api/time')
def get_time():
    time_format = request.args.get('format', '24') + 'h'
    if time_format not in ('24h', '12h'):
        time_format = '24h'

    try:
        timezone = request.args['timezone']
        zone_info = ZoneInfo(timezone)
    except (KeyError, ValueError, ZoneInfoNotFoundError):
        return jsonify({'error': 'Internal server error'}), INTERNAL_SERVER_ERROR_CODE

    now = datetime.now(zone_info)
    formatted_time = now.strftime(
        '%H:%M:%S' if time_format == '24h' else '%I:%M:%S %p'
    )

    return jsonify({
        'time': formatted_time,
        'timezone': timezone,
        'format': time_format
    })

@bp.route('/sw.js')
def service_worker():
    return send_from_directory(
        STATIC_DIR,
        'sw.js'
    )
