from odoo import models, fields, api
import logging
from datetime import datetime,timedelta
_logger = logging.getLogger(__name__)


class SupervisorioCiclosVapor(models.Model):
    _inherit = 'afr.supervisorio.ciclos'

    @api.model
    def process_cycle_data_vapor_sercon_or_2011(self,header,body,values):
        """
        Cria ou atualiza os dados do ciclo de ETO a partir do cabeçalho e corpo recebidos.
        
        Este método é chamado dinamicamente pelo método create_new_cycle da classe SupervisorioCiclos,
        que por sua vez é chamado pelo método action_ler_diretorio_ciclos.
        
        Args:
            header (dict): Dicionário com parâmetros do cabeçalho do ciclo
                Exemplo: {
                    'Data:': '13-4-2024',
                    'Hora:': '17:21:17', 
                    'Equipamento:': 'ETO01',
                    'Operador:': 'FLAVIOR',
                    'Cod. ciclo:': '7819',
                    'Ciclo Selecionado:': 'CICLO 01'
                }
            body (dict): Dicionário com dados do corpo do ciclo
            values (dict): Valores iniciais a serem mesclados
            create (bool): Se True, cria novo ciclo. Se False, atualiza existente
            id_ciclo (int): ID do ciclo para atualização (necessário se create=False)
            
        Returns:
            record: Registro do ciclo criado/atualizado
            
        Raises:
            UserError: Se id_ciclo não informado ao tentar atualizar
        """

        # self.ensure_one()

        _logger.debug(f"Header do ciclo: {header}")


        # procurando o ciclo selecionado no dicionário header
        ciclo_selecionado = header['CICLO']
        cycle_type = self.cycle_type_id or self.equipment_id.cycle_type_id
        cycle_features_id = cycle_type.cycle_features_id.filtered(lambda x: x.name == ciclo_selecionado)

      
      
        hora_str = header['Hora:']
        data_obj = header['Data:']
        # Extraindo horas, minutos e segundos da string de hora
        data_completa = self.data_hora_to_datetime(data_obj,hora_str)
       

        
        novos_valores = {
            'name': header['file_name'],
            'start_date': data_completa,  # Remove timezone antes de salvar
            'batch_number': header['LOTE'],
            'cycle_features_id': cycle_features_id.id,
        }
        _logger.debug(f"Novos valores: {novos_valores}")
        values.update(novos_valores)
       
        _logger.debug(f"valores atualizados: {values}")
        #ciclo não existe, cria novo ciclo
        _logger.debug(f"self.id: {self.id}")
        if not self.id:
            ciclo = self.create(values)
            _logger.debug(f"Ciclo não existe, criando novo ciclo. Ciclo criado: {ciclo.name}")
            return ciclo
        #ciclo existe, atualiza ciclo
        #verificando se ciclo finalizou
        # procurando no body o valor de 'CICLO FINALIZADO'
        
        values['state'] = 'em_andamento'
        if body['state'] == 'concluido':
            values['state'] = 'concluido'

        if body['state'] == 'abortado':
            values['state'] = 'abortado'
        
        if body['state'] == 'em_andamento':          
            return self.write(values)
        
        try:
            _logger.debug(f"body: {body['fase']}")
            final_ciclo = list(filter(lambda x: x[1] == 'FINAL DO CICLO', body['fase']))
            _logger.debug(f"final_ciclo: {final_ciclo}")
            if final_ciclo:
                values['end_date'] = final_ciclo[0][0] + timedelta(hours=3)
                return self.write(values)

            _logger.debug(f"ultima data_hora: {body['data'][-1][0]}")
            data_fim =body['data'][-1][0]
            data_fim_ajustada = data_fim + timedelta(hours=3)
            values['end_date'] = data_fim_ajustada          
        except Exception as e:
            _logger.error(f"Erro ao obter data de finalização do ciclo: {e}")
            values['end_date'] = self.start_date 
            values['state'] = 'erro'

            
        return self.write(values)
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
         # Converte a string de hora para objeto time
        hora = datetime.strptime(header['Hora:'], '%H:%M:%S').time()
        # Cria um dicionário com os novos valores
        novos_valores = {
            'name': header['file_name'],
            'start_date': datetime.combine(header['Data:'].date(), hora),
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
    