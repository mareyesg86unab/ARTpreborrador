# Contenido final y optimizado para: app.py

import streamlit as st
from modules.excel_parser import procesar_excel
from modules.art_logic import ART_OPTIONS, calculate_art_evaluation, get_nivel_riesgo
from modules.report_generator import generar_informe
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Evaluación Ergonómica TMERT", 
    page_icon="🦾", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado siguiendo ISO 9241-143 para mejorar contraste y usabilidad
st.markdown("""
<style>
    /* Mejoras de contraste y tipografía */
    .main {
        padding-top: 1rem;
    }
    
    /* Títulos más legibles */
    h1 {
        color: #1f2937 !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: #374151 !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #4b5563 !important;
        font-weight: 500 !important;
    }
    
    /* Tarjetas con mejor contraste */
    .element-container:has(.stSelectbox) {
        background: #f8fafc;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    
    /* Botones mejorados */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
    }
    
    /* Indicadores de estado */
    .status-completed {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-pending {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-error {
        background: #ef4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Campos obligatorios */
    .required-field {
        border-left: 4px solid #ef4444 !important;
    }
    
    .completed-field {
        border-left: 4px solid #10b981 !important;
    }
    
    /* Métricas mejoradas */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar personalizada */
    .progress-container {
        background: #f3f4f6;
        border-radius: 10px;
        padding: 2px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        height: 20px;
        border-radius: 8px;
        transition: width 0.3s ease;
    }
    
    /* Sidebar mejorado */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Alertas mejoradas */
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Contenedores con bordes */
    [data-testid="stContainer"] {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares para mejorar la UX
def calcular_progreso():
    """Calcula el progreso general de la evaluación"""
    pasos = {
        'archivo_cargado': bool(st.session_state.get('casos_filtrados')),
        'casos_seleccionados': bool(st.session_state.get('casos_seleccionados')),
        'evaluaciones_completadas': False,
        'datos_evaluador': False,
        'informe_generado': False
    }
    
    # Verificar evaluaciones completadas
    if st.session_state.get('casos_seleccionados'):
        total_casos = len(st.session_state.casos_seleccionados)
        casos_evaluados = 0
        for caso in st.session_state.casos_seleccionados:
            # Verificar si tiene al menos algunas evaluaciones
            nro = caso['nro']
            if any(st.session_state.get(f"{key}_{nro}") for key in ['a1_izq', 'a1_der', 'b_fuerza_izq']):
                casos_evaluados += 1
        pasos['evaluaciones_completadas'] = casos_evaluados == total_casos
    
    # Verificar datos del evaluador
    campos_evaluador = ['numero_informe', 'nombre_ergonomo', 'rut_ergonomo', 'fecha_visita']
    pasos['datos_evaluador'] = all(st.session_state.get(k) for k in campos_evaluador)
    
    completados = sum(pasos.values())
    total = len(pasos)
    porcentaje = completados / total
    
    return pasos, completados, total, porcentaje

def mostrar_sidebar_progreso():
    """Muestra la barra de progreso y estado en el sidebar"""
    st.sidebar.markdown("## 📊 Progreso de Evaluación")
    
    pasos, completados, total, porcentaje = calcular_progreso()
    
    # Barra de progreso visual
    st.sidebar.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {porcentaje*100}%"></div>
    </div>
    <p style="text-align: center; margin: 0.5rem 0; font-weight: 600;">
        {completados}/{total} pasos completados ({porcentaje*100:.0f}%)
    </p>
    """, unsafe_allow_html=True)
    
    # Lista de pasos con estados
    st.sidebar.markdown("### Estado de Pasos:")
    
    iconos_estado = {"True": "✅", "False": "⏳"}
    nombres_pasos = {
        'archivo_cargado': '1. Cargar Matriz TMERT',
        'casos_seleccionados': '2. Seleccionar Casos',
        'evaluaciones_completadas': '3. Completar Evaluaciones',
        'datos_evaluador': '4. Datos del Evaluador',
        'informe_generado': '5. Generar Informe'
    }
    
    for key, completado in pasos.items():
        icono = iconos_estado[str(completado)]
        nombre = nombres_pasos[key]
        color = "#10b981" if completado else "#6b7280"
        st.sidebar.markdown(f"""
        <div style="padding: 0.25rem 0; color: {color};">
            {icono} {nombre}
        </div>
        """, unsafe_allow_html=True)
    
    # Información adicional
    if st.session_state.get('casos_filtrados'):
        total_casos = len(st.session_state.casos_filtrados)
        casos_seleccionados = len(st.session_state.get('casos_seleccionados', []))
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 Resumen:")
        st.sidebar.metric("Casos encontrados", total_casos)
        st.sidebar.metric("Casos seleccionados", casos_seleccionados, 
                         delta=f"+{casos_seleccionados}" if casos_seleccionados > 0 else None)

