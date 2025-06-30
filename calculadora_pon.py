from dataclasses import dataclass, fields
from typing import Optional, List, Tuple, Dict

# Dicionário com perdas de inserção típicas para splitters ópticos (em dB).
SPLITTER_PERDAS: Dict[str, float] = {
    "1:2": 3.8,
    "1:4": 7.3,
    "1:8": 10.7,
    "1:16": 14.1,
    "1:32": 17.5,
    "1:64": 21.0,
}

# Dicionário de faixas típicas para validação e interface.
FAIXAS_TIPICAS = {
    "p_tx_dbm": (1.0, 7.0, "Potência de Transmissão (Tx)"),
    "s_rx_dbm": (-30.0, -25.0, "Sensibilidade de Recepção (Rx)"),
    "atenuacao_db_km": (0.2, 0.50, "Atenuação da Fibra"),
    "perda_conector_db": (0.2, 0.75, "Perda por Conector"),
    "margem_seguranca_db": (1.5, 3.0, "Margem de Segurança")
}

# -----------------------------------------------------------------------------
# PARTE 1: CLASSE DE DADOS E VALIDAÇÃO (MODELO)
# -----------------------------------------------------------------------------

@dataclass
class ParametrosPON:
    """Armazena todos os parâmetros de um enlace PON."""
    p_tx_dbm: Optional[float]
    s_rx_dbm: Optional[float]
    comprimento_km: Optional[float]
    atenuacao_db_km: Optional[float]
    perda_conector_db: Optional[float]
    num_conectores: Optional[int]
    perda_splitter_db: Optional[float]
    margem_seguranca_db: Optional[float]

    def validar_valores(self) -> List[str]:
        """Verifica se os valores fornecidos estão dentro de uma faixa convencional."""
        alertas = []
        for nome_param, (min_val, max_val, desc) in FAIXAS_TIPICAS.items():
            valor = getattr(self, nome_param)
            if valor is not None and not (min_val <= valor <= max_val):
                alerta = (f"ALERTA: O valor de '{desc}' ({valor}) está fora da faixa "
                          f"típica de mercado ({min_val} a {max_val}).")
                alertas.append(alerta)
        return alertas

    def encontrar_variavel_faltante(self) -> Tuple[Optional[str], int]:
        """Identifica qual variável não foi preenchida (está como None)."""
        faltantes = []
        for field in fields(self):
            if getattr(self, field.name) is None:
                faltantes.append(field.name)
        if len(faltantes) == 0:
            return None, 0
        return faltantes[0], len(faltantes)

# -----------------------------------------------------------------------------
# PARTE 2: CLASSE DE CÁLCULO (LÓGICA DE NEGÓCIO)
# -----------------------------------------------------------------------------

