#!/usr/bin/env python3
"""
Cliente OpenAI para Finance-IA Reviewer

Este módulo implementa um cliente simplificado para a API OpenAI,
focado em análise de conteúdo financeiro com integração às listas de validação.

Autor: Finance-IA Team
Versão: 2.0.0
Data: 2024
"""

import json
from typing import Dict, List, Optional, Any
from openai import OpenAI
from listas_validas import ListasValidas

class OpenAIClient:
    """Cliente simplificado para OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o cliente OpenAI
        
        Args:
            api_key: Chave da API OpenAI. Se não fornecida, usa variável de ambiente.
        """
        self.api_key = api_key or "sk-proj-YOUR_OPENAI_API_KEY_HERE"
        
        # Configurar cliente OpenAI
        self.client = OpenAI(api_key=self.api_key)
        
        # Carregar listas válidas
        self.listas = ListasValidas.obter_todas()
        
        # Configurações do modelo
        self.modelo = "gpt-3.5-turbo"
        self.temperatura = 0.3
        self.max_tokens = 1500
    
    def analisar_conteudo(self, conteudo: str, tipo_analise: str = "hibrido") -> Dict[str, Any]:
        """
        Analisa conteúdo usando OpenAI
        
        Args:
            conteudo: Texto a ser analisado
            tipo_analise: Tipo de análise (tom, lgpd, hibrido)
        
        Returns:
            Dicionário com resultado da análise
        """
        try:
            # Preparar prompt
            prompt = self._criar_prompt(conteudo, tipo_analise)
            
            # Fazer chamada para OpenAI
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperatura,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Processar resposta
            resultado = self._processar_resposta(response)
            
            # Adicionar metadados
            resultado['detalhes_ia'] = {
                'modelo': self.modelo,
                'tokens_usados': response.usage.total_tokens,
                'tokens_prompt': response.usage.prompt_tokens,
                'tokens_completion': response.usage.completion_tokens
            }
            
            return resultado
            
        except Exception as e:
            # Fallback em caso de erro
            return self._fallback_analysis(conteudo, str(e))
    
    def _get_system_prompt(self) -> str:
        """Retorna o prompt do sistema"""
        return f"""
        Você é um especialista em análise de conteúdo financeiro. Analise textos considerando:
        
        1. TOM E LINGUAGEM: Profissionalismo, clareza, ausência de pressão excessiva
        2. CONFORMIDADE LGPD: Transparência, consentimento, finalidade legítima
        3. SEGURANÇA: Ausência de características de phishing/fraude
        
        LISTAS DE REFERÊNCIA:
        - Palavras Suspeitas: {', '.join(self.listas['palavras_suspeitas'][:10])}...
        - Frases Problemáticas: {', '.join(self.listas['frases_problematicas'][:5])}...
        - Termos LGPD: {', '.join(self.listas['termos_lgpd'][:10])}...
        - Tom Inadequado: {', '.join(self.listas['palavras_tom_inadequado'][:10])}...
        
        Responda SEMPRE em JSON válido com:
        {{
            "score_conformidade": <0-100>,
            "classificacao": "<Excelente|Bom|Regular|Ruim|Crítico>",
            "problemas_encontrados": ["problema1", "problema2"],
            "sugestoes_melhoria": ["sugestao1", "sugestao2"],
            "analise_detalhada": "análise completa",
            "pontuacao_detalhada": {{
                "tom_linguagem": <0-100>,
                "conformidade_lgpd": <0-100>,
                "seguranca_confiabilidade": <0-100>
            }}
        }}
        
        CLASSIFICAÇÕES:
        - Excelente (90-100): Conteúdo exemplar
        - Bom (70-89): Adequado com pequenos ajustes
        - Regular (50-69): Aceitável mas precisa melhorias
        - Ruim (30-49): Problemático
        - Crítico (0-29): Inaceitável
        """
    
    def _criar_prompt(self, conteudo: str, tipo_analise: str) -> str:
        """Cria prompt específico para o tipo de análise"""
        base = f"Analise o seguinte conteúdo financeiro:\n\n{conteudo}\n\n"
        
        if tipo_analise == "tom":
            return base + "Foque especialmente na análise de tom e linguagem apropriada."
        elif tipo_analise == "lgpd":
            return base + "Foque especialmente na conformidade com LGPD e proteção de dados."
        else:  # hibrido
            return base + "Realize análise completa considerando tom, LGPD e segurança."
    
    def _processar_resposta(self, response) -> Dict[str, Any]:
        """Processa resposta da OpenAI"""
        try:
            # Extrair conteúdo JSON
            content = response.choices[0].message.content
            resultado = json.loads(content)
            
            # Validar e corrigir campos obrigatórios
            resultado = self._validar_resultado(resultado)
            
            return resultado
            
        except Exception as e:
            raise Exception(f"Erro ao processar resposta: {e}")
    
    def _validar_resultado(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Valida e corrige resultado da análise"""
        # Campos obrigatórios com valores padrão
        defaults = {
            'score_conformidade': 50,
            'classificacao': 'Regular',
            'problemas_encontrados': [],
            'sugestoes_melhoria': [],
            'analise_detalhada': 'Análise não disponível',
            'pontuacao_detalhada': {
                'tom_linguagem': 50,
                'conformidade_lgpd': 50,
                'seguranca_confiabilidade': 50
            }
        }
        
        # Aplicar defaults para campos ausentes
        for campo, valor_default in defaults.items():
            if campo not in resultado:
                resultado[campo] = valor_default
        
        # Validar score (0-100)
        score = resultado['score_conformidade']
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            resultado['score_conformidade'] = 50
        
        # Validar classificação
        classificacoes_validas = ['Excelente', 'Bom', 'Regular', 'Ruim', 'Crítico']
        if resultado['classificacao'] not in classificacoes_validas:
            score = resultado['score_conformidade']
            if score >= 90:
                resultado['classificacao'] = 'Excelente'
            elif score >= 70:
                resultado['classificacao'] = 'Bom'
            elif score >= 50:
                resultado['classificacao'] = 'Regular'
            elif score >= 30:
                resultado['classificacao'] = 'Ruim'
            else:
                resultado['classificacao'] = 'Crítico'
        
        # Garantir que listas são arrays
        for campo in ['problemas_encontrados', 'sugestoes_melhoria']:
            if not isinstance(resultado[campo], list):
                resultado[campo] = []
        
        return resultado
    
    def _fallback_analysis(self, conteudo: str, erro: str) -> Dict[str, Any]:
        """Análise de fallback usando regras básicas"""
        score = 70  # Score neutro
        problemas = []
        sugestoes = []
        
        conteudo_lower = conteudo.lower()
        
        # Verificar palavras suspeitas
        palavras_encontradas = []
        for palavra in self.listas['palavras_suspeitas']:
            if palavra.lower() in conteudo_lower:
                score -= 10
                palavras_encontradas.append(palavra)
        
        if palavras_encontradas:
            problemas.append(f"Palavras suspeitas: {', '.join(palavras_encontradas)}")
            sugestoes.append("Remover ou substituir palavras suspeitas")
        
        # Verificar frases problemáticas
        frases_encontradas = []
        for frase in self.listas['frases_problematicas']:
            if frase.lower() in conteudo_lower:
                score -= 15
                frases_encontradas.append(frase)
        
        if frases_encontradas:
            problemas.append(f"Frases problemáticas: {', '.join(frases_encontradas)}")
            sugestoes.append("Reformular frases problemáticas")
        
        # Verificar tom inadequado
        tom_inadequado = []
        for palavra in self.listas['palavras_tom_inadequado']:
            if palavra.lower() in conteudo_lower:
                score -= 5
                tom_inadequado.append(palavra)
        
        if tom_inadequado:
            problemas.append(f"Tom inadequado: {', '.join(tom_inadequado)}")
            sugestoes.append("Ajustar tom para mais profissional")
        
        # Verificações básicas de LGPD
        termos_lgpd_encontrados = []
        for termo in self.listas['termos_lgpd']:
            if termo.lower() in conteudo_lower:
                termos_lgpd_encontrados.append(termo)
        
        if not termos_lgpd_encontrados and len(conteudo) > 100:
            score -= 10
            problemas.append("Possível falta de informações sobre proteção de dados")
            sugestoes.append("Incluir informações sobre tratamento de dados pessoais")
        
        # Garantir score no range válido
        score = max(0, min(100, score))
        
        # Determinar classificação
        if score >= 90:
            classificacao = "Excelente"
        elif score >= 70:
            classificacao = "Bom"
        elif score >= 50:
            classificacao = "Regular"
        elif score >= 30:
            classificacao = "Ruim"
        else:
            classificacao = "Crítico"
        
        # Adicionar sugestões gerais se não houver específicas
        if not sugestoes:
            sugestoes = [
                "Revisar conteúdo manualmente",
                "Verificar conformidade com políticas internas",
                "Considerar revisão por especialista"
            ]
        
        return {
            'score_conformidade': score,
            'classificacao': classificacao,
            'problemas_encontrados': problemas,
            'sugestoes_melhoria': sugestoes,
            'analise_detalhada': f'Análise de fallback executada devido a erro na IA: {erro}. '
                               f'Score baseado em {len(problemas)} problemas identificados.',
            'pontuacao_detalhada': {
                'tom_linguagem': max(0, score - len(tom_inadequado) * 5),
                'conformidade_lgpd': max(0, score - (10 if not termos_lgpd_encontrados else 0)),
                'seguranca_confiabilidade': max(0, score - len(palavras_encontradas) * 10)
            },
            'erro_ia': erro,
            'modo_fallback': True
        }
    
    def testar_conexao(self) -> Dict[str, Any]:
        """Testa a conexão com a API OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "user", "content": "Responda apenas 'OK' se você pode me ouvir."}
                ],
                max_tokens=10
            )
            
            return {
                'status': 'sucesso',
                'modelo': self.modelo,
                'resposta': response.choices[0].message.content,
                'tokens_usados': response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'erro': str(e)
            }
    
    def obter_modelos_disponiveis(self) -> List[str]:
        """Obtém lista de modelos disponíveis"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if 'gpt' in model.id]
        except Exception as e:
            return ['gpt-3.5-turbo', 'gpt-4']  # Fallback
    
    def configurar_modelo(self, modelo: str, temperatura: float = None, max_tokens: int = None):
        """Configura parâmetros do modelo"""
        self.modelo = modelo
        if temperatura is not None:
            self.temperatura = max(0.0, min(2.0, temperatura))
        if max_tokens is not None:
            self.max_tokens = max(1, min(4000, max_tokens))
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do cliente"""
        return {
            'modelo': self.modelo,
            'temperatura': self.temperatura,
            'max_tokens': self.max_tokens,
            'listas_carregadas': {
                'palavras_suspeitas': len(self.listas['palavras_suspeitas']),
                'frases_problematicas': len(self.listas['frases_problematicas']),
                'termos_lgpd': len(self.listas['termos_lgpd']),
                'palavras_tom_inadequado': len(self.listas['palavras_tom_inadequado'])
            },
            'api_key_configurada': bool(self.api_key and self.api_key != "sk-proj-YOUR_OPENAI_API_KEY_HERE")
        }

