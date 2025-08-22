#!/usr/bin/env python3
"""
Exemplo de uso do Finance-IA Reviewer com IA

Este exemplo demonstra como usar o sistema Finance-IA com integração OpenAI,
mostrando diferentes tipos de revisores e funcionalidades avançadas.

Autor: Finance-IA Team
Versão: 2.0.0
Data: 2024
"""

import json
import os
from interface_revisor import InterfaceRevisor
from revisor_hibrido import TipoRevisor

# Configurar chave da API (em produção, use variáveis de ambiente)
API_KEY = "sk-proj-YOUR_OPENAI_API_KEY_HERE"

def exemplo_basico_com_ia():
    """
    Exemplo básico de uso com IA
    """
    print("🤖 EXEMPLO BÁSICO COM IA")
    print("=" * 50)
    
    # Inicializar interface com IA
    revisor = InterfaceRevisor(usar_ia=True, api_key=API_KEY)
    
    # Conteúdo de teste
    conteudo = """
    Prezado cliente,
    
    Sua conta foi SUSPENSA por atividade suspeita!
    Para reativar IMEDIATAMENTE, clique aqui: http://banco-falso.com/reativar
    
    Caso não faça isso em 24 horas, sua conta será CANCELADA permanentemente.
    
    Banco Seguro S.A.
    """
    
    print(f"📝 Conteúdo a ser revisado:")
    print(conteudo)
    print("\n" + "-" * 50)
    
    # Realizar revisão
    resultado = revisor.revisar(conteudo, TipoRevisor.HIBRIDO)
    
    print("\n📊 RESULTADO DA REVISÃO:")
    print(f"Score de Conformidade: {resultado.score_conformidade}")
    print(f"Classificação: {resultado.classificacao}")
    print(f"Usar IA: {resultado.usar_ia}")
    
    if resultado.problemas_encontrados:
        print("\n⚠️ Problemas encontrados:")
        for problema in resultado.problemas_encontrados:
            print(f"  • {problema}")
    
    if resultado.sugestoes_melhoria:
        print("\n💡 Sugestões de melhoria:")
        for sugestao in resultado.sugestoes_melhoria:
            print(f"  • {sugestao}")
    
    if resultado.detalhes_ia:
        print("\n🧠 Análise da IA:")
        print(f"  Modelo usado: {resultado.detalhes_ia.get('modelo', 'N/A')}")
        print(f"  Tokens usados: {resultado.detalhes_ia.get('tokens_usados', 'N/A')}")
        if 'analise_detalhada' in resultado.detalhes_ia:
            print(f"  Análise: {resultado.detalhes_ia['analise_detalhada']}")

def exemplo_comparacao_revisores():
    """
    Exemplo comparando diferentes tipos de revisores
    """
    print("\n🔍 COMPARAÇÃO DE REVISORES")
    print("=" * 50)
    
    # Conteúdo de teste
    conteudo = """
    PROMOÇÃO IMPERDÍVEL!
    
    Ganhe R$ 50.000 em apenas 1 semana!
    Investimento mínimo: R$ 100
    Retorno garantido de 500%!
    
    Vagas limitadas! Apenas hoje!
    WhatsApp: (11) 99999-9999
    """
    
    tipos_revisor = [
        (TipoRevisor.TOM, "Revisor de Tom"),
        (TipoRevisor.LGPD, "Revisor LGPD"),
        (TipoRevisor.HIBRIDO, "Revisor Híbrido")
    ]
    
    print(f"📝 Conteúdo: {conteudo[:100]}...")
    print("\n" + "-" * 50)
    
    for tipo, nome in tipos_revisor:
        print(f"\n🔎 {nome}:")
        
        # Sem IA
        revisor_sem_ia = InterfaceRevisor(usar_ia=False)
        resultado_sem_ia = revisor_sem_ia.revisar(conteudo, tipo)
        print(f"  Sem IA - Score: {resultado_sem_ia.score_conformidade} | Classificação: {resultado_sem_ia.classificacao}")
        
        # Com IA
        revisor_com_ia = InterfaceRevisor(usar_ia=True, api_key=API_KEY)
        resultado_com_ia = revisor_com_ia.revisar(conteudo, tipo)
        print(f"  Com IA - Score: {resultado_com_ia.score_conformidade} | Classificação: {resultado_com_ia.classificacao}")
        
        # Diferença
        diferenca = resultado_com_ia.score_conformidade - resultado_sem_ia.score_conformidade
        print(f"  📈 Diferença: {diferenca:+.1f} pontos")

