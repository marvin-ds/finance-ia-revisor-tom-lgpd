#!/usr/bin/env python3
"""
Agente OpenAI para Finance-IA Reviewer

Este módulo implementa um agente inteligente usando a API OpenAI Assistants
para análise avançada de conteúdo financeiro com foco em tom e LGPD.

Autor: Finance-IA Team
Versão: 2.0.0
Data: 2024
"""

import json
import time
from typing import Dict, List, Optional, Any
from openai import OpenAI
from listas_validas import ListasValidas

class OpenAIAgent:
    """Agente OpenAI para análise de conteúdo financeiro"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o agente OpenAI
        
        Args:
            api_key: Chave da API OpenAI
        """
        self.api_key = api_key or "sk-proj-YOUR_OPENAI_API_KEY_HERE"
        
        # Configurar cliente OpenAI
        self.client = OpenAI(api_key=self.api_key)
        
        # Carregar listas válidas
        self.listas = ListasValidas.obter_todas()
        
        # IDs do assistente e thread (serão criados dinamicamente)
        self.assistant_id = None
        self.thread_id = None
        
        # Configurações do modelo
        self.modelo = "gpt-4-1106-preview"
        self.temperatura = 0.3
        self.max_tokens = 2000
    
    def _criar_assistente(self) -> str:
        """Cria um assistente OpenAI especializado"""
        if self.assistant_id:
            return self.assistant_id
        
        # Instruções detalhadas para o assistente
        instrucoes = f"""
        Você é um especialista em análise de conteúdo financeiro com foco em:
        1. Tom e linguagem apropriada para comunicação financeira
        2. Conformidade com LGPD (Lei Geral de Proteção de Dados)
        3. Identificação de práticas suspeitas ou fraudulentas
        
        LISTAS DE REFERÊNCIA:
        
        Palavras Suspeitas: {', '.join(self.listas['palavras_suspeitas'])}
        
        Frases Problemáticas: {', '.join(self.listas['frases_problematicas'])}
        
        Termos LGPD: {', '.join(self.listas['termos_lgpd'])}
        
        Palavras de Tom Inadequado: {', '.join(self.listas['palavras_tom_inadequado'])}
        
        CRITÉRIOS DE ANÁLISE:
        
        1. TOM E LINGUAGEM (0-100 pontos):
           - Linguagem profissional e respeitosa
           - Ausência de urgência excessiva ou pressão
           - Tom adequado ao contexto financeiro
           - Clareza e objetividade
        
        2. CONFORMIDADE LGPD (0-100 pontos):
           - Transparência no uso de dados
           - Consentimento adequado
           - Finalidade específica e legítima
           - Direitos do titular respeitados
        
        3. SEGURANÇA E CONFIABILIDADE (0-100 pontos):
           - Ausência de características de phishing/fraude
           - Links e contatos legítimos
           - Informações verificáveis
           - Práticas éticas
        
        FORMATO DE RESPOSTA:
        Responda SEMPRE em JSON com a seguinte estrutura:
        {{
            "score_conformidade": <número de 0 a 100>,
            "classificacao": "<Excelente|Bom|Regular|Ruim|Crítico>",
            "problemas_encontrados": ["problema1", "problema2", ...],
            "sugestoes_melhoria": ["sugestao1", "sugestao2", ...],
            "analise_detalhada": "<análise completa do conteúdo>",
            "pontuacao_detalhada": {{
                "tom_linguagem": <0-100>,
                "conformidade_lgpd": <0-100>,
                "seguranca_confiabilidade": <0-100>
            }}
        }}
        
        CLASSIFICAÇÕES:
        - Excelente (90-100): Conteúdo exemplar
        - Bom (70-89): Conteúdo adequado com pequenos ajustes
        - Regular (50-69): Conteúdo aceitável mas precisa melhorias
        - Ruim (30-49): Conteúdo problemático
        - Crítico (0-29): Conteúdo inaceitável
        """
        
        try:
            assistant = self.client.beta.assistants.create(
                name="Finance-IA Reviewer",
                instructions=instrucoes,
                model=self.modelo,
                tools=[{"type": "code_interpreter"}]
            )
            
            self.assistant_id = assistant.id
            return self.assistant_id
            
        except Exception as e:
            raise Exception(f"Erro ao criar assistente: {e}")
    
    def _criar_thread(self) -> str:
        """Cria uma nova thread de conversa"""
        try:
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id
            return self.thread_id
        except Exception as e:
            raise Exception(f"Erro ao criar thread: {e}")
    
    def analisar_conteudo(self, conteudo: str, tipo_analise: str = "hibrido") -> Dict[str, Any]:
        """
        Analisa conteúdo usando o agente OpenAI
        
        Args:
            conteudo: Texto a ser analisado
            tipo_analise: Tipo de análise (tom, lgpd, hibrido)
        
        Returns:
            Dicionário com resultado da análise
        """
        try:
            # Criar assistente se necessário
            if not self.assistant_id:
                self._criar_assistente()
            
            # Criar thread se necessário
            if not self.thread_id:
                self._criar_thread()
            
            # Preparar prompt específico baseado no tipo
            prompt_especifico = self._preparar_prompt(conteudo, tipo_analise)
            
            # Enviar mensagem
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=prompt_especifico
            )
            
            # Executar assistente
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )
            
            # Aguardar conclusão
            resultado = self._aguardar_conclusao(run.id)
            
            # Processar resposta
            return self._processar_resposta(resultado)
            
        except Exception as e:
            # Fallback em caso de erro
            return self._fallback_analysis(conteudo, str(e))
    
    def _preparar_prompt(self, conteudo: str, tipo_analise: str) -> str:
        """Prepara prompt específico para o tipo de análise"""
        base_prompt = f"Analise o seguinte conteúdo financeiro:\n\n{conteudo}\n\n"
        
        if tipo_analise == "tom":
            return base_prompt + "Foque especialmente na análise de tom e linguagem."
        elif tipo_analise == "lgpd":
            return base_prompt + "Foque especialmente na conformidade com LGPD."
        else:  # hibrido
            return base_prompt + "Realize uma análise completa considerando tom, LGPD e segurança."
    
    def _aguardar_conclusao(self, run_id: str, timeout: int = 60) -> str:
        """Aguarda a conclusão da execução do assistente"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_id
            )
            
            if run.status == "completed":
                # Obter mensagens
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                
                # Retornar última mensagem do assistente
                for message in messages.data:
                    if message.role == "assistant":
                        return message.content[0].text.value
                
                raise Exception("Nenhuma resposta do assistente encontrada")
            
            elif run.status == "failed":
                raise Exception(f"Execução falhou: {run.last_error}")
            
            elif run.status == "requires_action":
                # Lidar com ações necessárias se houver
                pass
            
            time.sleep(2)
        
        raise Exception("Timeout na execução do assistente")
    
    def _processar_resposta(self, resposta: str) -> Dict[str, Any]:
        """Processa a resposta JSON do assistente"""
        try:
            # Tentar extrair JSON da resposta
            inicio_json = resposta.find('{')
            fim_json = resposta.rfind('}') + 1
            
            if inicio_json != -1 and fim_json > inicio_json:
                json_str = resposta[inicio_json:fim_json]
                resultado = json.loads(json_str)
                
                # Validar estrutura
                campos_obrigatorios = [
                    'score_conformidade', 'classificacao', 
                    'problemas_encontrados', 'sugestoes_melhoria'
                ]
                
                for campo in campos_obrigatorios:
                    if campo not in resultado:
                        resultado[campo] = self._valor_padrao(campo)
                
                # Garantir que score está no range correto
                resultado['score_conformidade'] = max(0, min(100, resultado['score_conformidade']))
                
                return resultado
            
            else:
                raise ValueError("JSON não encontrado na resposta")
                
        except Exception as e:
            return self._fallback_analysis("", f"Erro ao processar resposta: {e}")
    
    def _valor_padrao(self, campo: str) -> Any:
        """Retorna valor padrão para campos obrigatórios"""
        defaults = {
            'score_conformidade': 50,
            'classificacao': 'Regular',
            'problemas_encontrados': ['Erro na análise automática'],
            'sugestoes_melhoria': ['Revisar manualmente'],
            'analise_detalhada': 'Análise não disponível',
            'pontuacao_detalhada': {
                'tom_linguagem': 50,
                'conformidade_lgpd': 50,
                'seguranca_confiabilidade': 50
            }
        }
        return defaults.get(campo, None)
    
    def _fallback_analysis(self, conteudo: str, erro: str) -> Dict[str, Any]:
        """Análise de fallback em caso de erro"""
        # Análise básica usando as listas
        score = 70  # Score neutro
        problemas = []
        
        conteudo_lower = conteudo.lower()
        
        # Verificar palavras suspeitas
        for palavra in self.listas['palavras_suspeitas']:
            if palavra.lower() in conteudo_lower:
                score -= 10
                problemas.append(f"Palavra suspeita encontrada: {palavra}")
        
        # Verificar frases problemáticas
        for frase in self.listas['frases_problematicas']:
            if frase.lower() in conteudo_lower:
                score -= 15
                problemas.append(f"Frase problemática: {frase}")
        
        # Verificar tom inadequado
        for palavra in self.listas['palavras_tom_inadequado']:
            if palavra.lower() in conteudo_lower:
                score -= 5
                problemas.append(f"Tom inadequado: {palavra}")
        
        score = max(0, min(100, score))
        
        # Classificação baseada no score
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
        
        return {
            'score_conformidade': score,
            'classificacao': classificacao,
            'problemas_encontrados': problemas,
            'sugestoes_melhoria': ['Revisar conteúdo manualmente', 'Verificar conformidade'],
            'analise_detalhada': f'Análise de fallback devido a erro: {erro}',
            'pontuacao_detalhada': {
                'tom_linguagem': score,
                'conformidade_lgpd': score,
                'seguranca_confiabilidade': score
            },
            'erro_ia': erro
        }
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do agente"""
        return {
            'assistant_id': self.assistant_id,
            'thread_id': self.thread_id,
            'modelo': self.modelo,
            'temperatura': self.temperatura,
            'max_tokens': self.max_tokens,
            'listas_carregadas': len(self.listas),
            'status': 'ativo' if self.assistant_id else 'inativo'
        }
    
    def limpar_sessao(self):
        """Limpa a sessão atual (thread)"""
        self.thread_id = None
    
    def __del__(self):
        """Limpeza ao destruir o objeto"""
        try:
            # Opcional: limpar recursos se necessário
            pass
        except:
            pass

