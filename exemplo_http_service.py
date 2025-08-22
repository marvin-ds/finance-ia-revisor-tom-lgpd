#!/usr/bin/env python3
"""
Exemplo de uso do Finance-IA Reviewer via HTTP Service

Este exemplo demonstra como usar o sistema Finance-IA através de requisições HTTP,
perfeito para integração com outros sistemas, APIs ou automações.

Autor: Finance-IA Team
Versão: 2.0.0
Data: 2024
"""

import requests
import json
from typing import Dict, List, Optional, Any

# Configurações do serviço
SERVICE_URL = "http://localhost:5000"
AUTH_TOKEN = "finance-ia-reviewer-token"  # Token do agente
OPENAI_API_KEY = "sk-proj-YOUR_OPENAI_API_KEY_HERE"  # Sua chave OpenAI

class FinanceIAClient:
    """Cliente para o serviço HTTP Finance-IA Reviewer"""
    
    def __init__(self, base_url: str = SERVICE_URL, auth_token: str = AUTH_TOKEN):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica se o serviço está funcionando"""
        try:
            response = requests.get(f"{self.base_url}/healthz", headers=self.headers)
            return {
                'status': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': None
            }
        except Exception as e:
            return {
                'status': 500,
                'data': None,
                'error': str(e)
            }
    
    def revisar_conteudo(self, conteudo: str, tipo_revisor: str = "hibrido", 
                        usar_ia: bool = True, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Revisa conteúdo usando o serviço"""
        payload = {
            'conteudo': conteudo,
            'tipo_revisor': tipo_revisor,
            'usar_ia': usar_ia
        }
        
        if api_key:
            payload['api_key'] = api_key
        
        try:
            response = requests.post(
                f"{self.base_url}/revisar",
                headers=self.headers,
                json=payload
            )
            
            return {
                'status': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': response.json().get('error') if response.status_code != 200 else None
            }
        except Exception as e:
            return {
                'status': 500,
                'data': None,
                'error': str(e)
            }
    
    def testar_sistema(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Testa o sistema completo"""
        payload = {}
        if api_key:
            payload['api_key'] = api_key
        
        try:
            response = requests.post(
                f"{self.base_url}/testar",
                headers=self.headers,
                json=payload
            )
            
            return {
                'status': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': response.json().get('error') if response.status_code != 200 else None
            }
        except Exception as e:
            return {
                'status': 500,
                'data': None,
                'error': str(e)
            }
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema"""
        try:
            response = requests.get(f"{self.base_url}/estatisticas", headers=self.headers)
            return {
                'status': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': None
            }
        except Exception as e:
            return {
                'status': 500,
                'data': None,
                'error': str(e)
            }
    
    def obter_template(self) -> Dict[str, Any]:
        """Obtém template de exemplo"""
        try:
            response = requests.get(f"{self.base_url}/template", headers=self.headers)
            return {
                'status': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': None
            }
        except Exception as e:
            return {
                'status': 500,
                'data': None,
                'error': str(e)
            }
    
    def obter_listas_validas(self) -> Dict[str, Any]:
        """Obtém listas de validação"""
        try:
            response = requests.get(f"{self.base_url}/listas", headers=self.headers)
            return {
                'status': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': None
            }
        except Exception as e:
            return {
                'status': 500,
                'data': None,
                'error': str(e)
            }

def exemplo_uso_basico():
    """Exemplo básico de uso do cliente HTTP"""
    print("🌐 EXEMPLO DE USO VIA HTTP SERVICE")
    print("=" * 50)
    
    # Inicializar cliente
    client = FinanceIAClient()
    
    # 1. Verificar saúde do serviço
    print("\n1. 🏥 Verificando saúde do serviço...")
    health = client.health_check()
    if health['status'] == 200:
        print("✅ Serviço funcionando normalmente")
        print(f"📊 Status: {health['data']}")
    else:
        print(f"❌ Erro no serviço: {health['error']}")
        return
    
    # 2. Testar sistema
    print("\n2. 🧪 Testando sistema...")
    test_result = client.testar_sistema(api_key=OPENAI_API_KEY)
    if test_result['status'] == 200:
        print("✅ Teste do sistema concluído")
        print(f"📋 Resultados: {json.dumps(test_result['data'], indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Erro no teste: {test_result['error']}")
    
    # 3. Revisar conteúdo
    print("\n3. 📝 Revisando conteúdo...")
    conteudo_teste = """
    Prezado cliente,
    
    Informamos que sua conta foi BLOQUEADA devido a atividades suspeitas.
    Para desbloquear, clique no link: http://site-falso.com/desbloquear
    
    Atenciosamente,
    Banco XYZ
    """
    
    resultado = client.revisar_conteudo(
        conteudo=conteudo_teste,
        tipo_revisor="hibrido",
        usar_ia=True,
        api_key=OPENAI_API_KEY
    )
    
    if resultado['status'] == 200:
        print("✅ Revisão concluída")
        data = resultado['data']
        print(f"📊 Score de Conformidade: {data.get('score_conformidade', 'N/A')}")
        print(f"🎯 Classificação: {data.get('classificacao', 'N/A')}")
        
        if 'problemas_encontrados' in data and data['problemas_encontrados']:
            print("\n⚠️ Problemas encontrados:")
            for problema in data['problemas_encontrados']:
                print(f"  • {problema}")
        
        if 'sugestoes_melhoria' in data and data['sugestoes_melhoria']:
            print("\n💡 Sugestões de melhoria:")
            for sugestao in data['sugestoes_melhoria']:
                print(f"  • {sugestao}")
    else:
        print(f"❌ Erro na revisão: {resultado['error']}")
    
    # 4. Obter estatísticas
    print("\n4. 📈 Obtendo estatísticas...")
    stats = client.obter_estatisticas()
    if stats['status'] == 200:
        print("✅ Estatísticas obtidas")
        print(f"📊 Dados: {json.dumps(stats['data'], indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Erro ao obter estatísticas: {stats['error']}")

def exemplo_integracao_avancada():
    """Exemplo de integração avançada com tratamento de erros"""
    print("\n🚀 EXEMPLO DE INTEGRAÇÃO AVANÇADA")
    print("=" * 50)
    
    client = FinanceIAClient()
    
    # Lista de conteúdos para revisar
    conteudos = [
        "Oferta especial! Ganhe R$ 10.000 em apenas 1 dia!",
        "Prezado cliente, sua fatura vence amanhã. Valor: R$ 150,00",
        "URGENTE: Sua conta será cancelada! Clique aqui: http://link-suspeito.com",
        "Obrigado por escolher nossos serviços. Atendimento: 0800-123-4567"
    ]
    
    resultados = []
    
    for i, conteudo in enumerate(conteudos, 1):
        print(f"\n📝 Revisando conteúdo {i}/{len(conteudos)}...")
        print(f"Texto: {conteudo[:50]}...")
        
        resultado = client.revisar_conteudo(
            conteudo=conteudo,
            tipo_revisor="hibrido",
            usar_ia=True,
            api_key=OPENAI_API_KEY
        )
        
        if resultado['status'] == 200:
            data = resultado['data']
            score = data.get('score_conformidade', 0)
            classificacao = data.get('classificacao', 'Desconhecida')
            
            print(f"✅ Score: {score} | Classificação: {classificacao}")
            
            resultados.append({
                'conteudo': conteudo,
                'score': score,
                'classificacao': classificacao,
                'problemas': data.get('problemas_encontrados', []),
                'sugestoes': data.get('sugestoes_melhoria', [])
            })
        else:
            print(f"❌ Erro: {resultado['error']}")
            resultados.append({
                'conteudo': conteudo,
                'erro': resultado['error']
            })
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL")
    print("=" * 30)
    
    scores_validos = [r['score'] for r in resultados if 'score' in r]
    if scores_validos:
        media_score = sum(scores_validos) / len(scores_validos)
        print(f"📈 Score médio: {media_score:.2f}")
        print(f"🎯 Melhor score: {max(scores_validos)}")
        print(f"⚠️ Pior score: {min(scores_validos)}")
    
    problemas_totais = sum(len(r.get('problemas', [])) for r in resultados)
    print(f"🚨 Total de problemas encontrados: {problemas_totais}")
    
    return resultados

def exemplo_monitoramento_continuo():
    """Exemplo de monitoramento contínuo do serviço"""
    print("\n🔄 EXEMPLO DE MONITORAMENTO CONTÍNUO")
    print("=" * 50)
    
    client = FinanceIAClient()
    
    import time
    
    print("Monitorando serviço por 30 segundos...")
    
    start_time = time.time()
    checks = 0
    successful_checks = 0
    
    while time.time() - start_time < 30:
        health = client.health_check()
        checks += 1
        
        if health['status'] == 200:
            successful_checks += 1
            print(f"✅ Check {checks}: OK")
        else:
            print(f"❌ Check {checks}: FALHA - {health['error']}")
        
        time.sleep(5)  # Aguarda 5 segundos
    
    uptime_percentage = (successful_checks / checks) * 100
    print(f"\n📊 Relatório de Monitoramento:")
    print(f"🔍 Total de verificações: {checks}")
    print(f"✅ Verificações bem-sucedidas: {successful_checks}")
    print(f"📈 Uptime: {uptime_percentage:.1f}%")

if __name__ == "__main__":
    try:
        # Executar exemplos
        exemplo_uso_basico()
        
        print("\n" + "="*70)
        exemplo_integracao_avancada()
        
        print("\n" + "="*70)
        # exemplo_monitoramento_continuo()  # Descomente para testar monitoramento
        
        print("\n🎉 Todos os exemplos foram executados com sucesso!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()