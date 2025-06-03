from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum
import uvicorn

# Configuración de la aplicación
app = FastAPI(
    title="Sistema de Diagnóstico Hidropónico - Tierra del Fuego",
    description="API para diagnóstico automatizado de sistemas hidropónicos adaptado al clima de Tierra del Fuego",
    version="1.0.0"
)

# Enums para validación
class CultivoEnum(str, Enum):
    lechuga = "lechuga"
    rucula = "rucula"
    microgreens = "microgreens"
    aromaticas = "aromaticas"

class EtapaEnum(str, Enum):
    germinacion = "germinacion"
    crecimiento = "crecimiento"
    pre_cosecha = "pre_cosecha"
    cualquier_etapa = "cualquier_etapa"

class SintomaEnum(str, Enum):
    manchas_marrones_bordes_blandos = "manchas_marrones_bordes_blandos"
    hojas_amarillas_desde_abajo = "hojas_amarillas_desde_abajo"
    crecimiento_lento_raices_marrones = "crecimiento_lento_raices_marrones"

# Modelos Pydantic
class ParametrosAmbientales(BaseModel):
    ph: float = Field(..., ge=0, le=14, description="pH de la solución nutritiva")
    conductividad_electrica: float = Field(..., ge=0, description="CE en mS/cm")
    temperatura_solucion: float = Field(..., description="Temperatura de la solución en °C")
    humedad_relativa: float = Field(..., ge=0, le=100, description="Humedad relativa en %")
    temperatura_ambiente: float = Field(..., description="Temperatura ambiente en °C")
    horas_luz_diarias: float = Field(..., ge=0, le=24, description="Horas de luz diarias")
    dias_desde_renovacion: int = Field(..., ge=0, description="Días desde la última renovación de solución")
    bomba_oxigenacion_funcionando: bool = Field(True, description="Estado de la bomba de oxigenación")

class DiagnosticoInput(BaseModel):
    cultivo: CultivoEnum
    etapa: EtapaEnum
    sintomas_visuales: bool = Field(False, description="¿Hay síntomas visuales alarmantes?")
    tipo_sintoma: Optional[SintomaEnum] = None
    parametros: ParametrosAmbientales

class Accion(BaseModel):
    tipo: str
    descripcion: str
    prioridad: Literal["baja", "media", "alta", "critica"]
    tiempo_revision: str

class DiagnosticoOutput(BaseModel):
    diagnostico: str
    acciones: list[Accion]
    parametros_criticos: list[str]
    observaciones_clima_fueguino: list[str]

