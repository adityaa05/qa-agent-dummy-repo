"""
API Controller for user settings
"""

from flask import jsonify, request
from src.settings.theme import ThemeManager

theme_manager = ThemeManager()

def toggle_theme_endpoint():
    """POST /api/settings/theme/toggle"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    try:
        new_theme = theme_manager.toggle_theme(user_id)
        return jsonify({
            'success': True,
            'theme': new_theme
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def get_theme_endpoint():
    """GET /api/settings/theme"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    theme = theme_manager.get_user_theme(user_id)
    return jsonify({
        'user_id': user_id,
        'theme': theme
    }), 200
