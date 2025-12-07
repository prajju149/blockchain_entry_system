import time
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Support both module import and direct execution
try:
    from .blockchain import Blockchain
    from .storage import Storage
    from .utils import (audio_fingerprint, generate_qr_for_resident,
                        image_fingerprint)
except ImportError:
    # Fallback for direct script execution
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from blockchain import Blockchain
    from storage import Storage
    from utils import (audio_fingerprint, generate_qr_for_resident,
                       image_fingerprint)

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=str(BASE_DIR / 'static'),
            template_folder=str(BASE_DIR / 'templates'))
CORS(app)  # Enable CORS for all routes

storage = Storage(BASE_DIR / 'data')
chain = Blockchain(str(BASE_DIR / 'chain.json'), storage.master_key())


# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f'Error: {str(error)}', exc_info=True)
    return jsonify({'error': str(error)}), 500


@app.route('/')
def index():
    # Serve the web dashboard file which is outside server/ in web/
    try:
        return send_from_directory('../web', 'dashboard.html')
    except Exception as e:
        app.logger.error(f'Index route error: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500



@app.route('/api/register', methods=['POST'])
def register():
    try:
        name = request.form.get('name')
        room = request.form.get('room')
        if not name or not room:
            return jsonify({'error': 'name and room required'}), 400

        # Extract additional resident fields
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        floor = request.form.get('floor', '').strip()
        moveInDate = request.form.get('moveInDate', '').strip()
        occupation = request.form.get('occupation', '').strip()
        emergencyContact = request.form.get('emergencyContact', '').strip()

        # Biometric files
        photo = request.files.get('photo')
        voice = request.files.get('voice')

        # Create resident with all fields
        resident = storage.create_resident(
            name,
            room,
            email=email if email else None,
            phone=phone if phone else None,
            address=address if address else None,
            floor=floor if floor else None,
            moveInDate=moveInDate if moveInDate else None,
            occupation=occupation if occupation else None,
            emergencyContact=emergencyContact if emergencyContact else None
        )
        if photo:
            photo_path = storage.save_resident_photo(resident['id'], photo)
            resident['photo_fp'] = image_fingerprint(photo_path)
        if voice:
            voice_path = storage.save_resident_voice(resident['id'], voice)
            resident['voice_fp'] = audio_fingerprint(voice_path)
        storage.update_resident(resident['id'], resident)
        qr_path = generate_qr_for_resident(resident, storage)
        return jsonify({'resident': resident, 'qr': qr_path})
    except Exception as e:
        app.logger.error(f'Register error: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan', methods=['POST'])
def scan():
    try:
        data = request.json or {}
        mode = data.get('mode')
        if not mode:
            return jsonify({'error': 'mode required'}), 400
        resident = None
        if data.get('resident_id'):
            resident = storage.get_resident(data['resident_id'])
        elif data.get('qr_data'):
            resident = storage.get_resident(data['qr_data'])
        if not resident:
            return jsonify({'error': 'resident not found'}), 404
        ok = False
        details = {}
        if mode == 'qr':
            ok = True
        elif mode == 'face':
            photo_b64 = data.get('photo_b64')
            if not photo_b64:
                return jsonify({'error': 'photo_b64 required for face mode'}), 400
            temp_path = storage.save_temp_b64('temp_face.jpg', photo_b64)
            fp = image_fingerprint(temp_path)
            ok = (fp == resident.get('photo_fp'))
            details = {'fp': fp, 'expected': resident.get('photo_fp')}
        elif mode == 'voice':
            audio_b64 = data.get('audio_b64')
            if not audio_b64:
                return jsonify({'error': 'audio_b64 required for voice mode'}), 400
            temp_path = storage.save_temp_b64('temp_voice.wav', audio_b64)
            fp = audio_fingerprint(temp_path)
            ok = (fp == resident.get('voice_fp'))
            details = {'fp': fp, 'expected': resident.get('voice_fp')}
        event = {
            'resident_id': resident['id'],
            'name': resident['name'],
            'mode': mode,
            'success': bool(ok),
            'ts': time.time()
        }
        chain.add_block(event)
        return jsonify({'ok': bool(ok), 'event': event, 'details': details})
    except Exception as e:
        app.logger.error(f'Scan error: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500



@app.route('/api/residents', methods=['GET'])
def list_residents():
    try:
        return jsonify({'residents': storage.list_residents()})
    except Exception as e:
        app.logger.error(f'List residents error: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/ledger', methods=['GET'])
def get_ledger():
    try:
        return jsonify(chain.load_chain())
    except Exception as e:
        app.logger.error(f'Get ledger error: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/web/<path:filename>')
def web_files(filename):
    return send_from_directory('../web', filename)


if __name__ == '__main__':
    app.run(debug=True)
