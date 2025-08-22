#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance-IA Tone & LGPD Reviewer - Serviço HTTP

Serviço HTTP Flask para revisão automatizada de ideias de conteúdo
com integração OpenAI e gerenciamento seguro de chaves API.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from functools import wraps
from typing import Dict, Any, Tuple, Optional

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv não está instalado, usar apenas variáveis de ambiente do sistema
    pass

from flask import Flask, request, jsonify

# Importar módulos do revisor
from interface_revisor import InterfaceRevisor
from revisor_hibrido import TipoRevisor

# Configurar logging seguro
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações
AUTH_TOKEN = os.getenv('AUTH_TOKEN', 'finance-ia-reviewer-token')
REQUIRED_HEADERS = ['Content-Type']

class APIKeyManager:
    """Gerenciador seguro de chaves OpenAI"""
    
    @staticmethod
    def extract_api_key(request_obj) -> Tuple[Optional[str], Optional[str]]:
        """
        Extrai chave OpenAI seguindo ordem de prioridade:
        1. Header X-OPENAI-API-KEY (preferencial)
        2. Body JSON campo openai_api_key (opcional)
        3. Variável de ambiente OPENAI_API_KEY (fallback)
        
        Returns:
            Tuple[api_key, source] onde source indica a origem
        """
        # 1. Verificar header (prioridade máxima)
        api_key = request_obj.headers.get('X-OPENAI-API-KEY')
        if api_key and api_key.strip():
            return api_key.strip(), 'header'
        
        # 2. Verificar body JSON (opcional)
        try:
            if request_obj.is_json and request_obj.json:
                body_key = request_obj.json.get('openai_api_key')
                if body_key and str(body_key).strip():
                    return str(body_key).strip(), 'body'
        except Exception:
            pass  # Ignorar erros de parsing JSON
        
        # 3. Verificar variável de ambiente (fallback)
        env_key = os.getenv('OPENAI_API_KEY')
        if env_key and env_key.strip():
            return env_key.strip(), 'environment'
        
        return None, None
    
    @staticmethod
    def mask_api_key(api_key: str) -> str:
        """
        Mascara chave API para logs seguros
        Mostra apenas os 4 últimos caracteres
        """
        if not api_key or len(api_key) < 8:
            return "***masked***"
        return f"***{api_key[-4:]}"
    
    @staticmethod
    def sanitize_request_for_log(request_obj) -> Dict[str, Any]:
        """
        Remove dados sensíveis da requisição para log seguro
        """
        safe_data = {
            'method': request_obj.method,
            'path': request_obj.path,
            'content_type': request_obj.content_type,
            'user_agent': request_obj.headers.get('User-Agent', 'unknown')
        }
        
        # Incluir body sem chaves sensíveis
        if request_obj.is_json:
            try:
                body = request_obj.json.copy() if request_obj.json else {}
                # Remover chave OpenAI do body para log
                if 'openai_api_key' in body:
                    body['openai_api_key'] = '***masked***'
                safe_data['body'] = body
            except Exception:
                safe_data['body'] = 'invalid_json'
        
        return safe_data

def require_auth(f):
    """Decorator para verificar autenticação do agente"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'missing_authorization',
                'hint': 'Envie Authorization: Bearer <AUTH_TOKEN>'
            }), 401
        
        token = auth_header.replace('Bearer ', '').strip()
        if token != AUTH_TOKEN:
            return jsonify({
                'error': 'invalid_authorization',
                'hint': 'Token de autorização inválido'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def require_openai_key(f):
    """Decorator para verificar e extrair chave OpenAI"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key, source = APIKeyManager.extract_api_key(request)
        
        if not api_key:
            return jsonify({
                'error': 'missing_openai_key',
                'hint': 'Envie em X-OPENAI-API-KEY ou defina OPENAI_API_KEY'
            }), 401
        
        # Log seguro da origem da chave
        masked_key = APIKeyManager.mask_api_key(api_key)
        logger.info(f"OpenAI key loaded from {source}: {masked_key}")
        
        # Passar chave para a função
        return f(api_key, *args, **kwargs)
    return decorated_function

@app.errorhandler(Exception)
def handle_exception(e):
    """Handler global de exceções com logs seguros"""
    trace_id = str(uuid.uuid4())
    
    # Log interno com trace_id
    logger.error(f"Internal error [{trace_id}]: {str(e)}", exc_info=True)
    
    # Resposta sanitizada para cliente
    return jsonify({
        'error': 'internal_error',
        'trace_id': trace_id
    }), 500

@app.before_request
def log_request():
    """Log seguro de requisições"""
    safe_request = APIKeyManager.sanitize_request_for_log(request)
    logger.info(f"Request: {json.dumps(safe_request)}")

@app.route('/healthz', methods=['GET'])
def healthcheck():
    """Endpoint de healthcheck sem dependência da OpenAI"""
    return jsonify({
        'status': 'healthy',
        'service': 'finance-ia-reviewer',
        'version': '2.0.0'
    }), 200

