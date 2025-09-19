from flask import jsonify

def error_400(msg="Solicitud incorrecta"):
    return jsonify({"msg": msg}), 400

def error_401(msg="Credenciales invalidas"):
    return jsonify({"msg": msg}), 401

def error_403(msg="No autorizado"):
    return jsonify({"msg": msg}), 403

def error_404(msg="Recurso no encontrado"):
    return jsonify({"msg": msg}), 404

def error_409(msg="Conflicto de datos"):
    return jsonify({"msg": msg}), 409

def error_500(msg="Error interno del servidor"):
    return jsonify({"msg": msg}), 500