def exemplo_batch_processing():
    """
    Exemplo de processamento em lote
    """
    print("\n📦 PROCESSAMENTO EM LOTE")
    print("=" * 50)
    
    # Lista de conteúdos para processar
    conteudos = [
        "Oferta especial! Desconto de 90% apenas hoje!",
        "Sua fatura vence em 3 dias. Valor: R$ 250,00",
        "URGENTE: Clique aqui para evitar bloqueio da conta!",
        "Obrigado pela preferência. Atendimento: 0800-123-4567",
        "Ganhe dinheiro fácil! Sem esforço, sem risco!"
    ]
    
    revisor = InterfaceRevisor(usar_ia=True, api_key=API_KEY)
    resultados = []
    
    print(f"📊 Processando {len(conteudos)} conteúdos...\n")
    
    for i, conteudo in enumerate(conteudos, 1):
        print(f"[{i}/{len(conteudos)}] Processando: {conteudo[:50]}...")
        
        resultado = revisor.revisar(conteudo, TipoRevisor.HIBRIDO)
        resultados.append({
            'conteudo': conteudo,
            'score': resultado.score_conformidade,
            'classificacao': resultado.classificacao,
            'problemas': len(resultado.problemas_encontrados)
        })
        
        print(f"         Score: {resultado.score_conformidade} | {resultado.classificacao}")
    
    # Estatísticas
    print("\n📈 ESTATÍSTICAS:")
    scores = [r['score'] for r in resultados]
    print(f"Score médio: {sum(scores) / len(scores):.1f}")
    print(f"Melhor score: {max(scores)}")
    print(f"Pior score: {min(scores)}")
    
    problemas_total = sum(r['problemas'] for r in resultados)
    print(f"Total de problemas: {problemas_total}")
    
    # Conteúdos problemáticos
    problematicos = [r for r in resultados if r['score'] < 70]
    if problematicos:
        print(f"\n⚠️ Conteúdos problemáticos ({len(problematicos)}):")
        for item in problematicos:
            print(f"  • Score {item['score']}: {item['conteudo'][:60]}...")

def exemplo_configuracoes_avancadas():
    """
    Exemplo com configurações avançadas
    """
    print("\n⚙️ CONFIGURAÇÕES AVANÇADAS")
    print("=" * 50)
    
    # Configurações personalizadas
    config_personalizada = {
        'modelo': 'gpt-4',
        'temperatura': 0.3,
        'max_tokens': 1000,
        'timeout': 30
    }
    
    revisor = InterfaceRevisor(
        usar_ia=True, 
        api_key=API_KEY,
        config_ia=config_personalizada
    )
    
    conteudo = """
    Caro investidor,
    
    Oportunidade única de investimento em criptomoedas!
    Retorno de 1000% garantido em 30 dias.
    
    Não perca esta chance! Vagas limitadas.
    Investimento mínimo: R$ 1.000
    
    Para mais informações, entre em contato:
    WhatsApp: (11) 99999-9999
    Email: investimentos@empresa-duvidosa.com
    """
    
    print("📝 Analisando conteúdo com configurações personalizadas...")
    resultado = revisor.revisar(conteudo, TipoRevisor.HIBRIDO)
    
    print(f"\n📊 Resultado:")
    print(f"Score: {resultado.score_conformidade}")
    print(f"Classificação: {resultado.classificacao}")
    
    if resultado.detalhes_ia:
        print(f"\n🤖 Detalhes da IA:")
        for chave, valor in resultado.detalhes_ia.items():
            if chave != 'analise_detalhada':  # Evitar texto muito longo
                print(f"  {chave}: {valor}")

def exemplo_tratamento_erros():
    """
    Exemplo de tratamento de erros
    """
    print("\n🚨 TRATAMENTO DE ERROS")
    print("=" * 50)
    
    # Teste com API key inválida
    print("1. Testando com API key inválida...")
    try:
        revisor_invalido = InterfaceRevisor(usar_ia=True, api_key="sk-invalid-key")
        resultado = revisor_invalido.revisar("Teste", TipoRevisor.HIBRIDO)
        print(f"   Resultado inesperado: {resultado.score_conformidade}")
    except Exception as e:
        print(f"   ✅ Erro capturado corretamente: {type(e).__name__}")
    
    # Teste sem API key
    print("\n2. Testando sem API key...")
    try:
        revisor_sem_key = InterfaceRevisor(usar_ia=True)  # Sem API key
        resultado = revisor_sem_key.revisar("Teste", TipoRevisor.HIBRIDO)
        print(f"   Score (modo fallback): {resultado.score_conformidade}")
        print(f"   ✅ Sistema funcionou em modo fallback")
    except Exception as e:
        print(f"   ⚠️ Erro: {e}")
    
    # Teste com conteúdo vazio
    print("\n3. Testando com conteúdo vazio...")
    try:
        revisor = InterfaceRevisor(usar_ia=True, api_key=API_KEY)
        resultado = revisor.revisar("", TipoRevisor.HIBRIDO)
        print(f"   ✅ Score para conteúdo vazio: {resultado.score_conformidade}")
    except Exception as e:
        print(f"   ⚠️ Erro: {e}")

if __name__ == "__main__":
    try:
        # Verificar se a API key foi configurada
        if API_KEY == "sk-proj-YOUR_OPENAI_API_KEY_HERE":
            print("⚠️ ATENÇÃO: Configure sua API key OpenAI antes de executar os exemplos com IA!")
            print("Editando a variável API_KEY no início do arquivo.\n")
        
        # Executar exemplos
        exemplo_basico_com_ia()
        exemplo_comparacao_revisores()
        exemplo_batch_processing()
        exemplo_configuracoes_avancadas()
        exemplo_tratamento_erros()
        
        print("\n🎉 Todos os exemplos foram executados com sucesso!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()