@app.route('/revisar', methods=['POST'])
@require_auth
@require_openai_key
def revisar_ideia(openai_api_key: str):
    """
    Endpoint para revisão de ideias de conteúdo
    
    Headers:
        Authorization: Bearer <AUTH_TOKEN>
        X-OPENAI-API-KEY: <chave_openai> (preferencial)
        Content-Type: application/json
    
    Body:
        {
            "ideia": { ... },  // Objeto da ideia a ser revisada
            "tipo_revisor": "auto",  // local, openai_client, openai_agent, hibrido, auto
            "incluir_comparacao": false,  // Opcional
            "openai_api_key": "..."  // Opcional se não vier no header
        }
    """
    try:
        # Validar JSON
        if not request.is_json:
            return jsonify({
                'error': 'invalid_content_type',
                'hint': 'Content-Type deve ser application/json'
            }), 400
        
        data = request.json
        if not data:
            return jsonify({
                'error': 'empty_body',
                'hint': 'Body JSON é obrigatório'
            }), 400
        
        # Extrair parâmetros
        ideia = data.get('ideia')
        if not ideia:
            return jsonify({
                'error': 'missing_ideia',
                'hint': 'Campo "ideia" é obrigatório'
            }), 400
        
        tipo_revisor = data.get('tipo_revisor', 'auto')
        incluir_comparacao = data.get('incluir_comparacao', False)
        
        # Inicializar revisor com IA
        interface = InterfaceRevisor(usar_ia=True, api_key=openai_api_key)
        
        # Processar revisão
        resultado = interface.revisar_ideia_dict(
            ideia=ideia,
            tipo_revisor=tipo_revisor,
            incluir_comparacao=incluir_comparacao
        )
        
        # Log de sucesso (sem dados sensíveis)
        logger.info(f"Revisão concluída com sucesso - tipo: {tipo_revisor}")
        
        return jsonify(resultado), 200
        
    except ValueError as e:
        # Erro de validação
        return jsonify({
            'error': 'validation_error',
            'detail': str(e)
        }), 400
        
    except Exception as e:
        # Verificar se é erro da OpenAI
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ['openai', 'api key', 'unauthorized', 'quota']):
            return jsonify({
                'error': 'openai_client_error',
                'detail': 'Erro na comunicação com OpenAI - verifique a chave'
            }), 502
        
        # Re-raise para handler global
        raise

@app.route('/testar', methods=['POST'])
@require_auth
@require_openai_key
def testar_revisores(openai_api_key: str):
    """
    Endpoint para testar todos os revisores disponíveis
    
    Body:
        {
            "ideia": { ... }  // Objeto da ideia a ser testada
        }
    """
    try:
        if not request.is_json or not request.json:
            return jsonify({
                'error': 'invalid_request',
                'hint': 'Body JSON com campo "ideia" é obrigatório'
            }), 400
        
        ideia = request.json.get('ideia')
        if not ideia:
            return jsonify({
                'error': 'missing_ideia',
                'hint': 'Campo "ideia" é obrigatório'
            }), 400
        
        # Inicializar revisor
        interface = InterfaceRevisor(usar_ia=True, api_key=openai_api_key)
        
        # Testar todos os revisores
        resultados = interface.testar_todos_revisores(ideia)
        
        logger.info("Teste de todos os revisores concluído")
        
        return jsonify(resultados), 200
        
    except Exception as e:
        # Verificar se é erro da OpenAI
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ['openai', 'api key', 'unauthorized']):
            return jsonify({
                'error': 'openai_client_error',
                'detail': 'Erro na comunicação com OpenAI'
            }), 502
        
        raise

@app.route('/estatisticas', methods=['GET'])
@require_auth
@require_openai_key
def obter_estatisticas(openai_api_key: str):
    """
    Endpoint para obter estatísticas de uso
    """
    try:
        interface = InterfaceRevisor(usar_ia=True, api_key=openai_api_key)
        stats = interface.obter_estatisticas()
        
        return jsonify(stats), 200
        
    except Exception as e:
        raise

@app.route('/template', methods=['GET'])
@require_auth
def gerar_template():
    """
    Endpoint para gerar template de ideia (não requer OpenAI)
    """
    try:
        interface = InterfaceRevisor(usar_ia=False)
        template = interface.gerar_template_ideia()
        
        return jsonify(template), 200
        
    except Exception as e:
        raise

@app.route('/listas', methods=['GET'])
@require_auth
def obter_listas_validas():
    """
    Endpoint para obter listas de valores válidos (não requer OpenAI)
    """
    try:
        interface = InterfaceRevisor(usar_ia=False)
        listas = interface.obter_listas_validas()
        
        return jsonify(listas), 200
        
    except Exception as e:
        raise

if __name__ == '__main__':
    # Configurações para desenvolvimento
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Iniciando Finance-IA Reviewer Service na porta {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )