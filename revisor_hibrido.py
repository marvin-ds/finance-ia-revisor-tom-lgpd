#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revisor Híbrido - Finance-IA Tone & LGPD

Este módulo combina validações locais com inteligência artificial,
oferecendo múltiplas opções de revisão para ideias de conteúdo.
"""

import json
import time
from typing import Dict, List, Any, Optional, Literal
from enum import Enum

# Importar revisores
from revisor_tom_lgpd import RevisorTomLGPD
from openai_client import OpenAIRevisor
from openai_agent import FinanceIAAgent


class TipoRevisor(Enum):
    """Tipos de revisores disponíveis"""
    LOCAL = "local"
    OPENAI_CLIENT = "openai_client"
    OPENAI_AGENT = "openai_agent"
    HIBRIDO = "hibrido"
    AUTO = "auto"


class RevisorHibrido:
    """Revisor híbrido que combina validações locais com IA"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o revisor híbrido
        
        Args:
            api_key: Chave da API OpenAI (opcional)
        """
        # Inicializar revisores
        self.revisor_local = RevisorTomLGPD()
        
        try:
            self.openai_client = OpenAIRevisor(api_key)
            self.openai_agent = FinanceIAAgent(api_key)
            self.ia_disponivel = True
        except Exception as e:
            print(f"⚠️ IA não disponível: {str(e)}")
            self.openai_client = None
            self.openai_agent = None
            self.ia_disponivel = False
        
        # Estatísticas de uso
        self.stats = {
            "total_revisoes": 0,
            "revisoes_local": 0,
            "revisoes_client": 0,
            "revisoes_agent": 0,
            "revisoes_hibrido": 0,
            "erros_ia": 0,
            "tempo_medio": 0.0
        }
    
    def revisar_ideia(
        self,
        ideia: Dict[str, Any],
        tipo: TipoRevisor = TipoRevisor.AUTO,
        incluir_comparacao: bool = False
    ) -> Dict[str, Any]:
        """
        Revisa uma ideia usando o tipo de revisor especificado
        
        Args:
            ideia: Dicionário com os dados da ideia
            tipo: Tipo de revisor a usar
            incluir_comparacao: Se deve incluir comparação entre métodos
            
        Returns:
            Dict com resultado da revisão
        """
        inicio = time.time()
        self.stats["total_revisoes"] += 1
        
        try:
            if tipo == TipoRevisor.LOCAL:
                resultado = self._revisar_local(ideia)
                
            elif tipo == TipoRevisor.OPENAI_CLIENT:
                resultado = self._revisar_client(ideia)
                
            elif tipo == TipoRevisor.OPENAI_AGENT:
                resultado = self._revisar_agent(ideia)
                
            elif tipo == TipoRevisor.HIBRIDO:
                resultado = self._revisar_hibrido(ideia)
                
            elif tipo == TipoRevisor.AUTO:
                resultado = self._revisar_auto(ideia)
                
            else:
                raise ValueError(f"Tipo de revisor inválido: {tipo}")
            
            # Adicionar informações extras
            resultado["tipo_revisor_usado"] = tipo.value
            resultado["tempo_processamento"] = round(time.time() - inicio, 2)
            
            # Incluir comparação se solicitado
            if incluir_comparacao and tipo != TipoRevisor.LOCAL:
                resultado["comparacao"] = self._gerar_comparacao(ideia)
            
            # Atualizar estatísticas
            self._atualizar_stats(tipo, time.time() - inicio)
            
            return resultado
            
        except Exception as e:
            return {
                "erro": f"Erro no revisor híbrido: {str(e)}",
                "ideia_corrigida": ideia,
                "ajustes": ["Erro no processamento - ideia mantida sem alterações"],
                "tipo_revisor_usado": "erro",
                "tempo_processamento": round(time.time() - inicio, 2)
            }
    
    def _revisar_local(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Revisa usando apenas validações locais"""
        self.stats["revisoes_local"] += 1
        return self.revisor_local.revisar_ideia(ideia)
    
    def _revisar_client(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Revisa usando OpenAI Client"""
        if not self.ia_disponivel:
            return self._revisar_local(ideia)
        
        self.stats["revisoes_client"] += 1
        resultado = self.openai_client.revisar_com_fallback(ideia)
        
        if "erro" in resultado:
            self.stats["erros_ia"] += 1
        
        return resultado
    
    def _revisar_agent(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Revisa usando OpenAI Agent"""
        if not self.ia_disponivel:
            return self._revisar_local(ideia)
        
        self.stats["revisoes_agent"] += 1
        resultado = self.openai_agent.revisar_ideia_com_agente(ideia)
        
        if "erro" in resultado:
            self.stats["erros_ia"] += 1
            # Fallback para local
            return self._revisar_local(ideia)
        
        return resultado
    
    def _revisar_hibrido(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Revisa combinando validação local + refinamento com IA"""
        self.stats["revisoes_hibrido"] += 1
        
        # Primeira passada: validação local
        resultado_local = self._revisar_local(ideia)
        
        if not self.ia_disponivel:
            return resultado_local
        
        # Segunda passada: refinamento com IA
        try:
            ideia_pre_processada = resultado_local["ideia_corrigida"]
            resultado_ia = self.openai_client.revisar_ideia_com_ia(ideia_pre_processada)
            
            if "erro" not in resultado_ia:
                # Combinar ajustes
                ajustes_combinados = resultado_local["ajustes"] + [
                    "--- Refinamentos com IA ---"
                ] + resultado_ia["ajustes"]
                
                return {
                    "ideia_corrigida": resultado_ia["ideia_corrigida"],
                    "ajustes": ajustes_combinados[:8],  # Limitar a 8 ajustes
                    "metodo": "hibrido"
                }
        
        except Exception as e:
            print(f"⚠️ Erro no refinamento IA: {str(e)}")
            self.stats["erros_ia"] += 1
        
        # Fallback para resultado local
        return resultado_local
    
    def _revisar_auto(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Escolhe automaticamente o melhor método baseado na complexidade"""
        # Analisar complexidade da ideia
        complexidade = self._analisar_complexidade(ideia)
        
        if complexidade == "baixa":
            return self._revisar_local(ideia)
        elif complexidade == "media":
            return self._revisar_client(ideia)
        else:  # alta
            return self._revisar_agent(ideia)
    
    def _analisar_complexidade(self, ideia: Dict[str, Any]) -> Literal["baixa", "media", "alta"]:
        """Analisa a complexidade de uma ideia para escolher o revisor adequado"""
        pontos = 0
        
        # Verificar tema
        tema = ideia.get("tema", "")
        if len(tema) > 60:
            pontos += 2
        if any(palavra in tema.lower() for palavra in ["garanto", "100%", "rápido", "fácil"]):
            pontos += 3
        
        # Verificar inconsistências óbvias
        canal = ideia.get("canal", "")
        formato = ideia.get("formato", "")
        if (canal == "YouTube" and formato == "Carrossel") or \
           (canal == "Instagram" and formato == "YouTube Longo"):
            pontos += 2
        
        # Verificar CTA problemático
        cta = ideia.get("cta", "")
        if any(palavra in cta.lower() for palavra in ["email", "telefone", "cadastre"]):
            pontos += 2
        
        # Verificar persona vs tema
        persona = ideia.get("persona", "")
        if "iniciante" in persona.lower() and any(jargao in tema.lower() for jargao in ["alocação", "portfolio", "fluxo de caixa"]):
            pontos += 1
        
        # Classificar complexidade
        if pontos <= 2:
            return "baixa"
        elif pontos <= 5:
            return "media"
        else:
            return "alta"
    
    def _gerar_comparacao(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Gera comparação entre método local e IA"""
        try:
            resultado_local = self._revisar_local(ideia)
            
            return {
                "local": {
                    "tema": resultado_local["ideia_corrigida"]["tema"],
                    "ajustes_count": len(resultado_local["ajustes"]),
                    "principais_ajustes": resultado_local["ajustes"][:3]
                },
                "observacoes": "Comparação entre método local e IA para análise"
            }
        except Exception:
            return {"observacoes": "Comparação não disponível"}
    
    def _atualizar_stats(self, tipo: TipoRevisor, tempo: float):
        """Atualiza estatísticas de uso"""
        # Atualizar tempo médio
        total = self.stats["total_revisoes"]
        tempo_atual = self.stats["tempo_medio"]
        self.stats["tempo_medio"] = ((tempo_atual * (total - 1)) + tempo) / total
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas de uso do revisor"""
        stats = self.stats.copy()
        
        if stats["total_revisoes"] > 0:
            stats["taxa_erro_ia"] = round(
                (stats["erros_ia"] / stats["total_revisoes"]) * 100, 1
            )
            stats["distribuicao"] = {
                "local": round((stats["revisoes_local"] / stats["total_revisoes"]) * 100, 1),
                "client": round((stats["revisoes_client"] / stats["total_revisoes"]) * 100, 1),
                "agent": round((stats["revisoes_agent"] / stats["total_revisoes"]) * 100, 1),
                "hibrido": round((stats["revisoes_hibrido"] / stats["total_revisoes"]) * 100, 1)
            }
        
        stats["ia_disponivel"] = self.ia_disponivel
        stats["tempo_medio"] = round(stats["tempo_medio"], 2)
        
        return stats
    
    def testar_todos_revisores(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """Testa todos os revisores disponíveis com a mesma ideia"""
        resultados = {}
        
        # Testar revisor local
        print("🔧 Testando revisor local...")
        resultados["local"] = self._revisar_local(ideia)
        
        if self.ia_disponivel:
            # Testar OpenAI Client
            print("🤖 Testando OpenAI Client...")
            resultados["client"] = self._revisar_client(ideia)
            
            # Testar OpenAI Agent
            print("🎯 Testando OpenAI Agent...")
            resultados["agent"] = self._revisar_agent(ideia)
            
            # Testar híbrido
            print("⚡ Testando método híbrido...")
            resultados["hibrido"] = self._revisar_hibrido(ideia)
        
        return resultados
    
    def resetar_estatisticas(self):
        """Reseta as estatísticas de uso"""
        self.stats = {
            "total_revisoes": 0,
            "revisoes_local": 0,
            "revisoes_client": 0,
            "revisoes_agent": 0,
            "revisoes_hibrido": 0,
            "erros_ia": 0,
            "tempo_medio": 0.0
        }
        print("📊 Estatísticas resetadas")


def main():
    """Função principal para demonstração"""
    print("=== REVISOR HÍBRIDO - FINANCE-IA ===")
    
    # Criar revisor híbrido
    revisor = RevisorHibrido()
    
    # Exemplo de ideia complexa
    ideia_complexa = {
        "data_da_semana": "2024-01-15",
        "tema": "Garanto que você vai ficar rico em 30 dias com alocação de ativos e diversificação de portfolio",
        "persona": "Pessoa física iniciante",
        "pilar": "Investimentos",
        "formato": "Carrossel",
        "canal": "YouTube",
        "cta": "Cadastre seu email e telefone para receber o método secreto",
        "kpi_principal": "Retenção (50%)",
        "status": "Ideia",
        "roteirizado_em": "",
        "publicado_em": "",
        "lgpd_ok": "Sim",
        "prioridade": "Alta",
        "links_assets": "",
        "observacoes": ""
    }
    
    print("\n🧪 Testando todos os revisores...")
    resultados = revisor.testar_todos_revisores(ideia_complexa)
    
    for tipo, resultado in resultados.items():
        print(f"\n--- RESULTADO {tipo.upper()} ---")
        if "erro" in resultado:
            print(f"❌ Erro: {resultado['erro']}")
        else:
            print(f"📝 Tema: {resultado['ideia_corrigida']['tema']}")
            print(f"🔧 Ajustes ({len(resultado['ajustes'])}): {resultado['ajustes'][:2]}")
    
    print("\n📊 Estatísticas finais:")
    stats = revisor.obter_estatisticas()
    for key, value in stats.items():
        if key != "distribuicao":
            print(f"  {key}: {value}")
    
    if "distribuicao" in stats:
        print("  Distribuição de uso:")
        for metodo, percent in stats["distribuicao"].items():
            print(f"    {metodo}: {percent}%")


if __name__ == "__main__":
    main()