# Função de conveniência
def analisar_rapido(conteudo: str, api_key: str, tipo: str = "hibrido") -> Dict[str, Any]:
    """
    Função de conveniência para análise rápida
    
    Args:
        conteudo: Texto a ser analisado
        api_key: Chave da API OpenAI
        tipo: Tipo de análise
    
    Returns:
        Resultado da análise
    """
    client = OpenAIClient(api_key)
    return client.analisar_conteudo(conteudo, tipo)

if __name__ == "__main__":
    # Teste básico
    print("🔧 Testando OpenAI Client...")
    
    # Verificar configuração
    client = OpenAIClient()
    stats = client.obter_estatisticas()
    
    print(f"Modelo: {stats['modelo']}")
    print(f"Listas carregadas: {stats['listas_carregadas']}")
    print(f"API Key configurada: {stats['api_key_configurada']}")
    
    if not stats['api_key_configurada']:
        print("⚠️ Configure sua API key OpenAI para testar funcionalidades completas!")
    else:
        # Teste de conexão
        print("\nTestando conexão...")
        teste = client.testar_conexao()
        print(f"Status: {teste['status']}")
        
        if teste['status'] == 'sucesso':
            # Teste de análise
            print("\nTestando análise...")
            resultado = client.analisar_conteudo(
                "Oferta especial! Ganhe dinheiro fácil!",
                "hibrido"
            )
            print(f"Score: {resultado['score_conformidade']}")
            print(f"Classificação: {resultado['classificacao']}")
        else:
            print(f"Erro na conexão: {teste['erro']}")