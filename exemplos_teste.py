#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplos e Testes para o Revisor de Tom & LGPD do Finance-IA

Este arquivo contém exemplos de ideias para testar o revisor,
incluindo casos que precisam de correção e casos já corretos.
"""

import json
from interface_revisor import InterfaceRevisor
from datetime import datetime


def obter_exemplos_teste():
    """Retorna uma lista de exemplos para teste do revisor"""
    
    exemplos = [
        {
            "nome": "Exemplo 1 - Jargões e Canal Inconsistente",
            "descricao": "Ideia com jargões financeiros e canal incompatível com formato",
            "ideia": {
                "data_da_semana": "2024-01-15",
                "tema": "Como fazer alocação de ativos para diversificar portfolio e maximizar rentabilidade",
                "persona": "Pessoa física iniciante",
                "pilar": "Investimentos",
                "formato": "Carrossel",
                "canal": "YouTube",  # Inconsistente
                "cta": "Cadastre seu email para receber dicas exclusivas",  # Solicita dados
                "kpi_principal": "Retenção (50%)",  # Inadequado para carrossel
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Alta",
                "links_assets": "",
                "observacoes": ""
            }
        },
        
        {
            "nome": "Exemplo 2 - Promessas Irreais",
            "descricao": "Ideia com promessas irreais e tema muito longo",
            "ideia": {
                "data_da_semana": "2024-01-16",
                "tema": "Garanto que você vai ficar rico em 30 dias com este método milagroso de investimentos que nunca falha e é 100% garantido sem risco nenhum",
                "persona": "MEI/Autônomo",
                "pilar": "Renda Extra",
                "formato": "Reel",
                "canal": "Instagram",
                "cta": "Entrar na Comunidade Gratuita do Telegram",
                "kpi_principal": "Salvamentos",
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Média",
                "links_assets": "",
                "observacoes": ""
            }
        },
        
        {
            "nome": "Exemplo 3 - Dados Pessoais no Tema",
            "descricao": "Ideia com possíveis dados pessoais no tema",
            "ideia": {
                "data_da_semana": "2024-01-17",
                "tema": "Como João Silva, CPF 123.456.789-00, conseguiu R$ 50.000 em 6 meses",
                "persona": "Casal jovem (25-35 anos)",
                "pilar": "Planejamento",
                "formato": "YouTube Longo",
                "canal": "YouTube",
                "cta": "Digite seu nome e telefone para receber o método",
                "kpi_principal": "Cliques LP",
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Alta",
                "links_assets": "",
                "observacoes": ""
            }
        },
        
        {
            "nome": "Exemplo 4 - Tema Genérico sem Dor/Desejo",
            "descricao": "Tema genérico que não evidencia dor ou desejo específico",
            "ideia": {
                "data_da_semana": "2024-01-18",
                "tema": "Dicas de educação financeira",
                "persona": "Família com filhos",
                "pilar": "Educação Financeira",
                "formato": "Post Telegram",
                "canal": "Telegram",
                "cta": "Entrar na Comunidade Gratuita do Telegram",
                "kpi_principal": "Engajamento",
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Baixa",
                "links_assets": "",
                "observacoes": ""
            }
        },
        
        {
            "nome": "Exemplo 5 - Valores Fora das Listas",
            "descricao": "Ideia com valores que não estão nas listas válidas",
            "ideia": {
                "data_da_semana": "2024-01-19",
                "tema": "Como sair das dívidas do cartão: método passo a passo",
                "persona": "Estudante universitário",  # Não está na lista
                "pilar": "Controle de Dívidas",  # Não está na lista
                "formato": "Video Curto",  # Não está na lista
                "canal": "Instagram",
                "cta": "Baixar E-book Gratuito",  # Não está na lista
                "kpi_principal": "Downloads",  # Não está na lista
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Altíssima",  # Não está na lista
                "links_assets": "",
                "observacoes": ""
            }
        },
        
        {
            "nome": "Exemplo 6 - Ideia Já Correta",
            "descricao": "Ideia que já está bem formatada e não precisa de muitas correções",
            "ideia": {
                "data_da_semana": "2024-01-20",
                "tema": "Parar as brigas por dinheiro: 3 passos para dividir as contas em casal",
                "persona": "Casal jovem (25-35 anos)",
                "pilar": "Planejamento",
                "formato": "Carrossel",
                "canal": "Instagram",
                "cta": "Entrar na Comunidade Gratuita do Telegram",
                "kpi_principal": "Salvamentos",
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Alta",
                "links_assets": "",
                "observacoes": ""
            }
        },
        
        {
            "nome": "Exemplo 7 - MEI com Problemas Específicos",
            "descricao": "Ideia focada em MEI com jargões e formato inadequado",
            "ideia": {
                "data_da_semana": "2024-01-21",
                "tema": "Otimização tributária para maximizar o fluxo de caixa do MEI",
                "persona": "MEI/Autônomo",
                "pilar": "Impostos e Tributação",
                "formato": "Stories",
                "canal": "YouTube",  # Inconsistente
                "cta": "WhatsApp: Diagnóstico 5'",
                "kpi_principal": "Tempo de Visualização",  # Inadequado para Stories
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "Média",
                "links_assets": "",
                "observacoes": ""
            }
        }
    ]
    
    return exemplos


def executar_testes():
    """Executa todos os testes com os exemplos"""
    print("=== TESTES DO REVISOR DE TOM & LGPD ===")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    interface = InterfaceRevisor()
    exemplos = obter_exemplos_teste()
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n🧪 TESTE {i}: {exemplo['nome']}")
        print(f"📝 Descrição: {exemplo['descricao']}")
        print("-" * 40)
        
        # Mostrar ideia original
        print("\n📥 IDEIA ORIGINAL:")
        print(f"Tema: {exemplo['ideia']['tema']}")
        print(f"Persona: {exemplo['ideia']['persona']}")
        print(f"Canal/Formato: {exemplo['ideia']['canal']} / {exemplo['ideia']['formato']}")
        print(f"CTA: {exemplo['ideia']['cta']}")
        print(f"KPI: {exemplo['ideia']['kpi_principal']}")
        
        # Executar revisão
        resultado = interface.revisar_ideia_dict(exemplo['ideia'])
        
        if "erro" in resultado:
            print(f"\n❌ ERRO: {resultado['erro']}")
            continue
        
        # Mostrar resultado
        ideia_corrigida = resultado['ideia_corrigida']
        ajustes = resultado['ajustes']
        
        print("\n📤 IDEIA CORRIGIDA:")
        print(f"Tema: {ideia_corrigida['tema']}")
        print(f"Persona: {ideia_corrigida['persona']}")
        print(f"Canal/Formato: {ideia_corrigida['canal']} / {ideia_corrigida['formato']}")
        print(f"CTA: {ideia_corrigida['cta']}")
        print(f"KPI: {ideia_corrigida['kpi_principal']}")
        print(f"Observações: {ideia_corrigida['observacoes']}")
        
        print("\n🔧 AJUSTES REALIZADOS:")
        if ajustes:
            for j, ajuste in enumerate(ajustes, 1):
                print(f"  {j}. {ajuste}")
        else:
            print("  ✅ Nenhum ajuste necessário")
        
        print("\n" + "=" * 50)
    
    print("\n🎉 TESTES CONCLUÍDOS!")


def testar_validacao():
    """Testa a função de validação sem modificar as ideias"""
    print("\n=== TESTE DE VALIDAÇÃO (SEM MODIFICAÇÃO) ===")
    
    interface = InterfaceRevisor()
    exemplos = obter_exemplos_teste()
    
    for i, exemplo in enumerate(exemplos[:3], 1):  # Apenas os 3 primeiros
        print(f"\n🔍 VALIDAÇÃO {i}: {exemplo['nome']}")
        
        validacao = interface.validar_ideia_completa(exemplo['ideia'])
        
        print(f"✅ Válida: {validacao['valida']}")
        
        if validacao['erros']:
            print("❌ Erros:")
            for erro in validacao['erros']:
                print(f"  - {erro}")
        
        if validacao['avisos']:
            print("⚠️ Avisos:")
            for aviso in validacao['avisos']:
                print(f"  - {aviso}")
        
        if validacao['sugestoes']:
            print("💡 Sugestões:")
            for sugestao in validacao['sugestoes']:
                print(f"  - {sugestao}")


def salvar_exemplos_json():
    """Salva os exemplos em arquivos JSON para teste manual"""
    exemplos = obter_exemplos_teste()
    
    for i, exemplo in enumerate(exemplos, 1):
        nome_arquivo = f"exemplo_{i:02d}_{exemplo['nome'].lower().replace(' ', '_').replace('-', '_')}.json"
        nome_arquivo = nome_arquivo.replace('__', '_')
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(exemplo['ideia'], f, ensure_ascii=False, indent=2)
        
        print(f"💾 Salvo: {nome_arquivo}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--validacao":
            testar_validacao()
        elif sys.argv[1] == "--salvar":
            salvar_exemplos_json()
        elif sys.argv[1] == "--help":
            print("Uso:")
            print("  python exemplos_teste.py           # Executa todos os testes")
            print("  python exemplos_teste.py --validacao  # Testa apenas validação")
            print("  python exemplos_teste.py --salvar     # Salva exemplos em JSON")
        else:
            print("Argumento inválido. Use --help para ver as opções.")
    else:
        executar_testes()