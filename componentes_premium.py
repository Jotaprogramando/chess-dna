#!/usr/bin/env python3
"""
Chess DNA - Componentes Visuais Reutilizáveis
==============================================

Biblioteca de componentes Streamlit customizados para o dashboard premium.
Facilita a reutilização e manutenção de elementos visuais.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# ============================================================================
# CORES E PALETA
# ============================================================================

class PaletaCores:
    """Paleta de cores do Chess DNA."""
    
    # Cores primárias
    DOURADO = "#D4AF37"
    CIANO = "#58A6FF"
    VERMELHO = "#F85149"
    VERDE = "#3FB950"
    LARANJA = "#D29922"
    
    # Cores neutras
    BG_DARK = "#0E1117"
    BG_SECONDARY = "#161B22"
    TEXT_PRIMARY = "#F0F6FC"
    TEXT_SECONDARY = "#C9D1D9"
    TEXT_MUTED = "#8B949E"
    BORDER = "#30363D"
    
    # Gradientes
    GRADIENT_BLUE = "linear-gradient(135deg, #1F6FEB 0%, #0969DA 100%)"
    GRADIENT_DARK = "linear-gradient(135deg, rgba(22, 27, 34, 0.7) 0%, rgba(13, 17, 23, 0.5) 100%)"


class ComponentesCSS:
    """CSS reutilizáveis para componentes."""
    
    @staticmethod
    def get_metric_card_css(border_color: str = PaletaCores.DOURADO) -> str:
        """Retorna CSS para cards de métrica com glassmorphism."""
        return f"""
        <style>
            .metric-card-premium {{
                background: linear-gradient(135deg, rgba(22, 27, 34, 0.7) 0%, rgba(13, 17, 23, 0.5) 100%);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(212, 175, 55, 0.2);
                border-left: 4px solid {border_color};
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }}
            
            .metric-card-premium:hover {{
                background: linear-gradient(135deg, rgba(22, 27, 34, 0.9) 0%, rgba(13, 17, 23, 0.7) 100%);
                border-color: rgba(212, 175, 55, 0.4);
                box-shadow: 0 12px 48px rgba(212, 175, 55, 0.15);
                transform: translateY(-4px);
            }}
        </style>
        """

# ============================================================================
# COMPONENTES DE HEADER
# ============================================================================

class Header:
    """Componentes de cabeçalho."""
    
    @staticmethod
    def principal(titulo: str = "CHESS DNA", subtitulo: str = "Profiler de Estilo e Padrões Psicológicos"):
        """Renderiza o header principal."""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="padding-top: 10px;">
                <h1 style="color: {PaletaCores.DOURADO}; font-size: 3.5em; margin: 0; letter-spacing: 3px;">
                    ♟️ {titulo}
                </h1>
                <p style="color: {PaletaCores.TEXT_MUTED}; font-size: 1.1em; margin-top: 5px; letter-spacing: 1px;">
                    {subtitulo}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            status_cor = PaletaCores.VERDE
            st.markdown(f"""
            <div style="text-align: right; padding-top: 15px;">
                <p style="color: {PaletaCores.CIANO}; font-size: 0.9em; margin: 0;">
                    🔄 Última atualização: {datetime.now().strftime('%H:%M')}
                </p>
                <p style="color: {status_cor}; font-size: 0.9em; margin: 5px 0;">
                    ✓ Conexão Ativa
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<hr style="margin: 20px 0; border: 1px solid #30363D;">', unsafe_allow_html=True)
    
    @staticmethod
    def secao(titulo: str, icone: str = "📊"):
        """Renderiza um header de seção."""
        st.markdown(f"""
        <h2 style="color: {PaletaCores.TEXT_PRIMARY}; margin-top: 40px; margin-bottom: 20px; letter-spacing: 1px;">
            {icone} {titulo}
        </h2>
        """, unsafe_allow_html=True)


# ============================================================================
# COMPONENTES DE MÉTRICAS
# ============================================================================

