from flask import Flask, jsonify
from flask_cors import CORS
import os
from stalker import stalker_bp

app = Flask(__name__)
CORS(app)

# Register blueprint stalker
app.register_blueprint(stalker_bp)

@app.route('/')
def index():
    return jsonify({
        'service': 'Minecraft Stalker API',
        'creator': 'Iyann Nak MBG',
        'version': '2.5.1',
        'docs': '/api/status',
        'example': '/api/minecraft/stalk?username=Notch'
    })

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'service': 'Minecraft Stalker API',
        'version': '2.5.1',
        'creator': 'Iyann Nak MBG',
        'endpoints': {
            '/api/minecraft/stalk': {
                'method': 'GET/POST',
                'description': 'Cari user Minecraft berdasarkan username',
                'params': {'username': 'string (3-16 karakter)'}
            },
            '/api/minecraft/uuid/{uuid}': {
                'method': 'GET',
                'description': 'Konversi UUID ke username'
            },
            '/api/minecraft/batch': {
                'method': 'POST',
                'description': 'Cari multiple username sekaligus'
            },
            '/api/status': {
                'method': 'GET',
                'description': 'Cek status server'
            }
        },
        'example': {
            'stalk': '/api/minecraft/stalk?username=Notch',
            'uuid': '/api/minecraft/uuid/069a79f444e94726a5befca90e38aaf5',
            'batch': '/api/minecraft/batch -d \'{"username_list":["Notch","Dream"]}\''
        }
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'creator': 'Iyann Nak MBG',
        'status': False,
        'error': 'Endpoint tidak ditemukan'
    }), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Server running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)