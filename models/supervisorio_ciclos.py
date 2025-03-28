from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

class SupervisorioCiclosVapor(models.Model):
    _inherit = 'afr.supervisorio.ciclos'

    vapor_details = fields.Many2one('afr.supervisorio.ciclos.vapor.detalhes', string='Detalhes do Ciclo')
    vapor_temperature = fields.Float('Temperatura de Esterilização (°C)',
    related='vapor_details.vapor_temperature',
    help='Temperatura alvo para esterilização')
    vapor_pressure = fields.Float('Pressão de Esterilização (Bar)',
    related='vapor_details.vapor_pressure',
    help='Pressão alvo para esterilização')
    vapor_phases = fields.Integer('Número de Fases de Vácuo',
    related='vapor_details.vapor_phases',
    help='Número de fases de vácuo do ciclo')
    vapor_drying_time = fields.Float('Tempo de Secagem (min)',
    related='vapor_details.vapor_drying_time',
    help='Duração da fase de secagem')
    
    @api.model
    def create_cycle_data_vapor(self,header,body,values):
        """
        Cria os dados do ciclo de vapor a partir do cabeçalho e corpo recebidos.
        essa função é chamada dinamicamente pelo método create_new_cycle da classe SupervisorioCiclos
        o método create_new_cycle é chamado pelo método action_ler_diretorio_ciclos da classe SupervisorioCiclos
        que está na pasta afr_supervisorio_ciclos
        
        Args:
            header (dict): Dicionário contendo os parâmetros do cabeçalho do ciclo
                Exemplo de header: {'Data:': '13-4-2024', 'Hora:': '17:21:17', 'Equipamento:': 'ETO01', 
                'Operador:': 'FLAVIOR', 'Cod. ciclo:': '7819', 'Ciclo Selecionado:': 'CICLO 01'}
            body (dict): Dicionário contendo os dados do corpo do ciclo
            values (dict): Dicionário com valores iniciais a serem mesclados
            
        Returns:
            dict: Dicionário com os valores mesclados para criação do ciclo
            
        Este método extrai os dados relevantes do cabeçalho para criar um dicionário
        com os parâmetros do ciclo de vapor, como temperatura, pressão, número de fases
        e tempo de secagem.
        """
        #self.ensure_one()
       

        _logger.debug(f"Header do ciclo: {header}")  # Registra os dados para depuração
        
        # Cria um dicionário com os novos valores
        novos_valores = {
            'name': header['file_name'],
            'start_date': datetime.strptime(f"{header['Data:']} {header['Hora:']}", "%d-%m-%Y %H:%M:%S"),
            #'operator_id': header['Operador:'], #TODO: Fazer uma tabela de operadores e associar a esse apelido ao hr.employee.name
            'batch_number': header['Cod. ciclo:'],
            'state': 'em_andamento',
        }
        
        # Mescla os valores recebidos com os novos valores
        values.update(novos_valores)
        ciclo = self.create(values)
        
        _logger.debug(f"Body do ciclo: {values}")  # Registra os dados para depuração
        
        return ciclo
 
class SupervisorioCiclosVaporDetalhes(models.Model):
    _name = 'afr.supervisorio.ciclos.vapor.detalhes'
    _description = 'Detalhes do Ciclo de Esterilização por Vapor'

   
    vapor_temperature = fields.Float('Temperatura de Esterilização (°C)', help='Temperatura alvo para esterilização')
    vapor_pressure = fields.Float('Pressão de Esterilização (Bar)', help='Pressão alvo para esterilização')
    vapor_phases = fields.Integer('Número de Fases de Vácuo', help='Número de fases de vácuo do ciclo')
    vapor_drying_time = fields.Float('Tempo de Secagem (min)', help='Duração da fase de secagem') 
    