#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listas Válidas para o Revisor de Tom & LGPD do Finance-IA

Contém todas as listas de valores válidos para cada campo das ideias de conteúdo.
Essas listas são usadas para validação e correção automática dos campos.
"""

from typing import Dict, List


class ListasValidas:
    """Classe que centraliza todas as listas de valores válidos"""
    
    @staticmethod
    def obter_todas() -> Dict[str, List[str]]:
        """Retorna todas as listas válidas organizadas por categoria"""
        return {
            "personas": ListasValidas.get_personas(),
            "pilares": ListasValidas.get_pilares(),
            "formatos": ListasValidas.get_formatos(),
            "canais": ListasValidas.get_canais(),
            "ctas": ListasValidas.get_ctas(),
            "kpis": ListasValidas.get_kpis(),
            "prioridade": ListasValidas.get_prioridades()
        }
    
    @staticmethod
    def get_personas() -> List[str]:
        """Lista de personas válidas do Finance-IA"""
        return [
            "Casal jovem (25-35 anos)",
            "MEI/Autônomo",
            "Pessoa física iniciante",
            "Família com filhos",
            "Profissional liberal",
            "Aposentado/Pré-aposentadoria",
            "Jovem adulto (18-25 anos)",
            "Mulher empreendedora"
        ]
    
    @staticmethod
    def get_pilares() -> List[str]:
        """Lista de pilares de conteúdo do Finance-IA"""
        return [
            "Educação Financeira",
            "Investimentos",
            "Planejamento",
            "Controle de Gastos",
            "Renda Extra",
            "Mindset Financeiro",
            "Proteção Patrimonial",
            "Impostos e Tributação"
        ]
    
    @staticmethod
    def get_formatos() -> List[str]:
        """Lista de formatos de conteúdo válidos"""
        return [
            "Reel",
            "Short",
            "Carrossel",
            "YouTube Longo",
            "Post Telegram",
            "Stories",
            "Status",
            "Live",
            "Podcast",
            "Thread Twitter"
        ]
    
    @staticmethod
    def get_canais() -> List[str]:
        """Lista de canais de distribuição válidos"""
        return [
            "Instagram",
            "TikTok",
            "YouTube",
            "Telegram",
            "WhatsApp",
            "LinkedIn",
            "Twitter",
            "Facebook"
        ]
    
    @staticmethod
    def get_ctas() -> List[str]:
        """Lista de CTAs válidos priorizando conformidade LGPD"""
        return [
            "Entrar na Comunidade Gratuita do Telegram",
            "WhatsApp: Diagnóstico 5'",
            "Baixar Planilha Gratuita",
            "Acessar Conteúdo Completo",
            "Participar da Live Gratuita",
            "Seguir para Mais Dicas",
            "Salvar para Não Perder",
            "Compartilhar com Quem Precisa"
        ]
    
    @staticmethod
    def get_kpis() -> List[str]:
        """Lista de KPIs válidos para mensuração"""
        return [
            "Salvamentos",
            "CTR WhatsApp/Comunidade",
            "Retenção (50%)",
            "Cliques LP",
            "Engajamento",
            "Comentários",
            "Compartilhamentos",
            "Visualizações",
            "Tempo de Visualização",
            "Taxa de Conversão"
        ]
    
    @staticmethod
    def get_prioridades() -> List[str]:
        """Lista de níveis de prioridade válidos"""
        return [
            "Alta",
            "Média",
            "Baixa"
        ]
    
    @staticmethod
    def get_mapeamento_canal_formato() -> Dict[str, List[str]]:
        """Mapeamento de compatibilidade entre canais e formatos"""
        return {
            "Instagram": ["Reel", "Carrossel", "Stories", "Live"],
            "TikTok": ["Short", "Live"],
            "YouTube": ["Short", "YouTube Longo", "Live"],
            "Telegram": ["Post Telegram"],
            "WhatsApp": ["Status"],
            "LinkedIn": ["Carrossel", "Post Telegram"],
            "Twitter": ["Thread Twitter"],
            "Facebook": ["Reel", "Carrossel", "Live"]
        }
    
    @staticmethod
    def get_mapeamento_canal_kpi() -> Dict[str, List[str]]:
        """Mapeamento de KPIs mais adequados por canal"""
        return {
            "Instagram": ["Salvamentos", "CTR WhatsApp/Comunidade", "Engajamento"],
            "TikTok": ["Salvamentos", "CTR WhatsApp/Comunidade", "Compartilhamentos"],
            "YouTube": ["Retenção (50%)", "Cliques LP", "Tempo de Visualização"],
            "Telegram": ["Engajamento", "CTR WhatsApp/Comunidade", "Cliques LP"],
            "WhatsApp": ["Engajamento", "CTR WhatsApp/Comunidade"],
            "LinkedIn": ["Engajamento", "Cliques LP", "Compartilhamentos"],
            "Twitter": ["Engajamento", "Compartilhamentos", "Comentários"],
            "Facebook": ["Engajamento", "Compartilhamentos", "Cliques LP"]
        }
    
    @staticmethod
    def get_palavras_proibidas_lgpd() -> List[str]:
        """Lista de palavras/frases que podem indicar solicitação de dados pessoais"""
        return [
            "cadastre", "cadastro", "informe", "digite", "envie", 
            "seu nome", "seu email", "seu telefone", "seus dados",
            "nome completo", "data de nascimento", "endereço",
            "renda mensal", "salário", "cpf", "rg", "documento",
            "conta bancária", "cartão de crédito", "senha"
        ]
    
    @staticmethod
    def get_jargoes_financeiros() -> Dict[str, str]:
        """Mapeamento de jargões financeiros para linguagem simples"""
        return {
            "alocação de ativos": "divisão do dinheiro",
            "diversificação": "espalhar investimentos",
            "liquidez": "facilidade para resgatar",
            "rentabilidade": "retorno",
            "volatilidade": "variação",
            "patrimônio líquido": "valor total",
            "fluxo de caixa": "entrada e saída de dinheiro",
            "alavancagem": "usar dinheiro emprestado",
            "hedge": "proteção",
            "benchmark": "referência",
            "spread": "diferença",
            "yield": "rendimento",
            "equity": "ações",
            "bonds": "títulos",
            "commodities": "matérias-primas",
            "derivativos": "contratos baseados em outros ativos",
            "portfolio": "carteira de investimentos",
            "asset": "ativo",
            "liability": "dívida",
            "roi": "retorno sobre investimento"
        }
    
    @staticmethod
    def get_promessas_irreais() -> List[str]:
        """Lista de palavras/frases que indicam promessas irreais"""
        return [
            "garanto", "garantia", "garantido", "certeza absoluta",
            "riqueza rápida", "rico em 30 dias", "milhionário", 
            "sem esforço", "automático", "milagre", "segredo",
            "fórmula mágica", "método infalível", "100% garantido",
            "nunca perde", "risco zero", "lucro certo",
            "enriquecer dormindo", "dinheiro fácil", "fortuna rápida"
        ]
    
    @staticmethod
    def get_dores_por_persona() -> Dict[str, List[str]]:
        """Mapeamento de dores principais por persona"""
        return {
            "casal": [
                "brigas por dinheiro", "falta de organização financeira", 
                "gastos descontrolados", "objetivos diferentes",
                "falta de transparência", "divisão injusta das contas"
            ],
            "mei": [
                "renda variável", "falta de reserva de emergência", 
                "impostos confusos", "misturar pessoa física e jurídica",
                "não saber precificar", "falta de planejamento"
            ],
            "iniciante": [
                "não saber por onde começar", "medo de investir", 
                "falta de conhecimento", "informações conflitantes",
                "medo de perder dinheiro", "linguagem técnica"
            ],
            "família": [
                "gastos altos com filhos", "falta de planejamento educacional", 
                "pressão por casa própria", "seguro de vida inadequado",
                "não conseguir poupar", "futuro incerto dos filhos"
            ],
            "profissional": [
                "alta carga tributária", "falta de diversificação de renda", 
                "aposentadoria insuficiente", "não otimizar impostos",
                "dependência de um cliente", "falta de proteção patrimonial"
            ],
            "aposentado": [
                "renda insuficiente", "inflação corroendo poder de compra", 
                "medo de investimentos", "dependência dos filhos",
                "gastos médicos altos", "patrimônio mal estruturado"
            ],
            "jovem": [
                "primeiro emprego", "não saber poupar", 
                "pressão por consumo", "falta de educação financeira",
                "dívidas no cartão", "não pensar no futuro"
            ],
            "mulher": [
                "gap salarial", "dupla jornada", 
                "menor tempo para investir", "insegurança financeira",
                "dependência financeira", "aposentadoria menor"
            ]
        }
    
    @staticmethod
    def get_desejos_por_persona() -> Dict[str, List[str]]:
        """Mapeamento de desejos principais por persona"""
        return {
            "casal": [
                "harmonia financeira", "planejar juntos", 
                "primeiro imóvel", "viagem dos sonhos",
                "filhos sem aperto", "aposentadoria tranquila"
            ],
            "mei": [
                "estabilidade financeira", "crescer o negócio", 
                "aposentadoria digna", "reserva robusta",
                "diversificar renda", "organização financeira"
            ],
            "iniciante": [
                "começar a investir", "ter reserva de emergência", 
                "independência financeira", "conhecimento sólido",
                "confiança para decidir", "futuro seguro"
            ],
            "família": [
                "segurança para os filhos", "casa própria", 
                "educação de qualidade", "viagens em família",
                "tranquilidade financeira", "deixar herança"
            ],
            "profissional": [
                "otimização tributária", "diversificação de renda", 
                "aposentadoria precoce", "proteção patrimonial",
                "liberdade financeira", "crescimento patrimonial"
            ],
            "aposentado": [
                "renda complementar", "preservar patrimônio", 
                "independência dos filhos", "qualidade de vida",
                "tranquilidade financeira", "deixar legado"
            ],
            "jovem": [
                "independência dos pais", "primeiro investimento", 
                "casa própria", "viagens",
                "liberdade financeira cedo", "construir patrimônio"
            ],
            "mulher": [
                "independência financeira", "igualdade salarial", 
                "aposentadoria digna", "empreender",
                "segurança financeira", "empoderamento econômico"
            ]
        }


# Função utilitária para facilitar importação
def obter_listas_validas() -> Dict[str, List[str]]:
    """Função de conveniência para obter todas as listas válidas"""
    return ListasValidas.obter_todas()


if __name__ == "__main__":
    # Teste das listas
    import json
    
    listas = ListasValidas.obter_todas()
    print("=== LISTAS VÁLIDAS DO FINANCE-IA ===")
    
    for categoria, valores in listas.items():
        print(f"\n{categoria.upper()}:")
        for valor in valores:
            print(f"  - {valor}")
    
    print(f"\n=== ESTATÍSTICAS ===")
    print(f"Total de categorias: {len(listas)}")
    print(f"Total de valores: {sum(len(v) for v in listas.values())}")