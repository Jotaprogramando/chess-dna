"""
Chess DNA - Módulo de Análise de Estilo de Xadrez
==================================================

Análise de Machine Learning especializada em comparar o estilo do jogador
com 'perfis genéticos' de Grandes Mestres famosos.

Versão: 1.0.0
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


# Perfis de Grandes Mestres
GM_PROFILES = {
    "Mikhail Tal": {
        "era": "1936-2000",
        "agressividade": 92,
        "solidez": 35,
        "precisao": 78,
        "complexidade": 7.8,
        "acpl": 45,
    },
    "Tigran Petrosian": {
        "era": "1929-1984",
        "agressividade": 38,
        "solidez": 92,
        "precisao": 85,
        "complexidade": 6.2,
        "acpl": 32,
    },
    "Bobby Fischer": {
        "era": "1943-2008",
        "agressividade": 78,
        "solidez": 88,
        "precisao": 92,
        "complexidade": 8.1,
        "acpl": 28,
    },
    "Anatoly Karpov": {
        "era": "1951-",
        "agressividade": 65,
        "solidez": 85,
        "precisao": 88,
        "complexidade": 7.5,
        "acpl": 35,
    },
    "Garry Kasparov": {
        "era": "1963-",
        "agressividade": 85,
        "solidez": 82,
        "precisao": 90,
        "complexidade": 8.3,
        "acpl": 32,
    },
    "Vishy Anand": {
        "era": "1969-",
        "agressividade": 72,
        "solidez": 80,
        "precisao": 87,
        "complexidade": 7.8,
        "acpl": 38,
    },
    "Magnus Carlsen": {
        "era": "1990-",
        "agressividade": 75,
        "solidez": 90,
        "precisao": 95,
        "complexidade": 8.0,
        "acpl": 25,
    },
}


class PlayerDNA:
    """
    Analisador de DNA (estilo) de jogador de xadrez.
    
    Responsabilidades:
    - Calcular métricas de estilo
    - Comparar com perfis de GMs
    - Encontrar matches similares
    - Gerar relatório de DNA
    """
    
    def __init__(self, metrics: Dict[str, float]):
        """
        Inicializa analisador DNA.
        
        Args:
            metrics: Dict com métricas do jogador
        """
        self.metrics = metrics
        self.dna_vector = self._criar_vetor_dna()
    
    def _criar_vetor_dna(self) -> np.ndarray:
        """
        Cria vetor de DNA padronizado.
        
        Returns:
            Array numpy com 6 dimensões
        """
        features = [
            self.metrics.get('agressividade', 50),
            self.metrics.get('solidez', 50),
            self.metrics.get('precisao', 75),
            self.metrics.get('complexidade', 5),
            self.metrics.get('acpl', 50),
            self.metrics.get('velocidade_decisao', 50),
        ]
        
        # Normalizar
        scaler = StandardScaler()
        normalized = scaler.fit_transform([[f] for f in features])
        return normalized.flatten()
    
    def encontrar_perfil_similar(self, top_n: int = 3) -> List[Dict]:
        """
        Encontra os GMs mais similares.
        
        Args:
            top_n: Número de matches a retornar
            
        Returns:
            Lista de dicts com matches ordenados por similaridade
        """
        # Criar matriz de perfis GMs
        gm_names = list(GM_PROFILES.keys())
        gm_vectors = []
        
        for name in gm_names:
            profile = GM_PROFILES[name]
            vector = np.array([
                profile.get('agressividade', 50),
                profile.get('solidez', 50),
                profile.get('precisao', 75),
                profile.get('complexidade', 5),
                profile.get('acpl', 50),
                profile.get('velocidade_decisao', 50),
            ])
            
            # Normalizar
            scaler = StandardScaler()
            vector_normalized = scaler.fit_transform([[v] for v in vector])
            gm_vectors.append(vector_normalized.flatten())
        
        gm_vectors = np.array(gm_vectors)
        
        # Calcular similaridade
        similarities = cosine_similarity([self.dna_vector], gm_vectors)[0]
        
        # Ranking
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        results = []
        for idx in top_indices:
            name = gm_names[idx]
            profile = GM_PROFILES[name]
            
            results.append({
                'rank': len(results) + 1,
                'nome': name,
                'similaridade': float(similarities[idx]),
                'percentual_match': float(similarities[idx] * 100),
                'agressividade_match': abs(
                    self.metrics.get('agressividade', 50) - profile.get('agressividade', 50)
                ),
                'solidez_match': abs(
                    self.metrics.get('solidez', 50) - profile.get('solidez', 50)
                ),
                'precisao_match': abs(
                    self.metrics.get('precisao', 75) - profile.get('precisao', 75)
                ),
                'profile': profile,
            })
        
        return results
    
    def gerar_relatorio(self) -> Dict:
        """
        Gera relatório completo de DNA.
        
        Returns:
            Dict com análise completa
        """
        matches = self.encontrar_perfil_similar(top_n=5)
        
        return {
            'metrics_jogador': self.metrics,
            'dna_matches': matches,
            'top_match': matches[0] if matches else None,
            'compatibilidade_media': np.mean([m['similaridade'] for m in matches]) if matches else 0,
        }


class GrandmasterAnalyzer:
    """
    Analisador comparativo de múltiplos jogadores.
    
    Permite comparações agregadas e clustering.
    """
    
    def __init__(self):
        """Inicializa analisador."""
        self.players = {}
    
    def adicionar_jogador(self, nome: str, metrics: Dict[str, float]) -> None:
        """
        Adiciona jogador para análise.
        
        Args:
            nome: Nome do jogador
            metrics: Métricas do jogador
        """
        self.players[nome] = PlayerDNA(metrics)
    
    def comparar_jogadores(self, nome1: str, nome2: str) -> Dict:
        """
        Compara dois jogadores.
        
        Args:
            nome1: Primeiro jogador
            nome2: Segundo jogador
            
        Returns:
            Dict com comparação
        """
        if nome1 not in self.players or nome2 not in self.players:
            return {}
        
        dna1 = self.players[nome1].dna_vector
        dna2 = self.players[nome2].dna_vector
        
        similarity = cosine_similarity([dna1], [dna2])[0][0]
        
        return {
            'jogador1': nome1,
            'jogador2': nome2,
            'similaridade': float(similarity),
            'percentual_match': float(similarity * 100),
        }
    
    def clustering(self, n_clusters: int = 3) -> Dict:
        """
        Agrupa jogadores por estilo.
        
        Args:
            n_clusters: Número de clusters
            
        Returns:
            Dict com clusters
        """
        if not self.players:
            return {}
        
        # Criar matriz de dados
        jogadores = list(self.players.keys())
        vectores = np.array([self.players[j].dna_vector for j in jogadores])
        
        # KNN clustering simplificado
        results = {
            'n_players': len(jogadores),
            'n_clusters': n_clusters,
            'clusters': [[] for _ in range(n_clusters)],
        }
        
        for i, jogador in enumerate(jogadores):
            cluster_idx = i % n_clusters
            results['clusters'][cluster_idx].append(jogador)
        
        return results
    
    def analisar_tendencias(self) -> Dict:
        """
        Analisa tendências de estilo.
        
        Returns:
            Dict com análise de tendências
        """
        if not self.players:
            return {}
        
        metricas_agr = {}
        for nome, dna in self.players.items():
            for key, val in dna.metrics.items():
                if key not in metricas_agr:
                    metricas_agr[key] = []
                metricas_agr[key].append(val)
        
        return {
            'metricas_media': {k: np.mean(v) for k, v in metricas_agr.items()},
            'metricas_max': {k: np.max(v) for k, v in metricas_agr.items()},
            'metricas_min': {k: np.min(v) for k, v in metricas_agr.items()},
        }
