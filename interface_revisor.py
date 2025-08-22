#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Simplificada para o Revisor de Tom & LGPD do Finance-IA

Este módulo fornece uma interface amigável para usar o revisor,
com validação de entrada, formatação de saída e tratamento de erros.
Inclui suporte para revisão com IA (OpenAI).
"""

import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

from revisor_tom_lgpd import RevisorTomLGPD
from listas_validas import ListasValidas

try:
    from revisor_hibrido import RevisorHibrido, TipoRevisor
    IA_DISPONIVEL = True
except ImportError:
    IA_DISPONIVEL = False
    print("⚠️ Módulos de IA não disponíveis. Usando apenas revisor local.")


class InterfaceRevisor:
    """Interface simplificada para o revisor de tom e LGPD"""
    
    def __init__(self, usar_ia: bool = False, api_key: Optional[str] = None):
        """
        Inicializa a interface com o revisor
        
        Args:
            usar_ia: Se deve usar IA quando disponível
            api_key: Chave da API OpenAI (opcional)
        """
        self.revisor_local = RevisorTomLGPD()
        self.listas_validas = ListasValidas.obter_todas()
        
        # Configurar revisor híbrido se IA estiver disponível
        if usar_ia and IA_DISPONIVEL:
            try:
                self.revisor_hibrido = RevisorHibrido(api_key)
                self.usar_ia = True
                print("✅ Interface configurada com suporte à IA")
            except Exception as e:
                print(f"⚠️ Erro ao configurar IA: {str(e)}. Usando apenas revisor local.")
                self.revisor_hibrido = None
                self.usar_ia = False
        else:
            self.revisor_hibrido = None
            self.usar_ia = False
    
    def revisar_ideia_json(
        self, 
        ideia_json: str, 
        tipo_revisor: str = "auto",
        incluir_comparacao: bool = False
    ) -> str:
        """
        Revisa uma ideia recebida como JSON string
        
        Args:
            ideia_json: String JSON com a ideia a ser revisada
            tipo_revisor: Tipo de revisor (local, openai_client, openai_agent, hibrido, auto)
            incluir_comparacao: Se deve incluir comparação entre métodos
            
        Returns:
            String JSON com o resultado da revisão
        """
        try:
            # Parse do JSON de entrada
            ideia = json.loads(ideia_json)
            
            # Validar estrutura da ideia
            erro_validacao = self._validar_estrutura_ideia(ideia)
            if erro_validacao:
                return self._criar_resposta_erro(erro_validacao)
            
            # Revisar a ideia
            resultado = self.revisar_ideia_dict(ideia, tipo_revisor, incluir_comparacao)
            
            # Retornar resultado como JSON
            return json.dumps(resultado, ensure_ascii=False, indent=2)
            
        except json.JSONDecodeError as e:
            return self._criar_resposta_erro(f"JSON inválido: {str(e)}")
        except Exception as e:
            return self._criar_resposta_erro(f"Erro interno: {str(e)}")
    
    def revisar_ideia_dict(
        self, 
        ideia: Dict[str, Any], 
        tipo_revisor: str = "auto",
        incluir_comparacao: bool = False
    ) -> Dict[str, Any]:
        """
        Revisa uma ideia recebida como dicionário
        
        Args:
            ideia: Dicionário com a ideia a ser revisada
            tipo_revisor: Tipo de revisor (local, openai_client, openai_agent, hibrido, auto)
            incluir_comparacao: Se deve incluir comparação entre métodos
            
        Returns:
            Dicionário com o resultado da revisão
        """
        try:
            # Validar estrutura da ideia
            erro_validacao = self._validar_estrutura_ideia(ideia)
            if erro_validacao:
                return {
                    "erro": erro_validacao,
                    "ideia_corrigida": None,
                    "ajustes": []
                }
            
            # Escolher revisor
            if self.usar_ia and self.revisor_hibrido and tipo_revisor != "local":
                # Usar revisor híbrido
                try:
                    tipo_enum = TipoRevisor(tipo_revisor)
                    resultado = self.revisor_hibrido.revisar_ideia(
                        ideia, tipo_enum, incluir_comparacao
                    )
                except ValueError:
                    # Tipo inválido, usar local
                    resultado = self.revisor_local.revisar_ideia(ideia)
            else:
                # Usar revisor local
                resultado = self.revisor_local.revisar_ideia(ideia)
            
            return resultado
            
        except Exception as e:
            return {
                "erro": f"Erro interno: {str(e)}",
                "ideia_corrigida": None,
                "ajustes": []
            }
    
    def _validar_estrutura_ideia(self, ideia: Dict[str, Any]) -> Optional[str]:
        """Valida se a ideia tem a estrutura esperada"""
        campos_obrigatorios = [
            "data_da_semana", "tema", "persona", "pilar", "formato",
            "canal", "cta", "kpi_principal", "status", "roteirizado_em",
            "publicado_em", "lgpd_ok", "prioridade", "links_assets", "observacoes"
        ]
        
        # Verificar se todos os campos obrigatórios estão presentes
        campos_faltando = []
        for campo in campos_obrigatorios:
            if campo not in ideia:
                campos_faltando.append(campo)
        
        if campos_faltando:
            return f"Campos obrigatórios faltando: {', '.join(campos_faltando)}"
        
        # Validar formato da data
        try:
            datetime.strptime(ideia["data_da_semana"], "%Y-%m-%d")
        except ValueError:
            return "Campo 'data_da_semana' deve estar no formato YYYY-MM-DD"
        
        # Validar campos não vazios essenciais
        campos_essenciais = ["tema", "persona", "pilar", "formato", "canal"]
        campos_vazios = []
        for campo in campos_essenciais:
            if not ideia.get(campo, "").strip():
                campos_vazios.append(campo)
        
        if campos_vazios:
            return f"Campos essenciais não podem estar vazios: {', '.join(campos_vazios)}"
        
        return None
    
    def _criar_resposta_erro(self, mensagem_erro: str) -> str:
        """Cria uma resposta de erro formatada"""
        resposta_erro = {
            "erro": mensagem_erro,
            "ideia_corrigida": None,
            "ajustes": []
        }
        return json.dumps(resposta_erro, ensure_ascii=False, indent=2)
    
    def obter_listas_validas(self) -> Dict[str, Any]:
        """Retorna todas as listas de valores válidos"""
        return self.listas_validas
    
    def obter_listas_validas_json(self) -> str:
        """Retorna todas as listas de valores válidos como JSON"""
        return json.dumps(self.listas_validas, ensure_ascii=False, indent=2)
    
    def criar_ideia_template(self, data_semana: str = None) -> Dict[str, Any]:
        """Cria um template de ideia com valores padrão"""
        if not data_semana:
            data_semana = datetime.now().strftime("%Y-%m-%d")
        
        return {
            "data_da_semana": data_semana,
            "tema": "",
            "persona": self.listas_validas["personas"][0],
            "pilar": self.listas_validas["pilares"][0],
            "formato": self.listas_validas["formatos"][0],
            "canal": self.listas_validas["canais"][0],
            "cta": self.listas_validas["ctas"][0],
            "kpi_principal": self.listas_validas["kpis"][0],
            "status": "Ideia",
            "roteirizado_em": "",
            "publicado_em": "",
            "lgpd_ok": "Sim",
            "prioridade": self.listas_validas["prioridade"][1],  # Média
            "links_assets": "",
            "observacoes": ""
        }
    
    def validar_ideia_completa(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz uma validação completa da ideia sem modificá-la
        
        Returns:
            Dicionário com informações sobre a validação
        """
        resultado_validacao = {
            "valida": True,
            "erros": [],
            "avisos": [],
            "sugestoes": []
        }
        
        # Validar estrutura
        erro_estrutura = self._validar_estrutura_ideia(ideia)
        if erro_estrutura:
            resultado_validacao["valida"] = False
            resultado_validacao["erros"].append(erro_estrutura)
            return resultado_validacao
        
        # Validar valores das listas
        for campo, lista_key in {
            "persona": "personas",
            "pilar": "pilares",
            "formato": "formatos",
            "canal": "canais",
            "cta": "ctas",
            "kpi_principal": "kpis",
            "prioridade": "prioridade"
        }.items():
            valor = ideia.get(campo, "")
            if valor not in self.listas_validas[lista_key]:
                resultado_validacao["avisos"].append(
                    f"Valor '{valor}' em '{campo}' não está na lista válida"
                )
        
        # Verificar consistência canal/formato
        formato = ideia.get("formato", "")
        canal = ideia.get("canal", "")
        mapeamento = ListasValidas.get_mapeamento_canal_formato()
        
        canais_compativeis = []
        for c, formatos in mapeamento.items():
            if formato in formatos:
                canais_compativeis.append(c)
        
        if canal not in canais_compativeis and canais_compativeis:
            resultado_validacao["avisos"].append(
                f"Canal '{canal}' pode não ser compatível com formato '{formato}'. "
                f"Canais sugeridos: {', '.join(canais_compativeis)}"
            )
        
        # Verificar tema
        tema = ideia.get("tema", "")
        if len(tema) > 90:
            resultado_validacao["avisos"].append(
                f"Tema muito longo ({len(tema)} caracteres). Recomendado: até 90 caracteres."
            )
        
        # Verificar LGPD
        if self.revisor._contem_pii(tema):
            resultado_validacao["erros"].append(
                "Tema contém possíveis dados pessoais (PII)"
            )
            resultado_validacao["valida"] = False
        
        cta = ideia.get("cta", "")
        if self.revisor._cta_solicita_dados(cta):
            resultado_validacao["avisos"].append(
                "CTA pode estar solicitando dados pessoais"
            )
        
        return resultado_validacao


    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Obtém estatísticas de uso do revisor
        
        Returns:
            Dict com estatísticas ou mensagem se não disponível
        """
        if self.usar_ia and self.revisor_hibrido:
            return self.revisor_hibrido.obter_estatisticas()
        else:
            return {"status": "Estatísticas disponíveis apenas com IA habilitada"}
    
    def testar_todos_revisores(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Testa todos os revisores disponíveis
        
        Args:
            ideia: Dicionário com os dados da ideia
            
        Returns:
            Dict com resultados de todos os revisores
        """
        if self.usar_ia and self.revisor_hibrido:
            return self.revisor_hibrido.testar_todos_revisores(ideia)
        else:
            return {
                "local": self.revisor_local.revisar_ideia(ideia),
                "observacao": "Apenas revisor local disponível"
            }