class Metricas:
    """Componentes para exibição de métricas."""
    
    @staticmethod
    def card(label: str, value: str, icon: str, delta: Optional[str] = None, 
             color: str = PaletaCores.DOURADO):
        """Renderiza um card de métrica com glassmorphism."""
        delta_html = f'<span style="color: {PaletaCores.VERDE}; font-size: 0.85em; margin-left: 10px;">📈 {delta}</span>' if delta else ''
        
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: {PaletaCores.TEXT_MUTED}; font-size: 0.9em; margin: 0; text-transform: uppercase; letter-spacing: 1px;">
                        {icon} {label}
                    </p>
                    <p style="color: {color}; font-size: 2.2em; margin: 10px 0; font-weight: 900;">
                        {value}
                    </p>
                </div>
            </div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def grid_2x2(metricas: List[Tuple[str, str, str, str, Optional[str]]]):
        """Renderiza uma grid 2x2 de métricas.
        
        Args:
            metricas: Lista de tuplas (label, value, icon, color, delta)
        """
        col1, col2 = st.columns(2)
        
        for i, (label, value, icon, color, delta) in enumerate(metricas):
            if i % 2 == 0:
                with col1:
                    Metricas.card(label, value, icon, delta, color)
            else:
                with col2:
                    Metricas.card(label, value, icon, delta, color)
    
    @staticmethod
    def grid_4x1(metricas: List[Tuple[str, str, str, str, Optional[str]]]):
        """Renderiza uma grid 4x1 de métricas."""
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (label, value, icon, color, delta) in enumerate(metricas):
            with cols[i]:
                Metricas.card(label, value, icon, delta, color)


# ============================================================================
# COMPONENTES DE GRÁFICOS
# ============================================================================

