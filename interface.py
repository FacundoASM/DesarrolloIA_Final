import gradio as gr
import requests
import json
from typing import Dict, List, Tuple, Optional

# Configuración de la API (ajustar si es necesario)
API_BASE_URL = "http://localhost:8000"

class DiagnosticoHidroponicoUI:
    def __init__(self):
        self.rangos_optimos = {
            "ph": (5.8, 6.2),
            "ce": (1.4, 1.8),
            "temp_solucion": (18, 22),
            "humedad": (60, 75),
            "horas_luz": (12, 16)
        }
    
    def obtener_rangos_cultivo(self, cultivo: str, etapa: str) -> str:
        """Obtiene y muestra los rangos óptimos para el cultivo seleccionado"""
        try:
            response = requests.get(f"{API_BASE_URL}/rangos-optimos/{cultivo}/{etapa}")
            if response.status_code == 200:
                rangos = response.json()["rangos_optimos"]
                texto = f"📊 **Rangos óptimos para {cultivo.title()} - {etapa.replace('_', ' ').title()}:**\n\n"
                texto += f"• **pH:** {rangos['ph'][0]} - {rangos['ph'][1]}\n"
                texto += f"• **CE:** {rangos['ce'][0]} - {rangos['ce'][1]} mS/cm\n"
                texto += f"• **Temp. solución:** {rangos['temp_solucion'][0]} - {rangos['temp_solucion'][1]}°C\n"
                texto += f"• **Humedad:** {rangos['humedad'][0]} - {rangos['humedad'][1]}%\n"
                texto += f"• **Horas luz:** {rangos['horas_luz'][0]} - {rangos['horas_luz'][1]}h\n"
                return texto
            else:
                return "⚠️ No se pudieron obtener los rangos óptimos"
        except:
            return "⚠️ Error de conexión con la API"
    
    def realizar_diagnostico(
        self,
        cultivo: str,
        etapa: str,
        sintomas_visuales: bool,
        tipo_sintoma: str,
        ph: float,
        ce: float,
        temp_solucion: float,
        humedad: float,
        temp_ambiente: float,
        horas_luz: float,
        dias_renovacion: int,
        bomba_funcionando: bool
    ) -> Tuple[str, str, str]:
        """Realiza el diagnóstico y retorna resultado formateado"""
        
        # Preparar datos para la API
        payload = {
            "cultivo": cultivo,
            "etapa": etapa,
            "sintomas_visuales": sintomas_visuales,
            "tipo_sintoma": tipo_sintoma if sintomas_visuales else None,
            "parametros": {
                "ph": ph,
                "conductividad_electrica": ce,
                "temperatura_solucion": temp_solucion,
                "humedad_relativa": humedad,
                "temperatura_ambiente": temp_ambiente,
                "horas_luz_diarias": horas_luz,
                "dias_desde_renovacion": dias_renovacion,
                "bomba_oxigenacion_funcionando": bomba_funcionando
            }
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/diagnostico", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                return self.formatear_resultado(resultado)
            else:
                error_msg = f"❌ Error en la API: {response.status_code}"
                return error_msg, "", ""
                
        except requests.exceptions.ConnectionError:
            error_msg = "❌ **Error de conexión**\n\nNo se puede conectar con la API. Asegúrate de que el servidor esté ejecutándose en http://localhost:8000"
            return error_msg, "", ""
        except Exception as e:
            error_msg = f"❌ **Error inesperado**: {str(e)}"
            return error_msg, "", ""
    
    def formatear_resultado(self, resultado: Dict) -> Tuple[str, str, str]:
        """Formatea el resultado del diagnóstico para la interfaz"""
        
        # Diagnóstico principal
        diagnostico_texto = f"# {resultado['diagnostico']}\n\n"
        
        if resultado['parametros_criticos']:
            diagnostico_texto += "🚨 **Parámetros críticos detectados:**\n"
            for param in resultado['parametros_criticos']:
                diagnostico_texto += f"• {param.replace('_', ' ').title()}\n"
            diagnostico_texto += "\n"
        
        # Acciones recomendadas
        acciones_texto = "## 📋 Acciones Recomendadas\n\n"
        
        # Agrupar por prioridad
        acciones_por_prioridad = {}
        for accion in resultado['acciones']:
            prioridad = accion['prioridad']
            if prioridad not in acciones_por_prioridad:
                acciones_por_prioridad[prioridad] = []
            acciones_por_prioridad[prioridad].append(accion)
        
        # Mostrar por orden de prioridad
        orden_prioridad = ['critica', 'alta', 'media', 'baja']
        iconos_prioridad = {
            'critica': '🚨',
            'alta': '⚠️',
            'media': '📋',
            'baja': 'ℹ️'
        }
        
        for prioridad in orden_prioridad:
            if prioridad in acciones_por_prioridad:
                acciones_texto += f"### {iconos_prioridad[prioridad]} Prioridad {prioridad.title()}\n\n"
                for accion in acciones_por_prioridad[prioridad]:
                    acciones_texto += f"**{accion['tipo'].replace('_', ' ').title()}:**\n"
                    acciones_texto += f"{accion['descripcion']}\n"
                    acciones_texto += f"*⏱️ Revisar en: {accion['tiempo_revision']}*\n\n"
        
        # Observaciones específicas del clima
        observaciones_texto = ""
        if resultado['observaciones_clima_fueguino']:
            observaciones_texto = "## 🌪️ Consideraciones Clima Fueguino\n\n"
            for obs in resultado['observaciones_clima_fueguino']:
                observaciones_texto += f"• {obs}\n"
        
        return diagnostico_texto, acciones_texto, observaciones_texto
    
    def verificar_api(self) -> str:
        """Verifica si la API está funcionando"""
        try:
            response = requests.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                return "✅ API conectada correctamente"
            else:
                return f"⚠️ API respondió con código: {response.status_code}"
        except:
            return "❌ No se puede conectar con la API"

# Crear instancia del diagnóstico
diagnostico_ui = DiagnosticoHidroponicoUI()

# Definir la interfaz de Gradio
def crear_interfaz():
    with gr.Blocks(
        title="🌱 Diagnóstico Hidropónico - Tierra del Fuego",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .primary-button {
            background: linear-gradient(45deg, #4CAF50, #45a049) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }
        .diagnostic-result {
            border-left: 4px solid #4CAF50;
            padding-left: 1rem;
            background-color: #f8f9fa;
            color: #2E7D32 !important;
        }
        .diagnostic-result h1, .diagnostic-result h2, .diagnostic-result h3 {
            color: #1B5E20 !important;
        }
        .diagnostic-result p, .diagnostic-result li {
            color: #2E7D32 !important;
        }
        /* Para pestañas de resultados */
        .tab-nav button[data-testid="tab-header"] {
            color: #4CAF50 !important;
        }
        /* Para el contenido de las pestañas de acciones y observaciones */
        .tab-content {
            color: #2E7D32 !important;
        }
        """
    ) as interfaz:
        
        # Título y descripción
        gr.Markdown("""
        # 🌱 Sistema de Diagnóstico Hidropónico
        ## Especializado para el clima de Tierra del Fuego
        
        Esta herramienta te ayudará a diagnosticar problemas en tu sistema hidropónico, 
        considerando las condiciones específicas del clima fueguino.
        """)
        
        # Estado de la API
        with gr.Row():
            estado_api = gr.Markdown(diagnostico_ui.verificar_api())
            btn_verificar = gr.Button("🔄 Verificar API", size="sm")
            btn_verificar.click(diagnostico_ui.verificar_api, outputs=estado_api)
        
        with gr.Row():
            # Columna izquierda: Inputs
            with gr.Column(scale=1):
                gr.Markdown("### 🌿 Información del Cultivo")
                
                cultivo = gr.Dropdown(
                    choices=["lechuga", "rucula", "microgreens", "aromaticas"],
                    label="Tipo de Cultivo",
                    value="lechuga"
                )
                
                etapa = gr.Dropdown(
                    choices=["germinacion", "crecimiento", "pre_cosecha", "cualquier_etapa"],
                    label="Etapa del Cultivo",
                    value="crecimiento"
                )
                
                # Mostrar rangos óptimos
                rangos_info = gr.Markdown("")
                
                def actualizar_rangos(cult, et):
                    return diagnostico_ui.obtener_rangos_cultivo(cult, et)
                
                cultivo.change(actualizar_rangos, inputs=[cultivo, etapa], outputs=rangos_info)
                etapa.change(actualizar_rangos, inputs=[cultivo, etapa], outputs=rangos_info)
                
                gr.Markdown("### 👁️ Síntomas Visuales")
                
                sintomas_visuales = gr.Checkbox(
                    label="¿Observas síntomas visuales alarmantes?",
                    value=False
                )
                
                tipo_sintoma = gr.Dropdown(
                    choices=[
                        "manchas_marrones_bordes_blandos",
                        "hojas_amarillas_desde_abajo", 
                        "crecimiento_lento_raices_marrones"
                    ],
                    label="Tipo de síntoma (si aplica)",
                    visible=False
                )
                
                def mostrar_sintomas(mostrar):
                    return gr.update(visible=mostrar)
                
                sintomas_visuales.change(mostrar_sintomas, inputs=sintomas_visuales, outputs=tipo_sintoma)
                
                gr.Markdown("### 📊 Parámetros del Sistema")
                
                with gr.Row():
                    ph = gr.Slider(
                        minimum=4.0, maximum=8.0, step=0.1, value=6.0,
                        label="pH de la solución"
                    )
                    ce = gr.Slider(
                        minimum=0.5, maximum=3.0, step=0.1, value=1.6,
                        label="Conductividad Eléctrica (mS/cm)"
                    )
                
                with gr.Row():
                    temp_solucion = gr.Slider(
                        minimum=10, maximum=30, step=0.5, value=20,
                        label="Temperatura Solución (°C)"
                    )
                    humedad = gr.Slider(
                        minimum=30, maximum=90, step=1, value=65,
                        label="Humedad Relativa (%)"
                    )
                
                with gr.Row():
                    temp_ambiente = gr.Slider(
                        minimum=-10, maximum=25, step=0.5, value=15,
                        label="Temperatura Ambiente (°C)"
                    )
                    horas_luz = gr.Slider(
                        minimum=8, maximum=20, step=0.5, value=14,
                        label="Horas de Luz Diarias"
                    )
                
                with gr.Row():
                    dias_renovacion = gr.Slider(
                        minimum=0, maximum=30, step=1, value=7,
                        label="Días desde renovación"
                    )
                    bomba_funcionando = gr.Checkbox(
                        label="Bomba de oxigenación funcionando",
                        value=True
                    )
                
                # Botón de diagnóstico
                btn_diagnostico = gr.Button(
                    "🔍 Realizar Diagnóstico",
                    elem_classes=["primary-button"],
                    size="lg"
                )
            
            # Columna derecha: Resultados
            with gr.Column(scale=1):
                gr.Markdown("### 📋 Resultado del Diagnóstico")
                
                with gr.Tab("🎯 Diagnóstico"):
                    resultado_diagnostico = gr.Markdown("", elem_classes=["diagnostic-result"])
                
                with gr.Tab("📝 Acciones"):
                    resultado_acciones = gr.Markdown("")
                
                with gr.Tab("🌪️ Clima Fueguino"):
                    resultado_observaciones = gr.Markdown("")
        
        # Configurar el botón de diagnóstico
        btn_diagnostico.click(
            diagnostico_ui.realizar_diagnostico,
            inputs=[
                cultivo, etapa, sintomas_visuales, tipo_sintoma,
                ph, ce, temp_solucion, humedad, temp_ambiente,
                horas_luz, dias_renovacion, bomba_funcionando
            ],
            outputs=[resultado_diagnostico, resultado_acciones, resultado_observaciones]
        )
        
        # Cargar rangos iniciales
        interfaz.load(
            lambda: diagnostico_ui.obtener_rangos_cultivo("lechuga", "crecimiento"),
            outputs=rangos_info
        )
        
        # Información adicional
        with gr.Accordion("ℹ️ Información Adicional", open=False):
            gr.Markdown("""
            ### Cómo usar esta herramienta:
            
            1. **Selecciona tu cultivo y etapa** - Esto determinará los rangos óptimos
            2. **Indica si hay síntomas visuales** - Si los hay, especifica el tipo
            3. **Ingresa los parámetros actuales** - Usa los medidores de tu sistema
            4. **Presiona 'Realizar Diagnóstico'** - Obtendrás recomendaciones específicas
            
            ### Consideraciones para Tierra del Fuego:
            - Las bajas temperaturas requieren calefacción constante
            - Los vientos fuertes pueden afectar la ventilación
            - La baja radiación solar necesita compensación con LED
            - El invierno requiere ajustes especiales en nutrición
            
            ### Contacto:
            Para soporte técnico o consultas específicas, consulta la documentación del sistema.
            """)
    
    return interfaz

# Función principal para ejecutar la interfaz
def main():
    interfaz = crear_interfaz()
    interfaz.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main()