"""Flask routes for CPF validation API."""

from flask import Blueprint, request, jsonify
from app.validators import is_valid_cpf, get_cpf_info

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'CPF Validation API is running'
    }), 200


@bp.route('/validate', methods=['POST'])
def validate_cpf():
    """
    Validate a CPF.
    
    Request body:
    {
        "cpf": "12345678901"
    }
    
    Returns:
    {
        "cpf": "123.456.789-01",
        "is_valid": true
    }
    """
    data = request.get_json()
    
    if not data or 'cpf' not in data:
        return jsonify({
            'error': 'Missing CPF field in request body'
        }), 400
    
    cpf = data['cpf']
    
    if not isinstance(cpf, str):
        return jsonify({
            'error': 'CPF must be a string'
        }), 400
    
    is_valid = is_valid_cpf(cpf)
    info = get_cpf_info(cpf)
    
    return jsonify({
        'cpf': info['formatted'],
        'is_valid': is_valid,
        'original': cpf,
        'length': info['length']
    }), 200


@bp.route('/validate/<cpf>', methods=['GET'])
def validate_cpf_get(cpf):
    """
    Validate a CPF via GET request.
    
    URL parameter:
    /api/validate/12345678901
    
    Returns:
    {
        "cpf": "123.456.789-01",
        "is_valid": true
    }
    """
    is_valid = is_valid_cpf(cpf)
    info = get_cpf_info(cpf)
    
    return jsonify({
        'cpf': info['formatted'],
        'is_valid': is_valid,
        'original': cpf,
        'length': info['length']
    }), 200


@bp.route('/validate-batch', methods=['POST'])
def validate_batch():
    """
    Validate multiple CPFs.
    
    Request body:
    {
        "cpfs": ["12345678901", "98765432100"]
    }
    
    Returns:
    {
        "results": [
            {"cpf": "123.456.789-01", "is_valid": true},
            {"cpf": "987.654.321-00", "is_valid": false}
        ]
    }
    """
    data = request.get_json()
    
    if not data or 'cpfs' not in data:
        return jsonify({
            'error': 'Missing cpfs field in request body'
        }), 400
    
    cpfs = data['cpfs']
    
    if not isinstance(cpfs, list):
        return jsonify({
            'error': 'cpfs must be a list'
        }), 400
    
    results = []
    for cpf in cpfs:
        if not isinstance(cpf, str):
            results.append({
                'cpf': cpf,
                'is_valid': False,
                'error': 'CPF must be a string'
            })
            continue
        
        is_valid = is_valid_cpf(cpf)
        info = get_cpf_info(cpf)
        results.append({
            'cpf': info['formatted'],
            'is_valid': is_valid,
            'original': cpf
        })
    
    return jsonify({
        'results': results,
        'total': len(results),
        'valid_count': sum(1 for r in results if r.get('is_valid', False))
    }), 200


@bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error'
    }), 500