# Função de conveniência
def analisar_com_ia(conteudo: str, api_key: str, tipo_analise: str = "hibrido") -> Dict[str, Any]:
    """
    Função de conveniência para análise rápida
    
    Args:
        conteudo: Texto a ser analisado
        api_key: Chave da API OpenAI
        tipo_analise: Tipo de análise
    
    Returns:
        Resultado da análise
    """
    agent = OpenAIAgent(api_key)
    return agent.analisar_conteudo(conteudo, tipo_analise)

if __name__ == "__main__":
    # Teste básico
    print("🤖 Testando OpenAI Agent...")
    
    # Verificar se API key está configurada
    api_key = "sk-proj-YOUR_OPENAI_API_KEY_HERE"
    if api_key == "sk-proj-YOUR_OPENAI_API_KEY_HERE":
        print("⚠️ Configure sua API key OpenAI para testar!")
    else:
        try:
            agent = OpenAIAgent(api_key)
            
            conteudo_teste = """
            URGENTE! Sua conta será bloqueada!
            Clique aqui imediatamente: http://site-suspeito.com
            """
            
            resultado = agent.analisar_conteudo(conteudo_teste)
            print(f"Score: {resultado['score_conformidade']}")
            print(f"Classificação: {resultado['classificacao']}")
            print(f"Problemas: {len(resultado['problemas_encontrados'])}")
            
        except Exception as e:
            print(f"Erro no teste: {e}")