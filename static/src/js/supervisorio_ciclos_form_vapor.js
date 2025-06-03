/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { useService, useEffect } from "@web/core/utils/hooks";

/**
     * Repeatedly calls a callback function with a time delay between calls.
     */
function useInterval(callback, delay) {
    let intervalId;
    const { setInterval, clearInterval } = window;
    useEffect(() => {
        intervalId = setInterval(callback, delay);
        return () => clearInterval(intervalId);
    }, () => [delay]);
    return {
        pause: () => {
            clearInterval(intervalId);
            intervalId = undefined;
        },
        resume: () => {
            if (intervalId === undefined) {
                intervalId = setInterval(callback, delay);
            }
        },
    };
}

export class SupervisorioCiclosFormVaporController extends FormController {
    setup() {
        // Inicializa o serviço ORM para chamadas ao servidor
        this.orm = useService('orm');
        
        // Define os IDs ativos do contexto
        this.props.resIds = this.props.context.activeIds;
        
        // Chama o setup da classe pai
        super.setup();
        
        // Inicia o intervalo para atualização do gráfico a cada 10 segundos
        this.graphUpdateInterval = window.setInterval(() => {
            console.log("Atualizando gráfico...");
            this.updateCycleGraph();
        }, 10000);
    }
    
    // Método para atualizar o gráfico do ciclo e limpar o cache
    async updateCycleGraph() {
        try {
            // Chama o método compute_cycle_graph no modelo
            await this.model.root.load();
            const imageField = this.model.root.data.cycle_graph;  // substitua pelo nome do seu campo
            
            if (imageField) {
                // Atualiza o src da imagem com um timestamp
                const imageElement = document.querySelector('.cycle_graph_img');  // substitua pela classe da sua imagem
                if (imageElement) {
                    const timestamp = new Date().getTime();
                    imageElement.src = `/web/image?model=${this.model.root.resModel}&id=${this.model.root.resId}&field=cycle_graph&t=${timestamp}`;
                }
            }
            // Atualiza a visualização
            
            
        } catch (error) {
            console.error('Erro ao atualizar gráfico:', error);
        }
    }
    
    // Limpa o intervalo quando o componente é destruído
    onWillDestroy() {
        if (this.graphUpdateInterval) {
            clearInterval(this.graphUpdateInterval);
        }
        super.onWillDestroy();
    }
}

registry.category("views").add("supervisorio_ciclos_form_vapor", {
    ...formView,
    Controller: SupervisorioCiclosFormVaporController,
});