def crear_grafico_riesgo(puntaje_izq, puntaje_der, titulo="Nivel de Riesgo"):
    """Crea un gráfico de gauge para mostrar el nivel de riesgo"""
    puntaje_max = max(puntaje_izq, puntaje_der)
    
    # Determinar color basado en el riesgo
    if puntaje_max <= 11:
        color = "#10b981"  # Verde
        nivel = "BAJO"
    elif puntaje_max <= 21:
        color = "#f59e0b"  # Amarillo
        nivel = "MEDIO"
    else:
        color = "#ef4444"  # Rojo
        nivel = "ALTO"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = puntaje_max,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{titulo}<br><span style='font-size:0.8em;color:{color}'>{nivel}</span>"},
        delta = {'reference': 11, 'increasing': {'color': color}},
        gauge = {
            'axis': {'range': [None, 30]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 11], 'color': "#dcfce7"},
                {'range': [11, 21], 'color': "#fef3c7"},
                {'range': [21, 30], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 21
            }
        }
    ))
    
    fig.update_layout(height=250, font={'color': "#374151", 'family': "Arial"})
    return fig

# Inicializar variables de sesión
if 'casos_filtrados_procesados' not in st.session_state:
    st.session_state.casos_filtrados_procesados = False
if 'casos_filtrados' not in st.session_state:
    st.session_state.casos_filtrados = []

# Mostrar sidebar con progreso
mostrar_sidebar_progreso()

# Mostrar sidebar con progreso
mostrar_sidebar_progreso()

# Título principal con mejor diseño
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="margin: 0; border: none; padding: 0;">🧬 Sistema de Evaluación Ergonómica TMERT</h1>
    <p style="margin: 0.5rem 0 0 0; color: #6b7280; font-size: 1.1rem;">
        Herramienta para la evaluación cuantitativa de riesgos (Método ART) a partir de la Matriz TMERT v.7
    </p>