class CalculadoraPON:
    """Executa os cálculos de orçamento de potência da rede PON."""
    def __init__(self, params: ParametrosPON):
        self.params = params

    def calcular(self) -> str:
        variavel_faltante, num_faltantes = self.params.encontrar_variavel_faltante()
        if num_faltantes > 1:
            raise ValueError("Mais de uma variável foi deixada em branco. O cálculo é impossível.")
        if num_faltantes == 0:
            # Se nada for deixado em branco, o padrão é calcular a margem de segurança.
            variavel_faltante = "margem_seguranca_db"
            
        mapa_calculos = {
            "p_tx_dbm": self._calcular_p_tx, "s_rx_dbm": self._calcular_s_rx,
            "comprimento_km": self._calcular_comprimento, "perda_splitter_db": self._calcular_perda_splitter,
            "margem_seguranca_db": self._calcular_margem_seguranca, "atenuacao_db_km": self._calcular_atenuacao,
            "num_conectores": self._calcular_num_conectores, "perda_conector_db": self._calcular_perda_conector
        }
        if variavel_faltante in mapa_calculos:
            return mapa_calculos[variavel_faltante]()
        return "Erro: Variável desconhecida para cálculo."

    def _get_perdas_parciais(self, ignorar: str = "") -> float:
        p = self.params
        perda = 0.0
        if "fibra" not in ignorar and all(v is not None for v in [p.atenuacao_db_km, p.comprimento_km]):
            perda += p.atenuacao_db_km * p.comprimento_km
        if "conectores" not in ignorar and all(v is not None for v in [p.perda_conector_db, p.num_conectores]):
            perda += p.perda_conector_db * p.num_conectores
        if "splitter" not in ignorar and p.perda_splitter_db is not None:
            perda += p.perda_splitter_db
        return perda

    # ... Colar todos os seus métodos _calcular_... aqui ...
    # (Eles estão corretos e não precisam de alteração)
    def _calcular_margem_seguranca(self) -> str:
        p = self.params
        orcamento_potencia = p.p_tx_dbm - p.s_rx_dbm
        perda_total = self._get_perdas_parciais()
        margem = orcamento_potencia - perda_total
        resultado = (f"Cálculo da Margem de Segurança Resultante:\n"
                     f"  - Orçamento de Potência Bruto: {orcamento_potencia:.2f} dB\n"
                     f"  - Perda Total Estimada do Enlace: {perda_total:.2f} dB\n"
                     f"  - MARGEM DE SEGURANÇA: {margem:.2f} dB\n")
        if margem < 0:
            resultado += "\n  - ATENÇÃO: A margem é negativa. O projeto é INVIÁVEL."
        elif margem < 1.5:
            resultado += "\n  - AVISO: A margem é positiva, mas muito baixa (< 1.5 dB). Risco de instabilidade."
        else:
            resultado += "\n  - O projeto é VIÁVEL com a margem calculada."
        return resultado
    
    def _calcular_p_tx(self) -> str:
        p = self.params
        perda_total = self._get_perdas_parciais()
        p_tx_minima = p.s_rx_dbm + perda_total + p.margem_seguranca_db
        return (f"Para cobrir as perdas de {perda_total:.2f} dB, atender a sensibilidade de {p.s_rx_dbm} dBm "
                f"e garantir uma margem de {p.margem_seguranca_db} dB,\n"
                f"a potência de transmissão mínima necessária é:\n\n"
                f"  -> Potência de Transmissão (Tx) Mínima: {p_tx_minima:.2f} dBm")

    def _calcular_s_rx(self) -> str:
        p = self.params
        perda_total = self._get_perdas_parciais()
        potencia_recebida = p.p_tx_dbm - perda_total - p.margem_seguranca_db
        return (f"Com Tx={p.p_tx_dbm} dBm, perdas={perda_total:.2f} dB e margem={p.margem_seguranca_db} dB,\n"
                f"a potência final no receptor será de {potencia_recebida:.2f} dBm.\n"
                f"Portanto, a sensibilidade máxima do receptor deve ser:\n\n"
                f"  -> Sensibilidade de Recepção (Rx) Máxima: {potencia_recebida:.2f} dBm")

    def _calcular_comprimento(self) -> str:
        p = self.params
        orcamento_liquido = p.p_tx_dbm - p.s_rx_dbm - p.margem_seguranca_db
        perdas_fixas = self._get_perdas_parciais(ignorar="fibra")
        orcamento_para_fibra = orcamento_liquido - perdas_fixas
        if p.atenuacao_db_km is None or p.atenuacao_db_km <= 0:
            return "ERRO: Atenuação da fibra deve ser um valor positivo para este cálculo."
        if orcamento_para_fibra < 0:
            return (f"O orçamento ({orcamento_liquido:.2f} dB) não cobre as perdas fixas ({perdas_fixas:.2f} dB).\n"
                    "O alcance máximo é zero.")
        comprimento_max = orcamento_para_fibra / p.atenuacao_db_km
        return (f"Com um orçamento líquido de {orcamento_liquido:.2f} dB e perdas fixas de {perdas_fixas:.2f} dB,\n"
                f"restam {orcamento_para_fibra:.2f} dB para a fibra. Portanto:\n\n"
                f"  -> Alcance Máximo da Fibra: {comprimento_max:.2f} km")

    def _calcular_perda_splitter(self) -> str:
        p = self.params
        orcamento_liquido = p.p_tx_dbm - p.s_rx_dbm - p.margem_seguranca_db
        perdas_sem_splitter = self._get_perdas_parciais(ignorar="splitter")
        perda_max_splitter = orcamento_liquido - perdas_sem_splitter
        if perda_max_splitter < 0:
            return (f"O orçamento ({orcamento_liquido:.2f} dB) não cobre as outras perdas ({perdas_sem_splitter:.2f} dB).\n"
                    "Não há margem para um splitter.")
        melhor_splitter = "Nenhum splitter padrão compatível"
        for ratio, perda in sorted(SPLITTER_PERDAS.items(), key=lambda item: item[1]):
            if perda <= perda_max_splitter:
                melhor_splitter = f"{ratio} (perda típica de {perda} dB)"
        return (f"Considerando o orçamento e as outras perdas, a perda máxima que o splitter pode introduzir é:\n"
                f"  -> Perda Máxima do Splitter: {perda_max_splitter:.2f} dB\n\n"
                f"  -> RECOMENDAÇÃO: Você pode usar um splitter de até {melhor_splitter}.")

    def _calcular_atenuacao(self) -> str:
        p = self.params
        orcamento_liquido = p.p_tx_dbm - p.s_rx_dbm - p.margem_seguranca_db
        perdas_fixas = self._get_perdas_parciais(ignorar="fibra")
        orcamento_para_fibra = orcamento_liquido - perdas_fixas
        if p.comprimento_km is None or p.comprimento_km <= 0:
            return "ERRO: Comprimento da fibra deve ser um valor positivo para este cálculo."
        if orcamento_para_fibra < 0:
            return (f"O orçamento ({orcamento_liquido:.2f} dB) não cobre as perdas fixas ({perdas_fixas:.2f} dB).\n"
                    "Cálculo de atenuação inviável.")
        atenuacao_max = orcamento_para_fibra / p.comprimento_km
        return (f"Para o enlace funcionar com as perdas e margem especificadas,\n"
                f"a atenuação máxima da fibra deve ser:\n\n"
                f"  -> Atenuação Máxima: {atenuacao_max:.2f} dB/km")

    def _calcular_num_conectores(self) -> str:
        p = self.params
        orcamento_liquido = p.p_tx_dbm - p.s_rx_dbm - p.margem_seguranca_db
        perdas_fixas = self._get_perdas_parciais(ignorar="conectores")
        orcamento_para_conectores = orcamento_liquido - perdas_fixas
        if p.perda_conector_db is None or p.perda_conector_db <= 0:
            return "ERRO: A perda por conector deve ser um valor positivo para este cálculo."
        if orcamento_para_conectores < 0:
            return "O orçamento não cobre as outras perdas. Não há margem para nenhum conector."
        num_max_conectores = orcamento_para_conectores / p.perda_conector_db
        return (f"Com um orçamento restante de {orcamento_para_conectores:.2f} dB para os conectores,\n"
                f"o número máximo de conectores permitidos é:\n\n"
                f"  -> Número Máximo de Conectores: {int(num_max_conectores)}")

    def _calcular_perda_conector(self) -> str:
        p = self.params
        orcamento_liquido = p.p_tx_dbm - p.s_rx_dbm - p.margem_seguranca_db
        perdas_fixas = self._get_perdas_parciais(ignorar="conectores")
        orcamento_para_conectores = orcamento_liquido - perdas_fixas
        if p.num_conectores is None or p.num_conectores <= 0:
            return "ERRO: O número de conectores deve ser um valor positivo para este cálculo."
        if orcamento_para_conectores < 0:
            return "O orçamento não cobre as outras perdas. Cálculo inviável."
        perda_max_por_conector = orcamento_para_conectores / p.num_conectores
        return (f"Com um orçamento de {orcamento_para_conectores:.2f} dB para {p.num_conectores} conectores,\n"
                f"a perda máxima por conector deve ser:\n\n"
                f"  -> Perda Máxima por Conector: {perda_max_por_conector:.2f} dB")