class Graficos:
    """Componentes para gráficos Plotly."""
    
    @staticmethod
    def _config_layout_padrao(titulo: str = "", altura: int = 400) -> Dict:
        """Retorna configuração de layout padrão."""
        return {
            'title': dict(
                text=f'<b>{titulo}</b>' if titulo else '',
                font=dict(size=14, color=PaletaCores.TEXT_PRIMARY),
                x=0.5,
                xanchor='center'
            ) if titulo else {},
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': dict(family="Arial, sans-serif", color=PaletaCores.TEXT_SECONDARY),
            'hovermode': 'closest',
            'height': altura,
            'margin': dict(l=60, r=20, t=50, b=60),
        }
    
    @staticmethod
    def radar(data: Dict, titulo: str = "") -> go.Figure:
        """Cria um radar chart elegante."""
        fig = go.Figure(data=go.Scatterpolar(
            r=list(data.values()),
            theta=list(data.keys()),
            fill='toself',
            name='Estilo',
            line=dict(color=PaletaCores.DOURADO, width=2),
            fillcolor=f'rgba(212, 175, 55, 0.2)',
            hoverinfo='theta+r',
        ))
        
        layout = Graficos._config_layout_padrao(titulo)
        layout.update({
            'polar': dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor=PaletaCores.BORDER,
                    gridwidth=1,
                    linecolor=PaletaCores.BORDER,
                    tickcolor=PaletaCores.TEXT_MUTED,
                    tickfont=dict(color=PaletaCores.TEXT_MUTED, size=10),
                ),
                angularaxis=dict(
                    gridcolor=PaletaCores.BORDER,
                    linecolor=PaletaCores.BORDER,
                    tickcolor=PaletaCores.TEXT_MUTED,
                    tickfont=dict(color=PaletaCores.TEXT_SECONDARY, size=11),
                ),
                bgcolor='rgba(13, 17, 23, 0.5)',
            ),
            'showlegend': False,
        })
        
        fig.update_layout(**layout)
        return fig
    
    @staticmethod
    def heatmap(data: np.ndarray, x_labels: List[str], y_labels: List[str], 
                titulo: str = "") -> go.Figure:
        """Cria um heatmap."""
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=x_labels,
            y=y_labels,
            colorscale=[
                [0, PaletaCores.BG_DARK],
                [0.3, PaletaCores.VERDE],
                [0.6, PaletaCores.LARANJA],
                [1, PaletaCores.VERMELHO]
            ],
            hovertemplate='<b>%{y}</b><br>%{x}<br>Score: %{z}<extra></extra>',
            showscale=True,
            colorbar=dict(
                tickfont=dict(color=PaletaCores.TEXT_MUTED),
                thickness=20,
                len=0.7,
            )
        ))
        
        layout = Graficos._config_layout_padrao(titulo, 400)
        layout.update({
            'xaxis': dict(
                side='bottom',
                tickcolor=PaletaCores.TEXT_MUTED,
                tickfont=dict(color=PaletaCores.TEXT_SECONDARY, size=11),
                showgrid=False,
            ),
            'yaxis': dict(
                tickcolor=PaletaCores.TEXT_MUTED,
                tickfont=dict(color=PaletaCores.TEXT_SECONDARY, size=11),
                showgrid=False,
            ),
        })
        
        fig.update_layout(**layout)
        return fig
    
    @staticmethod
    def linha(df: pd.DataFrame, x: str, y: str, nome: str = "", titulo: str = "") -> go.Figure:
        """Cria um gráfico de linha."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y],
            name=nome or y,
            line=dict(color=PaletaCores.CIANO, width=3),
            fill='tozeroy',
            fillcolor=f'rgba(88, 166, 255, 0.2)',
            hovertemplate=f'<b>%{{x}}</b><br>{nome}: %{{y:.1f}}<extra></extra>',
        ))
        
        layout = Graficos._config_layout_padrao(titulo, 400)
        layout.update({
            'xaxis': dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=PaletaCores.BORDER,
                tickfont=dict(color=PaletaCores.TEXT_MUTED, size=10),
            ),
            'yaxis': dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=PaletaCores.BORDER,
                tickfont=dict(color=PaletaCores.TEXT_MUTED, size=10),
            ),
            'hovermode': 'x unified',
        })
        
        fig.update_layout(**layout)
        return fig
    
    @staticmethod
    def barras(df: pd.DataFrame, x: str, y: str, titulo: str = "") -> go.Figure:
        """Cria um gráfico de barras."""
        fig = go.Figure(data=[
            go.Bar(
                x=df[x],
                y=df[y],
                marker=dict(
                    color=df[y],
                    colorscale=[
                        [0, PaletaCores.VERMELHO],
                        [0.5, PaletaCores.LARANJA],
                        [1, PaletaCores.VERDE]
                    ],
                    showscale=False,
                ),
                hovertemplate='<b>%{x}</b><br>%{y:.1f}<extra></extra>',
            )
        ])
        
        layout = Graficos._config_layout_padrao(titulo, 400)
        layout.update({
            'xaxis': dict(
                tickfont=dict(color=PaletaCores.TEXT_MUTED),
                showgrid=False,
            ),
            'yaxis': dict(
                tickfont=dict(color=PaletaCores.TEXT_MUTED),
                showgrid=True,
                gridcolor=PaletaCores.BORDER,
            ),
        })
        
        fig.update_layout(**layout)
        return fig


# ============================================================================
# COMPONENTES DE LAYOUT
# ============================================================================

class Layout:
    """Componentes para estrutura de layout."""
    
    @staticmethod
    def divider():
        """Renderiza um divider elegante."""
        st.markdown(
            '<hr style="height: 2px; background: linear-gradient(90deg, transparent, #D4AF37, transparent); margin: 30px 0; border: none;">',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def info_box(titulo: str, mensagem: str, tipo: str = "info", icone: str = "ℹ️"):
        """Renderiza uma caixa de informação.
        
        Args:
            titulo: Título da caixa
            mensagem: Mensagem
            tipo: "info", "success", "warning", "error"
            icone: Ícone a usar
        """
        cores = {
            "info": ("#58A6FF", PaletaCores.CIANO),
            "success": ("#3FB950", PaletaCores.VERDE),
            "warning": ("#D29922", PaletaCores.LARANJA),
            "error": ("#F85149", PaletaCores.VERMELHO),
        }
        
        cor_border, cor_texto = cores.get(tipo, cores["info"])
        
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {cor_border};">
            <p style="color: {cor_border}; font-size: 1em; margin: 0; font-weight: 700;">
                {icone} {titulo}
            </p>
            <p style="color: {PaletaCores.TEXT_SECONDARY}; font-size: 0.95em; margin-top: 8px; margin-bottom: 0;">
                {mensagem}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def tabs_premium(nomes_abas: List[str]):
        """Retorna tabs premium."""
        return st.tabs(nomes_abas)


# ============================================================================
# COMPONENTES DE SIDEBAR
# ============================================================================

class Sidebar:
    """Componentes para a sidebar."""
    
    @staticmethod
    def header(titulo: str = "⚙️ Configurações"):
        """Renderiza o header da sidebar."""
        st.markdown(f"""
        <h3 style="color: {PaletaCores.DOURADO}; margin-top: 0; letter-spacing: 1px;">
            {titulo}
        </h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<hr style="border: 1px solid {PaletaCores.BORDER}; margin: 15px 0;">', 
                   unsafe_allow_html=True)
    
    @staticmethod
    def input_username(placeholder: str = "Ex: hikaru, GoogleDeepMind"):
        """Input para username."""
        st.markdown(f'<p style="color: {PaletaCores.TEXT_MUTED}; font-size: 0.9em; margin-bottom: 5px;">Username</p>', 
                   unsafe_allow_html=True)
        return st.text_input(
            "Insira o username",
            value="Kasparov",
            label_visibility="collapsed",
            placeholder=placeholder
        )
    
    @staticmethod
    def select_plataforma():
        """Select para plataforma."""
        st.markdown(f'<p style="color: {PaletaCores.TEXT_MUTED}; font-size: 0.9em; margin: 15px 0 5px 0;">Plataforma</p>', 
                   unsafe_allow_html=True)
        return st.selectbox(
            "Escolha a plataforma",
            ["Chess.com", "Lichess.org"],
            label_visibility="collapsed"
        )
    
    @staticmethod
    def slider_partidas(min_val: int = 10, max_val: int = 500, default: int = 100):
        """Slider para número de partidas."""
        st.markdown(f'<p style="color: {PaletaCores.TEXT_MUTED}; font-size: 0.9em; margin: 15px 0 5px 0;">Número de Partidas</p>', 
                   unsafe_allow_html=True)
        return st.slider(
            "Selecione quantidade",
            min_value=min_val,
            max_value=max_val,
            value=default,
            step=10,
            label_visibility="collapsed"
        )
    
    @staticmethod
    def select_tempo():
        """Select para tipo de tempo."""
        st.markdown(f'<p style="color: {PaletaCores.TEXT_MUTED}; font-size: 0.9em; margin: 15px 0 5px 0;">Tipo de Tempo</p>', 
                   unsafe_allow_html=True)
        return st.selectbox(
            "Filtro de tempo",
            ["Todos", "Bullet", "Blitz", "Rapid", "Classical"],
            label_visibility="collapsed"
        )
    
    @staticmethod
    def botoes_acao():
        """Renderiza botões de ação."""
        st.markdown(f'<hr style="border: 1px solid {PaletaCores.BORDER}; margin: 20px 0;">', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            btn_analisar = st.button("🔍 Analisar", use_container_width=True)
        
        with col2:
            btn_atualizar = st.button("🔄 Atualizar", use_container_width=True)
        
        return btn_analisar, btn_atualizar
    
    @staticmethod
    def dica():
        """Renderiza uma dica na sidebar."""
        Layout.info_box(
            "💡 Dica",
            "Use 'Blitz' ou 'Rapid' para análises mais rápidas.",
            tipo="info"
        )


# ============================================================================
# COMPONENTES DE FOOTER
# ============================================================================

class Footer:
    """Componentes para rodapé."""
    
    @staticmethod
    def padrao(versao: str = "0.5.0"):
        """Renderiza footer padrão."""
        st.markdown(f'<hr style="border: 1px solid {PaletaCores.BORDER}; margin: 30px 0;">', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; color: {PaletaCores.TEXT_MUTED}; font-size: 0.85em;">
                <p>Dashboard Premium</p>
                <p>Chess DNA v{versao}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; color: {PaletaCores.TEXT_MUTED}; font-size: 0.85em;">
                <p>Atualizado em</p>
                <p>{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; color: {PaletaCores.TEXT_MUTED}; font-size: 0.85em;">
                <p>Powered by</p>
                <p>Streamlit & Plotly</p>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'PaletaCores',
    'ComponentesCSS',
    'Header',
    'Metricas',
    'Graficos',
    'Layout',
    'Sidebar',
    'Footer',
]
