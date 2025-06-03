# Sistema Experto para Hidroponía en Tierra del Fuego

## Objetivo
Desarrollar un Sistema Experto rule-based implementado en Python (librería experta) que asista a productores locales en la optimización y mantenimiento de cultivos hidropónicos bajo invernadero en Tierra del Fuego.

## Cultivos Soportados
- **Lechuga** (Lactuca sativa)
- **Rúcula** (Eruca vesicaria)
- **Microgreens** (diversos)
- **Aromáticas** (albahaca, perejil, etc.)

## Árbol de Decisión del Sistema Experto

```mermaid
flowchart TD
    START["🌱 INICIO: Diagnóstico Sistema Hidropónico<br/>Tierra del Fuego"]
    
    %% Entrada inicial
    START --> CULT["¿Qué cultivo estás monitoreando?"]
    CULT -->|Lechuga| STAGE_L["¿En qué etapa está la lechuga?"]
    CULT -->|Rúcula| STAGE_R["¿En qué etapa está la rúcula?"]
    CULT -->|Microgreens| STAGE_M["¿En qué etapa están los microgreens?"]
    CULT -->|Aromáticas| STAGE_A["¿En qué etapa están las aromáticas?"]
    
    %% Etapas por cultivo
    STAGE_L -->|Germinación| PARAM_LG["Evaluar parámetros para lechuga germinación"]
    STAGE_L -->|Crecimiento| PARAM_LC["Evaluar parámetros para lechuga crecimiento"]
    STAGE_L -->|Pre-cosecha| PARAM_LP["Evaluar parámetros para lechuga pre-cosecha"]
    
    STAGE_R -->|Cualquier etapa| PARAM_R["Evaluar parámetros para rúcula"]
    STAGE_M -->|Cualquier etapa| PARAM_M["Evaluar parámetros para microgreens"]
    STAGE_A -->|Cualquier etapa| PARAM_A["Evaluar parámetros para aromáticas"]
    
    %% Evaluación de parámetros críticos
    PARAM_LC --> URGENT["🚨 ¿Hay algún síntoma visual alarmante?"]
    URGENT -->|Sí| SYMPTOMS["¿Qué síntomas observas?"]
    URGENT -->|No| PH_CHECK["Verificar pH de solución nutritiva"]
    
    %% Diagnóstico por síntomas
    SYMPTOMS -->|"Manchas marrones + bordes blandos"| BOTRYTIS_CHECK["¿Humedad relativa > 75%?"]
    SYMPTOMS -->|"Hojas amarillas desde abajo"| NUTRI_DEF["Posible deficiencia nutricional"]
    SYMPTOMS -->|"Crecimiento lento + raíces marrones"| ROOT_ROT["Posible pudrición radicular"]
    
    BOTRYTIS_CHECK -->|Sí| BOTRYTIS_ACTION["🍄 BOTRYTIS DETECTADO<br/>1. Aplicar fungicida biológico<br/>2. Reducir HR < 70%<br/>3. Aumentar ventilación<br/>4. Revisar en 24h"]
    BOTRYTIS_CHECK -->|No| OTHER_DISEASE["Evaluar otras causas<br/>¿Temperatura estable?"]
    
    %% Evaluación sistemática de parámetros
    PH_CHECK --> PH_RANGE["¿pH entre 5.8-6.2?"]
    PH_RANGE -->|Sí| CE_CHECK["Verificar conductividad eléctrica"]
    PH_RANGE -->|No| PH_LOW["¿pH < 5.8?"]
    
    PH_LOW -->|Sí| PH_RAISE["📈 SUBIR pH<br/>Agregar buffer alcalino<br/>hasta rango 5.8-6.2<br/>⚠️ Revisar en 2 horas"]
    PH_LOW -->|No| PH_LOWER["📉 BAJAR pH<br/>Agregar buffer ácido<br/>hasta rango 5.8-6.2<br/>⚠️ Revisar en 2 horas"]
    
    CE_CHECK --> CE_RANGE["¿CE entre 1.4-1.8 mS/cm?"]
    CE_RANGE -->|Sí| TEMP_CHECK["Verificar temperatura solución"]
    CE_RANGE -->|No| CE_LOW["¿CE < 1.4 mS/cm?"]
    
    CE_LOW -->|Sí| CE_RAISE["🔋 AUMENTAR NUTRIENTES<br/>Incrementar concentración hasta 1.4-1.8 mS/cm<br/>⚠️ Considerar etapa de cultivo"]
    CE_LOW -->|No| CE_LOWER["💧 DILUIR SOLUCIÓN<br/>Agregar agua hasta 1.4-1.8 mS/cm<br/>⚠️ Controlar pH después"]
    
    TEMP_CHECK --> TEMP_RANGE["¿Temperatura solución 18-22°C?"]
    TEMP_RANGE -->|Sí| AMBIENT_CHECK["Verificar condiciones ambientales"]
    TEMP_RANGE -->|No| TEMP_LOW["¿Temperatura < 18°C?"]
    
    TEMP_LOW -->|Sí| TEMP_HEAT["🔥 CALENTAR SOLUCIÓN<br/>Activar calefacción depósito<br/>Target: 18-22°C<br/>❄️ Crítico en invierno fueguino"]
    TEMP_LOW -->|No| TEMP_COOL["🧊 ENFRIAR SOLUCIÓN<br/>Mejorar aislamiento/ventilación<br/>Target: 18-22°C"]
    
    AMBIENT_CHECK --> HUMIDITY_CHECK["¿Humedad relativa 60-75%?"]
    HUMIDITY_CHECK -->|Sí| LIGHT_CHECK["Verificar fotoperiodo"]
    HUMIDITY_CHECK -->|No| HUMIDITY_HIGH["¿HR > 75%?"]
    
    HUMIDITY_HIGH -->|Sí| VENTILATION["💨 MEJORAR VENTILACIÓN<br/>Reducir HR < 75%<br/>⚠️ Prevenir hongos<br/>🌪️ Cuidado con vientos fueguinos"]
    HUMIDITY_HIGH -->|No| HUMIDIFY["💦 AUMENTAR HUMEDAD<br/>Nebulización o riego<br/>Target: 60-75%"]
    
    LIGHT_CHECK --> LIGHT_OK["¿Reciben luz adecuada?<br/>(12-16h LED en invierno fueguino)"]
    LIGHT_OK -->|Sí| SCHEDULE_CHECK["Revisar programación de tareas"]
    LIGHT_OK -->|No| LIGHT_ADJUST["💡 AJUSTAR ILUMINACIÓN<br/>Extender fotoperiodo LED<br/>🌞 Compensar baja radiación solar"]
    
    SCHEDULE_CHECK --> SOLUTION_AGE["¿Cuándo renovaste la solución?"]
    SOLUTION_AGE -->|"< 15 días"| MONITORING["✅ SISTEMA ÓPTIMO<br/>Continuar monitoreo diario<br/>📊 Registrar parámetros"]
    SOLUTION_AGE -->|"> 15 días"| SOLUTION_RENEW["🔄 RENOVAR SOLUCIÓN<br/>Cambio completo en 24h<br/>🧹 Limpiar sistema"]
    
    %% Acciones específicas del clima fueguino
    NUTRI_DEF --> COLD_STRESS["¿Temperatura ambiente < 10°C?"]
    COLD_STRESS -->|Sí| COLD_ACTION["❄️ ESTRÉS POR FRÍO<br/>1. Ajustar calefacción invernadero<br/>2. Revisar aislamiento<br/>3. Aumentar nutrientes 10%"]
    COLD_STRESS -->|No| NUTRI_ACTION["🌱 AJUSTE NUTRICIONAL<br/>Revisar formulación NPK<br/>según etapa de cultivo"]
    
    ROOT_ROT --> TEMP_WATER["¿Temperatura agua > 24°C?"]
    TEMP_WATER -->|Sí| COOL_WATER["🌡️ ENFRIAR AGUA<br/>+ oxigenación<br/>+ renovación parcial"]
    TEMP_WATER -->|No| OXYGEN_CHECK["Verificar oxigenación<br/>¿Bomba funcionando?"]
    
    %% Styling
    classDef startNode fill:#4caf50,color:#fff,stroke:#2e7d32,stroke-width:3px
    classDef questionNode fill:#2196f3,color:#fff,stroke:#1565c0,stroke-width:2px
    classDef actionNode fill:#ff9800,color:#fff,stroke:#ef6c00,stroke-width:2px
    classDef criticalNode fill:#f44336,color:#fff,stroke:#c62828,stroke-width:3px
    classDef successNode fill:#8bc34a,color:#fff,stroke:#558b2f,stroke-width:2px
    
    class START startNode
    class CULT,STAGE_L,STAGE_R,STAGE_M,STAGE_A,PARAM_LC,URGENT,PH_CHECK,PH_RANGE,CE_CHECK,CE_RANGE,TEMP_CHECK,TEMP_RANGE,AMBIENT_CHECK,HUMIDITY_CHECK,LIGHT_CHECK,LIGHT_OK,SCHEDULE_CHECK,SOLUTION_AGE,PH_LOW,CE_LOW,TEMP_LOW,HUMIDITY_HIGH,BOTRYTIS_CHECK,COLD_STRESS,TEMP_WATER,OXYGEN_CHECK questionNode
    class PH_RAISE,PH_LOWER,CE_RAISE,CE_LOWER,TEMP_HEAT,TEMP_COOL,VENTILATION,HUMIDIFY,LIGHT_ADJUST,SOLUTION_RENEW,NUTRI_ACTION,COOL_WATER actionNode
    class BOTRYTIS_ACTION,COLD_ACTION criticalNode
    class MONITORING successNode
```

