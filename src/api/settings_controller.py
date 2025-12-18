# src/api/settings_controller.py
from flask import jsonify, request
from src.settings.theme import ThemeManager

def toggle_theme_endpoint():
    """API endpoint to toggle user theme"""
    user_id = request.json.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    theme_manager = ThemeManager(user_id)
    new_theme = theme_manager.toggle_theme()
    
    return jsonify({
        "success": True,
        "theme": new_theme,
        "message": f"Theme switched to {new_theme} mode"
    }), 200

def get_theme_endpoint():
    """API endpoint to get current theme"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    theme_manager = ThemeManager(user_id)
    current_theme = theme_manager.get_current_theme()
    
    return jsonify({
        "theme": current_theme
    }), 200