# Clase principal para el diagnóstico
class DiagnosticoHidroponico:
    
    @staticmethod
    def obtener_rangos_optimos(cultivo: str, etapa: str) -> dict:
        """Obtiene los rangos óptimos según cultivo y etapa"""
        rangos_base = {
            "ph": (5.8, 6.2),
            "ce": (1.4, 1.8),
            "temp_solucion": (18, 22),
            "humedad": (60, 75),
            "horas_luz": (12, 16)
        }
        
        # Ajustes específicos por cultivo
        if cultivo == "microgreens":
            rangos_base["ce"] = (1.2, 1.6)
        elif cultivo == "aromaticas":
            rangos_base["ce"] = (1.6, 2.0)
            
        return rangos_base
    
    @staticmethod
    def diagnosticar_sintomas(tipo_sintoma: str, parametros: ParametrosAmbientales) -> DiagnosticoOutput:
        """Diagnóstica basado en síntomas visuales"""
        acciones = []
        parametros_criticos = []
        observaciones = []
        
        if tipo_sintoma == "manchas_marrones_bordes_blandos":
            if parametros.humedad_relativa > 75:
                diagnostico = "🍄 BOTRYTIS DETECTADO"
                acciones = [
                    Accion(
                        tipo="fungicida",
                        descripcion="Aplicar fungicida biológico",
                        prioridad="critica",
                        tiempo_revision="24 horas"
                    ),
                    Accion(
                        tipo="ventilacion",
                        descripcion="Reducir HR < 70% y aumentar ventilación",
                        prioridad="critica",
                        tiempo_revision="inmediato"
                    )
                ]
                parametros_criticos = ["humedad_relativa"]
                observaciones = ["Cuidado con vientos fueguinos al ventilar"]
            else:
                diagnostico = "Evaluar otras causas de manchas"
                acciones = [
                    Accion(
                        tipo="monitoreo",
                        descripcion="Verificar estabilidad de temperatura",
                        prioridad="media",
                        tiempo_revision="24 horas"
                    )
                ]
                
        elif tipo_sintoma == "hojas_amarillas_desde_abajo":
            diagnostico = "Posible deficiencia nutricional"
            if parametros.temperatura_ambiente < 10:
                acciones = [
                    Accion(
                        tipo="calefaccion",
                        descripcion="❄️ Ajustar calefacción invernadero y revisar aislamiento",
                        prioridad="alta",
                        tiempo_revision="inmediato"
                    ),
                    Accion(
                        tipo="nutricion",
                        descripcion="Aumentar nutrientes 10% por estrés por frío",
                        prioridad="media",
                        tiempo_revision="24 horas"
                    )
                ]
                parametros_criticos = ["temperatura_ambiente"]
                observaciones = ["Crítico en invierno fueguino"]
            else:
                acciones = [
                    Accion(
                        tipo="nutricion",
                        descripcion="🌱 Revisar formulación NPK según etapa de cultivo",
                        prioridad="media",
                        tiempo_revision="48 horas"
                    )
                ]
                
        elif tipo_sintoma == "crecimiento_lento_raices_marrones":
            diagnostico = "Posible pudrición radicular"
            if parametros.temperatura_solucion > 24:
                acciones = [
                    Accion(
                        tipo="enfriamiento",
                        descripcion="🌡️ Enfriar agua + oxigenación + renovación parcial",
                        prioridad="alta",
                        tiempo_revision="12 horas"
                    )
                ]
                parametros_criticos = ["temperatura_solucion"]
            else:
                acciones = [
                    Accion(
                        tipo="oxigenacion",
                        descripcion="Verificar y mejorar oxigenación",
                        prioridad="alta",
                        tiempo_revision="inmediato"
                    )
                ]
        
        return DiagnosticoOutput(
            diagnostico=diagnostico,
            acciones=acciones,
            parametros_criticos=parametros_criticos,
            observaciones_clima_fueguino=observaciones
        )
    
    @staticmethod
    def diagnosticar_parametros(cultivo: str, etapa: str, parametros: ParametrosAmbientales) -> DiagnosticoOutput:
        """Diagnóstica basado en parámetros sin síntomas visuales"""
        rangos = DiagnosticoHidroponico.obtener_rangos_optimos(cultivo, etapa)
        acciones = []
        parametros_criticos = []
        observaciones = []
        
        # Verificar pH
        if not (rangos["ph"][0] <= parametros.ph <= rangos["ph"][1]):
            parametros_criticos.append("ph")
            if parametros.ph < rangos["ph"][0]:
                acciones.append(Accion(
                    tipo="ajuste_ph",
                    descripcion="📈 SUBIR pH - Agregar buffer alcalino hasta rango 5.8-6.2",
                    prioridad="alta",
                    tiempo_revision="2 horas"
                ))
            else:
                acciones.append(Accion(
                    tipo="ajuste_ph",
                    descripcion="📉 BAJAR pH - Agregar buffer ácido hasta rango 5.8-6.2",
                    prioridad="alta",
                    tiempo_revision="2 horas"
                ))
        
        # Verificar CE
        if not (rangos["ce"][0] <= parametros.conductividad_electrica <= rangos["ce"][1]):
            parametros_criticos.append("conductividad_electrica")
            if parametros.conductividad_electrica < rangos["ce"][0]:
                acciones.append(Accion(
                    tipo="ajuste_nutrientes",
                    descripcion=f"🔋 AUMENTAR NUTRIENTES - Incrementar concentración hasta {rangos['ce'][0]}-{rangos['ce'][1]} mS/cm",
                    prioridad="media",
                    tiempo_revision="12 horas"
                ))
            else:
                acciones.append(Accion(
                    tipo="dilucion",
                    descripcion=f"💧 DILUIR SOLUCIÓN - Agregar agua hasta {rangos['ce'][0]}-{rangos['ce'][1]} mS/cm",
                    prioridad="media",
                    tiempo_revision="6 horas"
                ))
        
        # Verificar temperatura de solución
        if not (rangos["temp_solucion"][0] <= parametros.temperatura_solucion <= rangos["temp_solucion"][1]):
            parametros_criticos.append("temperatura_solucion")
            if parametros.temperatura_solucion < rangos["temp_solucion"][0]:
                acciones.append(Accion(
                    tipo="calefaccion",
                    descripcion="🔥 CALENTAR SOLUCIÓN - Activar calefacción depósito Target: 18-22°C",
                    prioridad="alta",
                    tiempo_revision="4 horas"
                ))
                observaciones.append("❄️ Crítico en invierno fueguino")
            else:
                acciones.append(Accion(
                    tipo="enfriamiento",
                    descripcion="🧊 ENFRIAR SOLUCIÓN - Mejorar aislamiento/ventilación Target: 18-22°C",
                    prioridad="media",
                    tiempo_revision="6 horas"
                ))
        
        # Verificar humedad relativa
        if not (rangos["humedad"][0] <= parametros.humedad_relativa <= rangos["humedad"][1]):
            parametros_criticos.append("humedad_relativa")
            if parametros.humedad_relativa > rangos["humedad"][1]:
                acciones.append(Accion(
                    tipo="ventilacion",
                    descripcion="💨 MEJORAR VENTILACIÓN - Reducir HR < 75%",
                    prioridad="alta",
                    tiempo_revision="inmediato"
                ))
                observaciones.append("🌪️ Cuidado con vientos fueguinos")
            else:
                acciones.append(Accion(
                    tipo="humidificacion",
                    descripcion="💦 AUMENTAR HUMEDAD - Nebulización o riego Target: 60-75%",
                    prioridad="media",
                    tiempo_revision="6 horas"
                ))
        
        # Verificar iluminación
        if parametros.horas_luz_diarias < rangos["horas_luz"][0]:
            parametros_criticos.append("horas_luz_diarias")
            acciones.append(Accion(
                tipo="iluminacion",
                descripcion="💡 AJUSTAR ILUMINACIÓN - Extender fotoperiodo LED",
                prioridad="media",
                tiempo_revision="24 horas"
            ))
            observaciones.append("🌞 Compensar baja radiación solar")
        
        # Verificar renovación de solución
        if parametros.dias_desde_renovacion > 15:
            acciones.append(Accion(
                tipo="renovacion",
                descripcion="🔄 RENOVAR SOLUCIÓN - Cambio completo en 24h",
                prioridad="media",
                tiempo_revision="24 horas"
            ))
        
        # Si no hay problemas
        if not acciones:
            diagnostico = "✅ SISTEMA ÓPTIMO"
            acciones.append(Accion(
                tipo="monitoreo",
                descripcion="Continuar monitoreo diario y registrar parámetros",
                prioridad="baja",
                tiempo_revision="24 horas"
            ))
        else:
            diagnostico = f"Se detectaron {len(parametros_criticos)} parámetros fuera de rango"
        
        return DiagnosticoOutput(
            diagnostico=diagnostico,
            acciones=acciones,
            parametros_criticos=parametros_criticos,
            observaciones_clima_fueguino=observaciones
        )