def processar_linha_comando():
    """Processa argumentos da linha de comando"""
    if len(sys.argv) < 2:
        print("Uso: python interface_revisor.py <comando> [argumentos]")
        print("Comandos:")
        print("  revisar <arquivo.json> [tipo] [--comparacao]  - Revisa ideia")
        print("    tipos: local, openai_client, openai_agent, hibrido, auto")
        print("  template                                      - Gera template")
        print("  listas                                        - Mostra listas válidas")
        print("  stats                                         - Mostra estatísticas")
        print("  testar <arquivo.json>                         - Testa todos revisores")
        return
    
    comando = sys.argv[1].lower()
    
    # Verificar se deve usar IA
    usar_ia = "--ia" in sys.argv or any(arg in ["openai_client", "openai_agent", "hibrido"] for arg in sys.argv)
    interface = InterfaceRevisor(usar_ia=usar_ia)
    
    if comando == "revisar":
        if len(sys.argv) < 3:
            print("❌ Erro: Especifique o arquivo JSON")
            return
        
        arquivo = sys.argv[2]
        tipo_revisor = sys.argv[3] if len(sys.argv) > 3 else "auto"
        incluir_comparacao = "--comparacao" in sys.argv
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            resultado = interface.revisar_ideia_json(
                conteudo, tipo_revisor, incluir_comparacao
            )
            print(resultado)
            
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo '{arquivo}' não encontrado")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    elif comando == "template":
        template = interface.criar_ideia_template()
        print(json.dumps(template, ensure_ascii=False, indent=2))
    
    elif comando == "listas":
        listas = interface.obter_listas_validas()
        print(json.dumps(listas, ensure_ascii=False, indent=2))
    
    elif comando == "stats":
        stats = interface.obter_estatisticas()
        print("\n📊 ESTATÍSTICAS DE USO:")
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif comando == "testar":
        if len(sys.argv) < 3:
            print("❌ Erro: Especifique o arquivo JSON")
            return
        
        arquivo = sys.argv[2]
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                ideia = json.load(f)
            
            resultados = interface.testar_todos_revisores(ideia)
            print("\n🧪 TESTE DE TODOS OS REVISORES:")
            print(json.dumps(resultados, ensure_ascii=False, indent=2))
            
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo '{arquivo}' não encontrado")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    else:
        print(f"❌ Comando inválido: {comando}")
        print("Use 'revisar', 'template', 'listas', 'stats' ou 'testar'")


if __name__ == "__main__":
    processar_linha_comando()