## Parámetros Críticos Monitoreados

| Parámetro | Rango Óptimo | Acción si fuera de rango |
|-----------|--------------|-------------------------|
| **pH** | 5.8 - 6.2 | Ajuste con buffer alcalino/ácido |
| **CE** | 1.4 - 1.8 mS/cm | Ajuste de concentración de nutrientes |
| **Temp. Solución** | 18 - 22°C | Calefacción/enfriamiento del depósito |
| **Humedad Relativa** | 60 - 75% | Ventilación/nebulización |
| **Fotoperiodo** | 12-16h (invierno) | Ajuste LED para compensar baja radiación |

## Alertas Críticas (Ventana 24-48h)

### Botrytis (Moho Gris)
- **Síntomas**: Manchas marrones + bordes blandos
- **Condición**: HR > 75%
- **Acción**: Fungicida biológico + reducir HR < 70%

### Estrés por Frío Fueguino
- **Condición**: Temperatura ambiente < 10°C
- **Acción**: Ajustar calefacción + revisar aislamiento + aumentar nutrientes 10%

## Tecnologías Utilizadas
- **Python** (Motor de inferencia)
- **Experta** (Sistema de reglas)
- **Mermaid** (Diagramas de flujo)

## Valor Agregado
- ✅ Reducción de pérdidas hasta 50%
- ✅ Optimización de recursos hídricos (< 10% vs agricultura tradicional)
- ✅ Suministro local 12 meses/año
- ✅ Reducción huella de carbono (menos importaciones)

## Contexto Tierra del Fuego
- **Clima extremo**: Invierno < 0°C, vientos fuertes
- **Baja radiación solar**: 3-4 meses cultivo exterior
- **Sistemas**: NFT/DWC predominantes
- **Especies adaptadas**: Resistentes a bajas temperaturas

## Utilización del programa

Para implementar el programa se debe en primer lugar instalar las dependencias en un entorno virtual.

``` bash
python -m venv venv

pip install -r requeriments.txt

```
Ejecutar el backend en la terminal.
``` bash
python app.py
```
Y seguidamente, en otra terminal, el frontend.

``` bash
python interface.py
```
### Despliegue

Una vez ejecutada la aplicación por terminal, se la podrá visitar en la url:

**localhost:7860**

Para los endpoints de la API:

**localhost:8000/docs**

---
*Desarrollado por Facundo Salinas - Sistema Experto para Hidroponía TdF*