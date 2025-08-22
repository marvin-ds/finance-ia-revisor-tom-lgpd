#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revisor de Tom & LGPD do Finance-IA

Sistema responsável por revisar ideias de conteúdo garantindo:
- Tom de voz adequado (6 pilares: didático, empático, prático, confiável, moderno, inspirador)
- Consistência entre canal, formato e KPI
- Conformidade com LGPD
- Clareza de dores e desejos do público-alvo
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple
from listas_validas import ListasValidas


class RevisorTomLGPD:
    """Classe principal para revisão de ideias de conteúdo do Finance-IA"""
    
    def __init__(self):
        """Inicializa o revisor com as listas válidas de valores"""
        self.listas_validas = self._carregar_listas_validas()
        self.pilares_tom = [
            "didático", "empático", "prático", 
            "confiável", "moderno", "inspirador"
        ]
    
    def _carregar_listas_validas(self) -> Dict[str, List[str]]:
        """Carrega as listas de valores válidos para cada campo"""
        return ListasValidas.obter_todas()
    
    def revisar_ideia(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Função principal que revisa uma ideia completa
        
        Args:
            ideia: Dicionário com os campos da ideia original
            
        Returns:
            Dicionário com 'ideia_corrigida' e 'ajustes'
        """
        ideia_corrigida = ideia.copy()
        ajustes = []
        
        # 1. Validar e corrigir valores das listas
        ajustes.extend(self._validar_listas_validas(ideia_corrigida))
        
        # 2. Revisar tom de voz
        ajustes.extend(self._revisar_tom_voz(ideia_corrigida))
        
        # 3. Validar consistência canal/formato/KPI
        ajustes.extend(self._validar_consistencia(ideia_corrigida))
        
        # 4. Verificar conformidade LGPD
        ajustes.extend(self._verificar_lgpd(ideia_corrigida))
        
        # 5. Garantir campos imutáveis
        self._garantir_campos_imutaveis(ideia_corrigida)
        
        # 6. Atualizar observações com dor/desejo
        ajustes.extend(self._atualizar_observacoes(ideia_corrigida))
        
        return {
            "ideia_corrigida": ideia_corrigida,
            "ajustes": ajustes[:6]  # Máximo 6 itens
        }
    
    def _validar_listas_validas(self, ideia: Dict[str, Any]) -> List[str]:
        """Valida se os valores estão nas listas válidas"""
        ajustes = []
        
        campos_validar = {
            "persona": "personas",
            "pilar": "pilares", 
            "formato": "formatos",
            "canal": "canais",
            "cta": "ctas",
            "kpi_principal": "kpis",
            "prioridade": "prioridade"
        }
        
        for campo, lista_key in campos_validar.items():
            valor_atual = ideia.get(campo, "")
            lista_valida = self.listas_validas[lista_key]
            
            if valor_atual not in lista_valida:
                # Encontrar o mais similar ou usar o primeiro da lista
                novo_valor = self._encontrar_valor_similar(valor_atual, lista_valida)
                ideia[campo] = novo_valor
                ajustes.append(f"Ajustei {campo} para '{novo_valor}' (valor válido da lista).")
        
        return ajustes
    
    def _encontrar_valor_similar(self, valor: str, lista_valida: List[str]) -> str:
        """Encontra o valor mais similar na lista válida"""
        if not valor:
            return lista_valida[0]
        
        valor_lower = valor.lower()
        
        # Busca por correspondência parcial
        for item in lista_valida:
            if valor_lower in item.lower() or item.lower() in valor_lower:
                return item
        
        # Se não encontrar, retorna o primeiro da lista
        return lista_valida[0]
    
    def _revisar_tom_voz(self, ideia: Dict[str, Any]) -> List[str]:
        """Revisa o tom de voz do tema seguindo os 6 pilares"""
        ajustes = []
        tema_original = ideia.get("tema", "")
        
        if not tema_original:
            return ajustes
        
        tema_revisado = self._aplicar_pilares_tom(tema_original)
        
        if tema_revisado != tema_original:
            ideia["tema"] = tema_revisado
            ajustes.append("Ajustei o tema para evidenciar a dor/desejo e seguir o tom de voz.")
        
        return ajustes
    
    def _aplicar_pilares_tom(self, tema: str) -> str:
        """Aplica os 6 pilares do tom de voz ao tema"""
        # Remover jargões técnicos e simplificar
        tema = self._simplificar_linguagem(tema)
        
        # Garantir que a dor/desejo esteja explícita
        tema = self._explicitar_dor_desejo(tema)
        
        # Tornar mais prático (focar em ações)
        tema = self._tornar_pratico(tema)
        
        # Remover promessas irreais
        tema = self._remover_promessas_irreais(tema)
        
        # Limitar tamanho (80-90 caracteres)
        if len(tema) > 90:
            tema = tema[:87] + "..."
        
        return tema
    
    def _simplificar_linguagem(self, texto: str) -> str:
        """Simplifica a linguagem removendo jargões"""
        # Usar jargões das listas válidas
        jargoes = ListasValidas.get_jargoes_financeiros()
        
        texto_processado = texto.lower()
        for jargao, simples in jargoes.items():
            # Busca por palavra completa para evitar substituições incorretas
            import re
            padrao = r'\b' + re.escape(jargao) + r'\b'
            texto_processado = re.sub(padrao, simples, texto_processado, flags=re.IGNORECASE)
        
        return texto_processado.capitalize()
    
    def _explicitar_dor_desejo(self, tema: str) -> str:
        """Garante que a dor ou desejo esteja explícito no tema"""
        # Padrões que indicam dor/desejo já explícitos
        padroes_ok = [
            r"parar", r"evitar", r"sem", r"acabar com",  # dores
            r"conseguir", r"alcançar", r"realizar", r"conquistar"  # desejos
        ]
        
        tema_lower = tema.lower()
        tem_dor_desejo = any(re.search(padrao, tema_lower) for padrao in padroes_ok)
        
        if not tem_dor_desejo:
            # Adicionar contexto de dor/desejo no início
            if "dinheiro" in tema_lower or "financ" in tema_lower:
                tema = f"Parar de se preocupar: {tema.lower()}"
            elif "invest" in tema_lower:
                tema = f"Começar a investir: {tema.lower()}"
            else:
                tema = f"Resolver de vez: {tema.lower()}"
        
        return tema
    
    def _tornar_pratico(self, tema: str) -> str:
        """Torna o tema mais prático com foco em ações"""
        # Adicionar indicação de praticidade se não houver
        padroes_praticos = [r"\d+\s*passos?", r"como", r"guia", r"roteiro", r"método"]
        
        tema_lower = tema.lower()
        tem_praticidade = any(re.search(padrao, tema_lower) for padrao in padroes_praticos)
        
        if not tem_praticidade and len(tema) < 70:
            tema += ": 3 passos simples"
        
        return tema
    
    def _remover_promessas_irreais(self, tema: str) -> str:
        """Remove promessas irreais do tema"""
        promessas_irreais = ListasValidas.get_promessas_irreais()
        
        tema_processado = tema
        for promessa in promessas_irreais:
            # Remove a promessa irreal
            padrao = r'\b' + re.escape(promessa) + r'\b'
            tema_processado = re.sub(padrao, "", tema_processado, flags=re.IGNORECASE)
        
        # Limpar espaços duplos e pontuação órfã
        tema_processado = re.sub(r"\s+", " ", tema_processado)
        tema_processado = re.sub(r"\s*[,;:]\s*", ": ", tema_processado)
        tema_processado = tema_processado.strip()
        
        return tema_processado
    
    def _validar_consistencia(self, ideia: Dict[str, Any]) -> List[str]:
        """Valida consistência entre canal, formato e KPI"""
        ajustes = []
        
        formato = ideia.get("formato", "")
        canal = ideia.get("canal", "")
        kpi = ideia.get("kpi_principal", "")
        
        # Correções de canal baseadas no formato
        canal_corrigido = self._corrigir_canal_formato(formato, canal)
        if canal_corrigido != canal:
            ideia["canal"] = canal_corrigido
            ajustes.append(f"Ajustei o canal para {canal_corrigido} (compatível com {formato}).")
        
        # Correções de KPI baseadas no canal/formato
        kpi_corrigido = self._corrigir_kpi_canal(canal_corrigido, formato, kpi)
        if kpi_corrigido != kpi:
            ideia["kpi_principal"] = kpi_corrigido
            ajustes.append(f"Troquei KPI para {kpi_corrigido} (adequado ao canal/formato).")
        
        return ajustes
    
    def _corrigir_canal_formato(self, formato: str, canal: str) -> str:
        """Corrige o canal baseado no formato usando mapeamento das listas válidas"""
        mapeamento_canal_formato = ListasValidas.get_mapeamento_canal_formato()
        
        # Encontrar canais compatíveis com o formato
        canais_compativeis = []
        for canal_valido, formatos_validos in mapeamento_canal_formato.items():
            if formato in formatos_validos:
                canais_compativeis.append(canal_valido)
        
        # Se o canal atual é compatível, mantém
        if canal in canais_compativeis:
            return canal
        
        # Senão, retorna o primeiro canal compatível
        return canais_compativeis[0] if canais_compativeis else canal
    
    def _corrigir_kpi_canal(self, canal: str, formato: str, kpi_atual: str) -> str:
        """Corrige o KPI baseado no canal e formato usando mapeamento das listas válidas"""
        mapeamento_canal_kpi = ListasValidas.get_mapeamento_canal_kpi()
        
        # Obter KPIs preferidos para o canal
        kpis_preferidos = mapeamento_canal_kpi.get(canal, ["Engajamento"])
        
        # Ajuste especial para YouTube baseado no formato
        if canal == "YouTube" and formato == "YouTube Longo":
            kpis_preferidos = ["Retenção (50%)", "Cliques LP", "Tempo de Visualização"]
        elif canal == "YouTube" and formato == "Short":
            kpis_preferidos = ["Salvamentos", "CTR WhatsApp/Comunidade", "Compartilhamentos"]
        
        # Se o KPI atual não está na lista de preferidos, usar o primeiro preferido
        if kpi_atual not in kpis_preferidos:
            return kpis_preferidos[0]
        
        return kpi_atual
    
    def _verificar_lgpd(self, ideia: Dict[str, Any]) -> List[str]:
        """Verifica conformidade com LGPD"""
        ajustes = []
        
        # Verificar PII no tema e observações
        campos_verificar = ["tema", "observacoes"]
        
        for campo in campos_verificar:
            texto = ideia.get(campo, "")
            if self._contem_pii(texto):
                texto_limpo = self._remover_pii(texto)
                ideia[campo] = texto_limpo
                ajustes.append(f"Removi dados pessoais do campo {campo} (conformidade LGPD).")
        
        # Garantir que CTA não solicita dados
        cta = ideia.get("cta", "")
        if self._cta_solicita_dados(cta):
            ideia["cta"] = "Entrar na Comunidade Gratuita do Telegram"
            ajustes.append("Ajustei CTA para não solicitar dados pessoais.")
        
        return ajustes
    
    def _contem_pii(self, texto: str) -> bool:
        """Verifica se o texto contém informações pessoais"""
        if not texto:
            return False
        
        padroes_pii = [
            r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",  # CPF
            r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",  # CNPJ
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\(?\d{2}\)?\s?\d{4,5}-?\d{4}\b",  # Telefone
            r"\bR\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?\b",  # Valores específicos
        ]
        
        return any(re.search(padrao, texto) for padrao in padroes_pii)
    
    def _remover_pii(self, texto: str) -> str:
        """Remove informações pessoais do texto"""
        # Substituir por placeholders genéricos
        substituicoes = [
            (r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "[CPF]"),
            (r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", "[CNPJ]"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[email]"),
            (r"\b\(?\d{2}\)?\s?\d{4,5}-?\d{4}\b", "[telefone]"),
            (r"\bR\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?\b", "[valor]"),
        ]
        
        for padrao, substituto in substituicoes:
            texto = re.sub(padrao, substituto, texto)
        
        return texto
    
    def _cta_solicita_dados(self, cta: str) -> bool:
        """Verifica se o CTA solicita dados pessoais usando lista de palavras proibidas"""
        palavras_proibidas = ListasValidas.get_palavras_proibidas_lgpd()
        
        cta_lower = cta.lower()
        return any(palavra in cta_lower for palavra in palavras_proibidas)
    
    def _garantir_campos_imutaveis(self, ideia: Dict[str, Any]) -> None:
        """Garante que campos imutáveis permaneçam com valores corretos"""
        ideia["status"] = "Ideia"
        ideia["roteirizado_em"] = ""
        ideia["publicado_em"] = ""
        ideia["lgpd_ok"] = "Sim"
    
    def _atualizar_observacoes(self, ideia: Dict[str, Any]) -> List[str]:
        """Atualiza observações com dor/desejo identificados"""
        ajustes = []
        
        tema = ideia.get("tema", "")
        persona = ideia.get("persona", "")
        observacoes_atual = ideia.get("observacoes", "")
        
        # Identificar dor e desejo baseados no tema e persona
        dor, desejo = self._identificar_dor_desejo(tema, persona)
        
        if dor or desejo:
            nova_observacao = f"dor: {dor} | desejo: {desejo}"
            
            if nova_observacao != observacoes_atual:
                ideia["observacoes"] = nova_observacao
                ajustes.append("Atualizei observações com dor/desejo identificados.")
        
        return ajustes
    
    def _identificar_dor_desejo(self, tema: str, persona: str) -> Tuple[str, str]:
        """Identifica dor e desejo baseados no tema e persona"""
        tema_lower = tema.lower()
        persona_lower = persona.lower()
        
        # Usar mapeamentos das listas válidas
        dores_por_persona = ListasValidas.get_dores_por_persona()
        desejos_por_persona = ListasValidas.get_desejos_por_persona()
        
        # Identificar categoria da persona
        categoria = self._identificar_categoria_persona(persona_lower)
        
        # Selecionar dor e desejo mais relevantes ao tema
        dores_possiveis = dores_por_persona.get(categoria, dores_por_persona["iniciante"])
        desejos_possiveis = desejos_por_persona.get(categoria, desejos_por_persona["iniciante"])
        
        dor_selecionada = self._selecionar_mais_relevante(tema_lower, dores_possiveis)
        desejo_selecionado = self._selecionar_mais_relevante(tema_lower, desejos_possiveis)
        
        return dor_selecionada, desejo_selecionado
    
    def _identificar_categoria_persona(self, persona_lower: str) -> str:
        """Identifica a categoria da persona baseada no texto"""
        mapeamento_categorias = {
            "casal": ["casal", "jovem"],
            "mei": ["mei", "autônomo", "empreend"],
            "iniciante": ["iniciante", "física"],
            "família": ["família", "filhos"],
            "profissional": ["profissional", "liberal"],
            "aposentado": ["aposentad", "pré-aposentad"],
            "jovem": ["jovem", "adulto"],
            "mulher": ["mulher", "empreendedora"]
        }
        
        for categoria, palavras_chave in mapeamento_categorias.items():
            if any(palavra in persona_lower for palavra in palavras_chave):
                return categoria
        
        return "iniciante"  # padrão
    
    def _selecionar_mais_relevante(self, tema: str, opcoes: List[str]) -> str:
        """Seleciona a opção mais relevante baseada no tema"""
        for opcao in opcoes:
            palavras_opcao = opcao.split()
            if any(palavra in tema for palavra in palavras_opcao):
                return opcao
        
        # Se não encontrar correspondência, retorna a primeira
        return opcoes[0] if opcoes else ""


def main():
    """Função principal para teste do revisor"""
    revisor = RevisorTomLGPD()
    
    # Exemplo de ideia para teste
    ideia_exemplo = {
        "data_da_semana": "2024-01-15",
        "tema": "Como fazer alocação de ativos para diversificar portfolio",
        "persona": "Pessoa física iniciante",
        "pilar": "Investimentos",
        "formato": "Carrossel",
        "canal": "YouTube",  # Inconsistente com formato
        "cta": "Cadastre seu email para receber dicas",  # Solicita dados
        "kpi_principal": "Retenção (50%)",  # Inadequado para carrossel
        "status": "Ideia",
        "roteirizado_em": "",
        "publicado_em": "",
        "lgpd_ok": "Sim",
        "prioridade": "Alta",
        "links_assets": "",
        "observacoes": ""
    }
    
    resultado = revisor.revisar_ideia(ideia_exemplo)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()