</div>
""", unsafe_allow_html=True)

# Layout principal mejorado
col_principal, col_lateral = st.columns([2, 1])

with col_lateral:
    # Tarjeta de carga de archivo
    with st.container():
        st.markdown("### 📁 PASO 1: Cargar Matriz TMERT")
        uploaded_file = st.file_uploader(
            "Selecciona el archivo Excel",
            type=["xlsx"],
            help="Archivo: 'Herramienta_TMERT_...V.7.xlsx'",
            on_change=lambda: st.session_state.clear()
        )

        if uploaded_file and not st.session_state.casos_filtrados_procesados:
            with st.spinner("🔄 Procesando Excel..."):
                st.session_state.datos_generales, st.session_state.casos_filtrados = procesar_excel(uploaded_file)
                st.session_state.casos_filtrados_procesados = True
                if not st.session_state.casos_filtrados:
                    st.markdown('<div class="status-error">❌ No se encontraron casos con riesgo "Intermedio"</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="status-completed">✅ {len(st.session_state.casos_filtrados)} casos encontrados</div>', 
                               unsafe_allow_html=True)

    # Tarjeta de datos del evaluador
    if st.session_state.get('casos_seleccionados'):
        with st.container():
            st.markdown("### 👤 PASO 4: Datos del Evaluador")
            
            # Indicador de campos obligatorios
            campos_evaluador = ['numero_informe', 'nombre_ergonomo', 'rut_ergonomo', 'fecha_visita']
            campos_completos = all(st.session_state.get(k) for k in campos_evaluador)
            
            if campos_completos:
                st.markdown('<div class="status-completed">✅ Datos completos</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-pending">⏳ Completar datos obligatorios</div>', unsafe_allow_html=True)
            
            with st.expander("✍️ Completar Información", expanded=not campos_completos):
                col_eval1, col_eval2 = st.columns(2)
                
                with col_eval1:
                    st.markdown("**Datos Básicos** ⚠️")
                    st.text_input("Nº Informe Técnico*:", 
                                 key="numero_informe",
                                 help="Número único del informe técnico")
                    st.text_input("Nombre Ergónomo*:", 
                                 value="Mauricio Andrés Reyes González", 
                                 key="nombre_ergonomo")
                    st.text_input("RUT Ergónomo*:", 
                                 value="16473734-9", 
                                 key="rut_ergonomo")
                    st.text_input("Correo Ergónomo:", 
                                 value="mauricio.reyes@ejemplo.com", 
                                 key="correo_ergonomo")
                    st.date_input("Fecha de Visita*:", 
                                 format="DD-MM-YYYY", 
                                 key="fecha_visita",
                                 help="Fecha en que se realizó la evaluación en terreno")
                
                with col_eval2:
                    st.markdown("**Información del Centro de Trabajo**")
                    st.selectbox("Reglamento HS:", ["SI", "NO"], key="reglamento_hs")
                    st.selectbox("Depto. Preventivo:", ["SI", "NO"], key="depto_preventivo")
                    st.selectbox("Rol Empresa en CT:", ["Empresa principal", "Contratista"], key="rol_empresa_en_ct")
                    st.selectbox("Comité Paritario:", ["SI", "NO"], key="comite_paritario")
                    st.selectbox("Experto en Prevención:", ["SI", "NO"], key="experto_en_prevencion")
                    st.text_input("Horas Semanales Experto:", key="horas_semanales_experto_empresa")
                    
                st.markdown("**Fechas del Centro de Trabajo**")
                col_fechas1, col_fechas2, col_fechas3 = st.columns(3)
                
                with col_fechas1:
                    st.date_input("Fecha Inicio CT:", format="DD-MM-YYYY", key="fecha_inicio_ct", value=None)
                with col_fechas2:
                    st.date_input("Fecha Término Conocido CT:", format="DD-MM-YYYY", key="fecha_termino_conocido_ct", value=None)
                with col_fechas3:
                    st.date_input("Fecha Término Informe:", format="DD-MM-YYYY", key="fecha_termino_informe", value=None)
                    
                st.info("⚠️ Los campos marcados con * son obligatorios para generar el informe.")

        # Botón de generación de informe mejorado
        casos_seleccionados = st.session_state.get('casos_seleccionados', [])
        
        if casos_seleccionados:
            with st.container():
                st.markdown("### 🚀 PASO 5: Generar Informe")
                
                # Resumen pre-informe
                with st.expander("📋 Resumen para el Informe", expanded=True):
                    for caso in casos_seleccionados:
                        res = calculate_art_evaluation(st.session_state, caso['nro'])
                        max_score = max(res['puntaje_exposicion']['izq'], res['puntaje_exposicion']['der'])
                        nivel = get_nivel_riesgo(max_score)
                        
                        # Color del nivel
                        color = "#10b981" if nivel == "Bajo" else "#f59e0b" if nivel == "Medio" else "#ef4444"
                        
                        st.markdown(f"""
                        <div style="padding: 0.5rem; margin: 0.25rem 0; border-left: 4px solid {color}; background: #f9fafb;">
                            <strong>Caso N°{caso['nro']} ({caso['puesto']})</strong><br>
                            Puntaje máx: <strong>{max_score:.2f}</strong> → 
                            <span style="color: {color}; font-weight: bold;">{nivel}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                generar_btn = st.button(
                    "🚀 Generar Informe Word", 
                    type="primary", 
                    use_container_width=True, 
                    disabled=not (casos_seleccionados and campos_completos),
                    help="Genera el informe técnico completo en formato Word"
                )

                if casos_seleccionados and not campos_completos:
                    st.error("⚠️ Completa todos los datos obligatorios del evaluador para generar el informe.")

with col_principal:
        with st.spinner("Generando informe..."):
            # Calcular evaluaciones ART con datos extendidos
            casos_evaluados = []
            for c in casos_seleccionados:
                art_eval = calculate_art_evaluation(st.session_state, c['nro'])
                # Importar la función para calcular máximos
                from modules.art_logic import calcular_maximos_caso
                maximos = calcular_maximos_caso(art_eval)
                
                # Combinar todos los datos del caso
                caso_completo = {
                    **c,  # Datos del caso original
                    'art': art_eval,  # Evaluación ART completa
                    **maximos  # Agregar campos máximos calculados
                }
                casos_evaluados.append(caso_completo)
            
            # Agrupar casos por nivel de riesgo para las conclusiones
            casos_por_riesgo = {
                'alto': [],
                'medio': [],
                'bajo': []
            }
            
            for caso in casos_evaluados:
                nivel = caso['nivel_riesgo_maximo'].lower()
                if nivel == 'alto':
                    casos_por_riesgo['alto'].append(caso)
                elif nivel == 'medio':
                    casos_por_riesgo['medio'].append(caso)
                else:
                    casos_por_riesgo['bajo'].append(caso)
            
            # Crear textos dinámicos para conclusiones con numeración consecutiva
            secciones_conclusiones = []
            
            # Ordenar por prioridad: Alto -> Medio -> Bajo
            if len(casos_por_riesgo['alto']) > 0:
                secciones_conclusiones.append({
                    'numero': len(secciones_conclusiones) + 1,
                    'nivel': 'alto',
                    'nivel_accion': '4',
                    'casos': casos_por_riesgo['alto'],
                    'texto': 'riesgo alto (nivel de acción 4), es indispensable intervenir la situación de trabajo enfatizando y priorizando la disminución de la exposición laboral a aquellos factores que poseen una mayor valoración según la aplicación del método de evaluación.'
                })
            
            if len(casos_por_riesgo['medio']) > 0:
                secciones_conclusiones.append({
                    'numero': len(secciones_conclusiones) + 1,
                    'nivel': 'medio',
                    'nivel_accion': '3',
                    'casos': casos_por_riesgo['medio'],
                    'texto': 'riesgo medio (nivel de acción 3), es indispensable intervenir la situación de trabajo enfatizando y priorizando la disminución de la exposición laboral a aquellos factores que poseen una mayor valoración según la aplicación del método de evaluación.'
                })
            
            if len(casos_por_riesgo['bajo']) > 0:
                secciones_conclusiones.append({
                    'numero': len(secciones_conclusiones) + 1,
                    'nivel': 'bajo',
                    'nivel_accion': '0, 1 y 2',
                    'casos': casos_por_riesgo['bajo'],
                    'texto': 'riesgo bajo (nivel de acción 0, 1 y 2), entonces corresponde realizar una revisión periódica de la tarea cada 3 años.'
                })
            
            conclusiones = {
                'tiene_riesgo_alto': len(casos_por_riesgo['alto']) > 0,
                'tiene_riesgo_medio': len(casos_por_riesgo['medio']) > 0,
                'tiene_riesgo_bajo': len(casos_por_riesgo['bajo']) > 0,
                'casos_riesgo_alto': casos_por_riesgo['alto'],
                'casos_riesgo_medio': casos_por_riesgo['medio'],
                'casos_riesgo_bajo': casos_por_riesgo['bajo'],
                'secciones': secciones_conclusiones
            }
            
            contexto = {
                # Variables nivel raíz (según plantilla)
                'numero_informe_tecnico': st.session_state.numero_informe,
                'nombre_ergonomo': st.session_state.nombre_ergonomo,
                'rut_ergonomo': st.session_state.rut_ergonomo,
                'correo_ergonomo': st.session_state.get('correo_ergonomo', 'mauricio.reyes@ejemplo.com'),
                'fecha_actual_reporte': datetime.now().strftime("%d-%m-%Y"),
                'fecha_visita_empresa': st.session_state.fecha_visita.strftime("%d-%m-%Y"),
                
                # Variables adicionales del centro de trabajo
                'reglamento_hs': st.session_state.get('reglamento_hs', 'NO'),
                'depto_preventivo': st.session_state.get('depto_preventivo', 'NO'),
                'rol_empresa_en_ct': st.session_state.get('rol_empresa_en_ct', 'Empresa principal'),
                'comite_paritario': st.session_state.get('comite_paritario', 'NO'),
                'experto_en_prevencion': st.session_state.get('experto_en_prevencion', 'NO'),
                'horas_semanales_experto_empresa': st.session_state.get('horas_semanales_experto_empresa', ''),
                'fecha_inicio_ct': st.session_state.get('fecha_inicio_ct').strftime("%d-%m-%Y") if st.session_state.get('fecha_inicio_ct') else '',
                'fecha_termino_conocido_ct': st.session_state.get('fecha_termino_conocido_ct').strftime("%d-%m-%Y") if st.session_state.get('fecha_termino_conocido_ct') else '',
                'fecha_termino_informe': st.session_state.get('fecha_termino_informe').strftime("%d-%m-%Y") if st.session_state.get('fecha_termino_informe') else '',
                
                # Información general (estructura anidada)
                'informacion_general': {
                    'antecedentes_empresa': st.session_state.datos_generales.get('antecedentes_empresa', {}),
                    'centro_trabajo': st.session_state.datos_generales.get('centro_trabajo', {}),
                    'responsable_protocolo': st.session_state.datos_generales.get('responsable_protocolo', {})
                },
                
                # Casos evaluados (nombre que espera la plantilla)
                'puestos_trabajo_detalle': casos_evaluados,
                'casos_evaluados': casos_evaluados,  # Mantener ambos por compatibilidad
                
                # Datos para conclusiones dinámicas
                'conclusiones': conclusiones
            }
            informe_bytes = generar_informe(contexto)
            if informe_bytes:
                st.success("¡Informe generado!")
                fname = f"Informe_ART_{st.session_state.numero_informe}_{datetime.now().strftime('%Y%m%d')}.docx"
                st.download_button("📥 Descargar Informe", informe_bytes, fname, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            else:
                st.error("Error al generar. Revisa la plantilla en la carpeta 'templates'.")

with col_principal:
    # Sección de selección de casos mejorada
    with st.container():
        st.markdown("### 📋 PASO 2: Seleccionar Casos a Evaluar")
        
        if not st.session_state.casos_filtrados:
            st.info("🔍 **Esperando la carga del archivo Excel**\n\nUna vez cargado el archivo, aquí aparecerán los casos con riesgo 'Intermedio' para su evaluación.")
        else:
            # Métricas de casos
            col_met1, col_met2, col_met3 = st.columns(3)
            total_casos = len(st.session_state.casos_filtrados)
            casos_seleccionados_count = len(st.session_state.get('casos_seleccionados', []))
            
            col_met1.metric("📊 Casos Encontrados", total_casos)
            col_met2.metric("✅ Casos Seleccionados", casos_seleccionados_count)
            col_met3.metric("⏳ Pendientes", total_casos - casos_seleccionados_count)
            
            st.markdown("---")
            
            # Lista de casos con mejor diseño
            selection_states = {}
            for i, caso in enumerate(st.session_state.casos_filtrados):
                nro = caso['nro']
                
                # Contenedor para cada caso
                caso_container = st.container()
                with caso_container:
                    col_check, col_info, col_preview = st.columns([0.1, 0.7, 0.2])
                    
                    with col_check:
                        selection_states[nro] = st.checkbox(
                            f"Caso {nro}", 
                            key=f"sel_{nro}", 
                            label_visibility="collapsed"
                        )
                    
                    with col_info:
                        # Información del caso con mejor formato
                        st.markdown(f"""
                        **Caso N°{nro}** | 🏢 **Área:** {caso['area']} | 👤 **Puesto:** {caso['puesto']}
                        
                        📋 **Tarea:** {caso['tarea']}
                        """)
                    
                    with col_preview:
                        if selection_states[nro]:
                            st.markdown('<div class="status-completed">✅ Seleccionado</div>', 
                                       unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="color: #6b7280;">⚪ No seleccionado</div>', 
                                       unsafe_allow_html=True)
                
                # Separador visual
                if i < len(st.session_state.casos_filtrados) - 1:
                    st.markdown("---")
            
            # Actualizar casos seleccionados
            st.session_state.casos_seleccionados = [
                c for c in st.session_state.casos_filtrados 
                if selection_states.get(c['nro'])
            ]

    # Sección de evaluación ART mejorada
    if st.session_state.get('casos_seleccionados'):
        st.markdown("---")
        with st.container():
            st.markdown("### 🔬 PASO 3: Realizar Evaluación ART")
            
            # Dashboard de evaluaciones
            casos_sel = st.session_state.casos_seleccionados
            
            # Métricas de evaluación
            col_eval_met1, col_eval_met2, col_eval_met3 = st.columns(3)
            
            total_evaluaciones = len(casos_sel)
            evaluaciones_iniciadas = 0
            evaluaciones_completas = 0
            
            for caso in casos_sel:
                nro = caso['nro']
                # Verificar si tiene alguna evaluación iniciada
                if any(st.session_state.get(f"{key}_{nro}") for key in ['a1_izq', 'a1_der', 'b_fuerza_izq']):
                    evaluaciones_iniciadas += 1
                    # Verificar si está completa (ejemplo simplificado)
                    if all(st.session_state.get(f"{key}_{nro}") for key in ['a1_izq', 'a1_der', 'c1']):
                        evaluaciones_completas += 1
            
            col_eval_met1.metric("📝 Total Evaluaciones", total_evaluaciones)
            col_eval_met2.metric("🟡 Iniciadas", evaluaciones_iniciadas)
            col_eval_met3.metric("🟢 Completas", evaluaciones_completas)
            
            # Tabs para cada evaluación
            tabs = st.tabs([f"🔬 Evaluar Caso N°{c['nro']}" for c in casos_sel])
            
            for i, tab in enumerate(tabs):
                with tab:
                    caso = casos_sel[i]
                    nro = caso['nro']
                    
                    # Encabezado del caso con información
                    st.markdown(f"""
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;">
                        <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">📋 Evaluación: {caso['puesto']}</h4>
                        <p style="margin: 0; color: #6b7280;"><strong>Tarea:</strong> {caso['tarea']}</p>
                        <p style="margin: 0; color: #6b7280;"><strong>Área:</strong> {caso['area']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Calcular y mostrar resultados
                    results = calculate_art_evaluation(st.session_state, nro)
                    
                    # Dashboard de resultados con gráficos
                    col_grafico, col_metricas = st.columns([1, 1])
                    
                    with col_grafico:
                        fig = crear_grafico_riesgo(
                            results['puntaje_exposicion']['izq'],
                            results['puntaje_exposicion']['der'],
                            f"Riesgo Caso N°{nro}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col_metricas:
                        st.markdown("#### 📊 Resultados por Lado")
                        
                        # Métricas lado izquierdo
                        col_izq, col_der = st.columns(2)
                        
                        with col_izq:
                            st.markdown("**🤚 Lado Izquierdo**")
                            puntaje_izq = results['puntaje_exposicion']['izq']
                            nivel_izq = results['nivel_riesgo']['izq']
                            color_izq = "#10b981" if nivel_izq == "Bajo" else "#f59e0b" if nivel_izq == "Medio" else "#ef4444"
                            
                            st.metric("Puntaje Exposición", f"{puntaje_izq:.2f}")
                            st.markdown(f'<div style="color: {color_izq}; font-weight: bold;">🎯 Riesgo: {nivel_izq}</div>', 
                                       unsafe_allow_html=True)
                        
                        with col_der:
                            st.markdown("**🤚 Lado Derecho**")
                            puntaje_der = results['puntaje_exposicion']['der']
                            nivel_der = results['nivel_riesgo']['der']
                            color_der = "#10b981" if nivel_der == "Bajo" else "#f59e0b" if nivel_der == "Medio" else "#ef4444"
                            
                            st.metric("Puntaje Exposición", f"{puntaje_der:.2f}")
                            st.markdown(f'<div style="color: {color_der}; font-weight: bold;">🎯 Riesgo: {nivel_der}</div>', 
                                       unsafe_allow_html=True)
                    
                    st.markdown("---")

                    # Formularios de evaluación organizados en expandibles
                    with st.expander("🔄 A. Frecuencia y Repetición", expanded=False):
                        st.markdown("##### Movimiento de Brazo y Repetición")
                        opts_a1 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['a1_mov_brazo']['opciones']]
                        opts_a2 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['a2_repeticion']['opciones']]
                        
                        col_a1, col_a2 = st.columns(2)
                        with col_a1:
                            st.selectbox(
                                "A1. Movimiento de brazo (Izquierdo)", 
                                opts_a1, 
                                key=f"a1_izq_{nro}",
                                help="Evalúa la frecuencia de movimiento del brazo izquierdo"
                            )
                            st.selectbox(
                                "A2. Repetición (Izquierdo)", 
                                opts_a2, 
                                key=f"a2_izq_{nro}",
                                help="Frecuencia de repetición de patrones de movimiento"
                            )
                        with col_a2:
                            st.selectbox(
                                "A1. Movimiento de brazo (Derecho)", 
                                opts_a1, 
                                key=f"a1_der_{nro}",
                                help="Evalúa la frecuencia de movimiento del brazo derecho"
                            )
                            st.selectbox(
                                "A2. Repetición (Derecho)", 
                                opts_a2, 
                                key=f"a2_der_{nro}",
                                help="Frecuencia de repetición de patrones de movimiento"
                            )
                        
                        # Subtotal visual
                        sub_a_izq = results['a1']['izq']['puntaje'] + results['a2']['izq']['puntaje']
                        sub_a_der = results['a1']['der']['puntaje'] + results['a2']['der']['puntaje']
                        
                        col_sub1, col_sub2 = st.columns(2)
                        col_sub1.metric("Subtotal A (Izq)", sub_a_izq)
                        col_sub2.metric("Subtotal A (Der)", sub_a_der)

                    with st.expander("💪 B. Fuerza", expanded=False):
                        st.markdown("##### Evaluación de Fuerza Aplicada")
                        
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            st.markdown("**🤚 Lado Izquierdo**")
                            st.selectbox(
                                "Criterio de Fuerza", 
                                ART_OPTIONS['b_fuerza']['opciones_fuerza'], 
                                key=f"b_fuerza_izq_{nro}",
                                help="Intensidad de la fuerza ejercida"
                            )
                            st.selectbox(
                                "Tiempo de Aplicación", 
                                ART_OPTIONS['b_fuerza']['opciones_tiempo'], 
                                key=f"b_tiempo_izq_{nro}",
                                help="Duración de aplicación de la fuerza"
                            )
                        with col_b2:
                            st.markdown("**🤚 Lado Derecho**")
                            st.selectbox(
                                "Criterio de Fuerza", 
                                ART_OPTIONS['b_fuerza']['opciones_fuerza'], 
                                key=f"b_fuerza_der_{nro}",
                                help="Intensidad de la fuerza ejercida"
                            )
                            st.selectbox(
                                "Tiempo de Aplicación", 
                                ART_OPTIONS['b_fuerza']['opciones_tiempo'], 
                                key=f"b_tiempo_der_{nro}",
                                help="Duración de aplicación de la fuerza"
                            )
                        
                        # Subtotal visual
                        col_sub1, col_sub2 = st.columns(2)
                        col_sub1.metric("Subtotal B (Izq)", results['b']['izq']['puntaje'])
                        col_sub2.metric("Subtotal B (Der)", results['b']['der']['puntaje'])

                    with st.expander("🦴 C. Posturas Inadecuadas", expanded=False):
                        st.markdown("##### Evaluación Postural")
                        
                        # Posturas generales
                        opts_c1 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c1_cabeza_cuello']['opciones']]
                        opts_c2 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c2_espalda']['opciones']]
                        
                        col_c_gen1, col_c_gen2 = st.columns(2)
                        with col_c_gen1:
                            st.selectbox(
                                "C1. Cabeza y cuello", 
                                opts_c1, 
                                key=f"c1_{nro}",
                                help="Posición de cabeza y cuello durante la tarea"
                            )
                        with col_c_gen2:
                            st.selectbox(
                                "C2. Espalda", 
                                opts_c2, 
                                key=f"c2_{nro}",
                                help="Posición de la espalda durante la tarea"
                            )
                        
                        st.markdown("---")
                        
                        # Posturas específicas por lado
                        opts_c3 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c3_brazos']['opciones']]
                        opts_c4 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c4_munecas']['opciones']]
                        opts_c5 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c5_agarre']['opciones']]
                        
                        col_c_izq, col_c_der = st.columns(2)
                        with col_c_izq:
                            st.markdown("**🤚 Lado Izquierdo**")
                            st.selectbox("C3. Brazos", opts_c3, key=f"c3_izq_{nro}", help="Posición del brazo izquierdo")
                            st.selectbox("C4. Muñecas", opts_c4, key=f"c4_izq_{nro}", help="Posición de la muñeca izquierda")
                            st.selectbox("C5. Agarre", opts_c5, key=f"c5_izq_{nro}", help="Tipo de agarre con la mano izquierda")
                        with col_c_der:
                            st.markdown("**🤚 Lado Derecho**")
                            st.selectbox("C3. Brazos", opts_c3, key=f"c3_der_{nro}", help="Posición del brazo derecho")
                            st.selectbox("C4. Muñecas", opts_c4, key=f"c4_der_{nro}", help="Posición de la muñeca derecha")
                            st.selectbox("C5. Agarre", opts_c5, key=f"c5_der_{nro}", help="Tipo de agarre con la mano derecha")
                        
                        # Subtotal visual
                        sub_c_izq = (results['c1']['puntaje'] + results['c2']['puntaje'] + 
                                    results['c3']['izq']['puntaje'] + results['c4']['izq']['puntaje'] + 
                                    results['c5']['izq']['puntaje'])
                        sub_c_der = (results['c1']['puntaje'] + results['c2']['puntaje'] + 
                                    results['c3']['der']['puntaje'] + results['c4']['der']['puntaje'] + 
                                    results['c5']['der']['puntaje'])
                        
                        col_sub1, col_sub2 = st.columns(2)
                        col_sub1.metric("Subtotal C (Izq)", sub_c_izq)
                        col_sub2.metric("Subtotal C (Der)", sub_c_der)

                    with st.expander("⚙️ D. Factores Adicionales", expanded=False):
                        st.markdown("##### Factores Complementarios")
                        
                        opts_d1 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['d1_pausas']['opciones']]
                        opts_d2 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['d2_ritmo']['opciones']]
                        opts_d4 = [f"{o['label']} (x{o['multiplicador']:.2f})" for o in ART_OPTIONS['d4_duracion']['opciones']]
                        
                        col_d1, col_d2 = st.columns(2)
                        with col_d1:
                            st.selectbox(
                                "D1. Pausas", 
                                opts_d1, 
                                key=f"d1_{nro}",
                                help="Frecuencia y duración de las pausas"
                            )
                            st.selectbox(
                                "D2. Ritmo de trabajo", 
                                opts_d2, 
                                key=f"d2_{nro}",
                                help="Presión temporal en el trabajo"
                            )
                        with col_d2:
                            st.selectbox(
                                "D4. Duración de la tarea", 
                                opts_d4, 
                                key=f"d4_duracion_{nro}",
                                help="Tiempo total dedicado a la tarea"
                            )
                        
                        st.markdown("**D3. Otros factores de riesgo**")
                        col_d3_izq, col_d3_der = st.columns(2)
                        with col_d3_izq:
                            st.multiselect(
                                "Factores adicionales (Izquierdo)", 
                                ART_OPTIONS['d3_otros']['opciones'], 
                                key=f"d3_izq_{nro}",
                                help="Selecciona todos los factores que apliquen"
                            )
                        with col_d3_der:
                            st.multiselect(
                                "Factores adicionales (Derecho)", 
                                ART_OPTIONS['d3_otros']['opciones'], 
                                key=f"d3_der_{nro}",
                                help="Selecciona todos los factores que apliquen"
                            )
                        
                        st.markdown("**D5. Factores Psicosociales**")
                        st.multiselect(
                            "Factores psicosociales presentes", 
                            ART_OPTIONS['d5_psicosociales']['opciones'], 
                            key=f"d5_{nro}",
                            help="Factores del ambiente psicosocial que pueden influir en el riesgo"
                        )

    # Proceso de generación de informe
    casos_seleccionados = st.session_state.get('casos_seleccionados', [])
    datos_evaluador_completos = all(st.session_state.get(k) for k in ['numero_informe', 'nombre_ergonomo', 'rut_ergonomo', 'fecha_visita'])
    
    # Este botón se renderiza en la columna lateral
    generar_btn = st.button("🚀 Generar Informe Word", type="primary", use_container_width=True, disabled=not (casos_seleccionados and datos_evaluador_completos), key="generar_informe_btn") if casos_seleccionados else False

    if generar_btn: