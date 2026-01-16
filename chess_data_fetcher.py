"""
Chess Data Fetcher - Módulo de Captura de Dados
===============================================

Conexão com API Chess.com para baixar histórico de partidas.
Implementa cache inteligente e tratamento de erros robusto.

Versão: 1.0.0
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum
import logging
import time

logger = logging.getLogger(__name__)


class TimeControl(Enum):
    """Categorias de controle de tempo."""
    BULLET = "bullet"
    BLITZ = "blitz"
    RAPID = "rapid"
    CLASSICAL = "classical"
    ALL = "all"


class Platform(Enum):
    """Plataformas de xadrez suportadas."""
    CHESS_COM = "chess.com"
    LICHESS = "lichess.org"


class ChessDataFetcher:
    """
    Buscador de dados de partidas de xadrez via API Chess.com.
    
    Características:
    - Busca histórico de partidas
    - Suporte a múltiplos controles de tempo
    - Cache de dados em JSON
    - Tratamento de erros robusto
    - Compatível com Streamlit Cloud
    """
    
    CHESS_COM_API = "https://api.chess.com/pub/player"
    CACHE_DIR = Path("cache/dados_xadrez")
    
    def __init__(self, platform: Platform = Platform.CHESS_COM, timeout: int = 15):
        """
        Inicializa o fetcher de dados.
        
        Args:
            platform: Plataforma (Chess.com ou Lichess)
            timeout: Timeout para requisições (segundos)
        """
        self.platform = platform
        self.timeout = timeout
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ChessDNA/1.0 (xadrez.ai)'
        })
    
    def buscar_chess_com(
        self,
        username: str,
        time_control: TimeControl = TimeControl.ALL,
        max_games: int = 100,
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Busca partidas de um jogador na Chess.com.
        
        Args:
            username: Nome do usuário
            time_control: Tipo de controle de tempo
            max_games: Número máximo de partidas
            use_cache: Usar cache se disponível
            
        Returns:
            DataFrame com dados das partidas
        """
        username = username.strip().lower()
        if not username:
            raise ValueError("Username não pode estar vazio")
        
        # Verificar cache
        cache_file = self.CACHE_DIR / f"{username}_{time_control.value}.json"
        if use_cache and cache_file.exists():
            try:
                logger.info(f"Usando cache para {username}")
                return self._carregar_cache(cache_file)
            except Exception as e:
                logger.warning(f"Erro ao ler cache: {e}")
        
        try:
            logger.info(f"Buscando dados para {username}...")
            
            # Verificar se usuário existe
            if not self._usuario_existe(username):
                raise ValueError(f"Usuário '{username}' não encontrado no Chess.com")
            
            # Buscar partidas
            games_data = self._buscar_games_mensais(username, time_control, max_games)
            
            if not games_data:
                logger.warning(f"Nenhuma partida encontrada para {username}")
                return pd.DataFrame()
            
            # Processar dados
            df = self._processar_games(games_data, username)
            
            # Salvar em cache
            if len(df) > 0:
                self._salvar_cache(df, cache_file)
            
            logger.info(f"✅ {len(df)} partidas carregadas com sucesso")
            return df
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados: {str(e)}")
            raise
    
    def _usuario_existe(self, username: str) -> bool:
        """Verifica se usuário existe no Chess.com."""
        try:
            url = f"{self.CHESS_COM_API}/{username}"
            response = self.session.get(url, timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao verificar usuário: {e}")
            return False
    
    def _buscar_games_mensais(
        self,
        username: str,
        time_control: TimeControl,
        max_games: int
    ) -> List[Dict]:
        """
        Busca partidas agrupadas por mês (últimos 3 meses).
        
        Args:
            username: Nome do usuário
            time_control: Tipo de controle
            max_games: Máximo de partidas
            
        Returns:
            Lista de dicionários de games
        """
        all_games = []
        url = f"{self.CHESS_COM_API}/{username}/games/archives"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            archives = response.json().get("archives", [])
            
            # Buscar games em ordem reversa (mais recentes primeiro)
            for archive_url in reversed(archives[-3:]):  # Últimos 3 meses
                if len(all_games) >= max_games:
                    break
                
                try:
                    response = self.session.get(archive_url, timeout=self.timeout)
                    response.raise_for_status()
                    games = response.json().get("games", [])
                    
                    for game in games:
                        if len(all_games) >= max_games:
                            break
                        
                        if time_control == TimeControl.ALL:
                            all_games.append(game)
                        elif game.get("time_class") == time_control.value:
                            all_games.append(game)
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except requests.RequestException as e:
                    logger.warning(f"Erro ao buscar arquivo: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Erro ao buscar arquivos: {e}")
        
        return all_games[:max_games]
    
    def _processar_games(self, games_data: List[Dict], username: str) -> pd.DataFrame:
        """
        Processa dados brutos de games para DataFrame.
        
        Args:
            games_data: Lista de dicionários de games
            username: Nome do usuário
            
        Returns:
            DataFrame processado
        """
        processed = []
        
        for game in games_data:
            try:
                white = game.get("white", {})
                black = game.get("black", {})
                
                # Determinar cor do jogador
                if white.get("username", "").lower() == username.lower():
                    player_color = "white"
                    opponent = black
                    player_rating = white.get("rating")
                    opponent_rating = black.get("rating")
                elif black.get("username", "").lower() == username.lower():
                    player_color = "black"
                    opponent = white
                    player_rating = black.get("rating")
                    opponent_rating = white.get("rating")
                else:
                    continue
                
                # Extrair resultado
                result = game.get("result", "")
                if player_color == "white":
                    if result == "win":
                        outcome = "Win"
                    elif result == "loss":
                        outcome = "Loss"
                    else:
                        outcome = "Draw"
                else:  # black
                    if result == "win":
                        outcome = "Win"
                    elif result == "loss":
                        outcome = "Loss"
                    else:
                        outcome = "Draw"
                
                processed.append({
                    "url": game.get("url", ""),
                    "date": datetime.fromtimestamp(game.get("end_time", 0)),
                    "player_color": player_color,
                    "opponent": opponent.get("username", "Unknown"),
                    "player_rating": player_rating,
                    "opponent_rating": opponent_rating,
                    "time_class": game.get("time_class", ""),
                    "time_control": f"{game.get('time_control', 'N/A')}",
                    "outcome": outcome,
                    "pgn": game.get("pgn", ""),
                    "eco": self._extrair_eco(game.get("pgn", "")),
                })
            except Exception as e:
                logger.warning(f"Erro ao processar game: {e}")
                continue
        
        return pd.DataFrame(processed)
    
    def _extrair_eco(self, pgn: str) -> str:
        """Extrai código ECO do PGN."""
        for linha in pgn.split('\n'):
            if '[ECO' in linha and '"' in linha:
                return linha.split('"')[1]
        return "Unknown"
    
    def _salvar_cache(self, df: pd.DataFrame, path: Path) -> None:
        """Salva DataFrame em cache JSON."""
        try:
            df.to_json(path, orient="records", date_format='iso')
            logger.info(f"Cache salvo em {path}")
        except Exception as e:
            logger.warning(f"Erro ao salvar cache: {e}")
    
    def _carregar_cache(self, path: Path) -> pd.DataFrame:
        """Carrega DataFrame do cache JSON."""
        with open(path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df
