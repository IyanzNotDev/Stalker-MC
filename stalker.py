from flask import Blueprint, request, jsonify
import requests
import re
from datetime import datetime

# Buat blueprint
stalker_bp = Blueprint('stalker', __name__, url_prefix='/api/minecraft')

def validate_username(username):
    """Validasi username Minecraft (3-16 karakter, alfanumerik + underscore)"""
    if not username:
        return False, "Username tidak boleh kosong"
    if len(username) < 3 or len(username) > 16:
        return False, "Username harus 3-16 karakter"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username hanya boleh huruf, angka, dan underscore"
    return True, None

@stalker_bp.route('/stalk', methods=['GET', 'POST'])
def stalk_minecraft():
    # Ambil username dari GET atau POST
    if request.method == 'GET':
        username = request.args.get('username', '').strip()
    else:
        data = request.get_json()
        username = data.get('username', '').strip() if data else ''
    
    # Validasi
    valid, error = validate_username(username)
    if not valid:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': error
        }), 400
    
    try:
        # ===== 1. CEK KE MOJANG API =====
        mojang_resp = requests.get(
            f'https://api.mojang.com/users/profiles/minecraft/{username}',
            timeout=10
        )
        
        if mojang_resp.status_code == 404:
            return jsonify({
                'creator': 'Iyann Nak MBG',
                'status': False,
                'message': f'Username "{username}" tidak terdaftar di Minecraft'
            }), 404
            
        if mojang_resp.status_code != 200:
            return jsonify({
                'creator': 'Iyann Nak MBG',
                'status': False,
                'error': f'Mojang API error: {mojang_resp.status_code}'
            }), 500
        
        mojang_data = mojang_resp.json()
        uuid = mojang_data.get('id', '')
        current_username = mojang_data.get('name', username)
        
        # ===== 2. AMBIL NAME HISTORY =====
        history_resp = requests.get(
            f'https://api.mojang.com/user/profiles/{uuid}/names',
            timeout=10
        )
        name_history = []
        if history_resp.status_code == 200:
            history = history_resp.json()
            name_history = [
                {
                    'name': h.get('name', ''),
                    'changed_at': h.get('changedToAt', None)
                }
                for h in history
            ]
        
        # ===== 3. AMBIL SKIN DARI CRAFATAR =====
        skin_url = f'https://crafatar.com/skins/{uuid}'
        avatar_url = f'https://crafatar.com/avatars/{uuid}'
        cape_url = f'https://crafatar.com/capes/{uuid}'
        render_url = f'https://crafatar.com/renders/body/{uuid}'
        
        # ===== 4. BUILD RESPONSE =====
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': True,
            'timestamp': datetime.now().isoformat(),
            'result': {
                'uuid': uuid,
                'username': current_username,
                'skin': skin_url,
                'avatar': avatar_url,
                'cape': cape_url,
                'render': render_url,
                'name_history': name_history,
                'total_name_changes': len(name_history) - 1
            }
        })
        
    except requests.exceptions.Timeout:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': 'Mojang API timeout, coba lagi nanti'
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': 'Gagal terhubung ke Mojang API'
        }), 503
    except Exception as e:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500

@stalker_bp.route('/uuid/<uuid>', methods=['GET'])
def uuid_to_username(uuid):
    """Konversi UUID ke username Minecraft"""
    uuid = uuid.strip().replace('-', '')
    if len(uuid) != 32:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': 'UUID harus 32 karakter hex'
        }), 400
    
    try:
        resp = requests.get(
            f'https://api.mojang.com/user/profile/{uuid}',
            timeout=10
        )
        
        if resp.status_code == 404:
            return jsonify({
                'creator': 'Iyann Nak MBG',
                'status': False,
                'message': f'UUID {uuid} tidak ditemukan'
            }), 404
        
        if resp.status_code == 200:
            data = resp.json()
            return jsonify({
                'creator': 'Iyann Nak MBG',
                'status': True,
                'result': {
                    'uuid': uuid,
                    'username': data.get('name', ''),
                    'skin': f'https://crafatar.com/skins/{uuid}',
                    'avatar': f'https://crafatar.com/avatars/{uuid}'
                }
            })
        
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': f'Mojang API error: {resp.status_code}'
        }), 500
        
    except Exception as e:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': str(e)
        }), 500

@stalker_bp.route('/batch', methods=['POST'])
def batch_stalk():
    """Stalk multiple username sekaligus"""
    data = request.get_json()
    if not data or 'username_list' not in data:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': 'Parameter "username_list" wajib diisi'
        }), 400
    
    username_list = data['username_list']
    if not isinstance(username_list, list):
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': 'username_list harus berupa array'
        }), 400
    
    if len(username_list) > 20:
        return jsonify({
            'creator': 'Iyann Nak MBG',
            'status': False,
            'error': 'Maksimal 20 username per request'
        }), 400
    
    results = []
    for username in username_list:
        username = str(username).strip()
        valid, error = validate_username(username)
        if not valid:
            results.append({
                'username': username,
                'status': 'INVALID',
                'error': error
            })
            continue
        
        try:
            resp = requests.get(
                f'https://api.mojang.com/users/profiles/minecraft/{username}',
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                results.append({
                    'username': username,
                    'status': 'FOUND',
                    'uuid': data.get('id', ''),
                    'skin': f'https://crafatar.com/skins/{data.get("id", "")}'
                })
            else:
                results.append({
                    'username': username,
                    'status': 'NOT_FOUND'
                })
        except:
            results.append({
                'username': username,
                'status': 'ERROR',
                'error': 'Timeout atau koneksi gagal'
            })
    
    return jsonify({
        'creator': 'Iyann Nak MBG',
        'status': True,
        'total': len(results),
        'results': results
    })