# Endpoints de la API
@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "mensaje": "🌱 Sistema de Diagnóstico Hidropónico - Tierra del Fuego",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.post("/diagnostico", response_model=DiagnosticoOutput)
async def realizar_diagnostico(entrada: DiagnosticoInput):
    """
    Realiza un diagnóstico completo del sistema hidropónico
    basado en el árbol de decisión específico para Tierra del Fuego
    """
    try:
        # Si hay síntomas visuales, priorizarlos
        if entrada.sintomas_visuales and entrada.tipo_sintoma:
            resultado = DiagnosticoHidroponico.diagnosticar_sintomas(
                entrada.tipo_sintoma.value, 
                entrada.parametros
            )
        else:
            # Diagnóstico basado en parámetros
            resultado = DiagnosticoHidroponico.diagnosticar_parametros(
                entrada.cultivo.value,
                entrada.etapa.value,
                entrada.parametros
            )
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el diagnóstico: {str(e)}")

@app.get("/cultivos")
async def obtener_cultivos():
    """Obtiene la lista de cultivos disponibles"""
    return {
        "cultivos": [cultivo.value for cultivo in CultivoEnum],
        "etapas": [etapa.value for etapa in EtapaEnum],
        "sintomas": [sintoma.value for sintoma in SintomaEnum]
    }

@app.get("/rangos-optimos/{cultivo}/{etapa}")
async def obtener_rangos_optimos(cultivo: CultivoEnum, etapa: EtapaEnum):
    """Obtiene los rangos óptimos para un cultivo y etapa específicos"""
    rangos = DiagnosticoHidroponico.obtener_rangos_optimos(cultivo.value, etapa.value)
    return {
        "cultivo": cultivo.value,
        "etapa": etapa.value,
        "rangos_optimos": rangos
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {
        "status": "healthy",
        "timestamp": "2025-06-03",
        "location": "Tierra del Fuego, Argentina"
    }

# Configuración para ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )