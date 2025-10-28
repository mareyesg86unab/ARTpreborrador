# Contenido final y optimizado para: app.py

import streamlit as st
from modules.excel_parser import procesar_excel
from modules.art_logic import ART_OPTIONS, calculate_art_evaluation, get_nivel_riesgo
from modules.report_generator import generar_informe
from datetime import datetime

st.set_page_config(page_title="Evaluación Ergonómica TMERT", page_icon="🦾", layout="wide")

st.title("🧬 Sistema de Evaluación Ergonómica TMERT")
st.markdown("Herramienta para la evaluación cuantitativa de riesgos (Método ART) a partir de la Matriz TMERT v.7.")

if 'casos_filtrados_procesados' not in st.session_state:
    st.session_state.casos_filtrados_procesados = False
if 'casos_filtrados' not in st.session_state:
    st.session_state.casos_filtrados = []

col_carga, col_casos = st.columns([1, 2])

with col_carga:
    st.header("PASO 1: Cargar Matriz TMERT")
    uploaded_file = st.file_uploader(
        "Selecciona el archivo Excel 'Herramienta_TMERT_...V.7.xlsx'",
        type=["xlsx"],
        on_change=lambda: st.session_state.clear()
    )

    if uploaded_file and not st.session_state.casos_filtrados_procesados:
        with st.spinner("Procesando Excel..."):
            st.session_state.datos_generales, st.session_state.casos_filtrados = procesar_excel(uploaded_file)
            st.session_state.casos_filtrados_procesados = True
            if not st.session_state.casos_filtrados:
                st.error("No se encontraron casos con riesgo 'Intermedio'.")
            else:
                st.success(f"Se encontraron {len(st.session_state.casos_filtrados)} casos.")

    st.header("PASO 4: Generar Informe")
    with st.expander("✍️ Datos del Evaluador", expanded=True):
        col_evaluador1, col_evaluador2 = st.columns(2)
        
        with col_evaluador1:
            st.subheader("Datos Básicos *")
            st.text_input("Número de Informe Técnico*:", key="numero_informe")
            st.text_input("Nombre Ergónomo*:", value="Mauricio Andrés Reyes González", key="nombre_ergonomo")
            st.text_input("RUT Ergónomo*:", value="16473734-9", key="rut_ergonomo")
            st.text_input("Correo Ergónomo:", value="mauricio.reyes@ejemplo.com", key="correo_ergonomo")
            st.date_input("Fecha de Visita*:", format="DD-MM-YYYY", key="fecha_visita")
        
        with col_evaluador2:
            st.subheader("Información Adicional Centro de Trabajo")
            st.selectbox("Reglamento HS:", ["SI", "NO"], key="reglamento_hs")
            st.selectbox("Depto. Preventivo:", ["SI", "NO"], key="depto_preventivo")
            st.selectbox("Rol Empresa en CT:", ["Empresa principal", "Contratista"], key="rol_empresa_en_ct")
            st.selectbox("Comité Paritario:", ["SI", "NO"], key="comite_paritario")
            st.selectbox("Experto en Prevención:", ["SI", "NO"], key="experto_en_prevencion")
            st.text_input("Horas Semanales Experto:", key="horas_semanales_experto_empresa")
            
        st.subheader("Fechas del Centro de Trabajo")
        col_fechas1, col_fechas2, col_fechas3 = st.columns(3)
        
        with col_fechas1:
            st.date_input("Fecha Inicio CT:", format="DD-MM-YYYY", key="fecha_inicio_ct", value=None)
        with col_fechas2:
            st.date_input("Fecha Término Conocido CT:", format="DD-MM-YYYY", key="fecha_termino_conocido_ct", value=None)
        with col_fechas3:
            st.date_input("Fecha Término Informe:", format="DD-MM-YYYY", key="fecha_termino_informe", value=None)
            
        st.info("* Campos obligatorios.")

    casos_seleccionados = st.session_state.get('casos_seleccionados', [])
    datos_evaluador_completos = all(st.session_state.get(k) for k in ['numero_informe', 'nombre_ergonomo', 'rut_ergonomo', 'fecha_visita'])
    
    generar_btn = st.button("🚀 Generar Informe Word", type="primary", use_container_width=True, disabled=not (casos_seleccionados and datos_evaluador_completos))

    if casos_seleccionados and not datos_evaluador_completos:
        st.error("⚠️ Completa los datos del evaluador para generar el informe.")

    if casos_seleccionados:
        with st.container(border=True):
            st.subheader("Resumen para el Informe")
            for caso in casos_seleccionados:
                res = calculate_art_evaluation(st.session_state, caso['nro'])
                max_score = max(res['puntaje_exposicion']['izq'], res['puntaje_exposicion']['der'])
                st.markdown(f"- **Caso N°{caso['nro']} ({caso['puesto']}):** Puntaje máx. **{max_score:.2f}** → Nivel de Riesgo **{get_nivel_riesgo(max_score)}**")

    if generar_btn:
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

with col_casos:
    st.header("PASO 2: Seleccionar Casos a Evaluar")
    if not st.session_state.casos_filtrados:
        st.info("Esperando la carga del archivo Excel.")
    else:
        selection_states = {}
        for caso in st.session_state.casos_filtrados:
            nro = caso['nro']
            st.markdown("---")
            c1, c2 = st.columns([0.1, 0.9])
            selection_states[nro] = c1.checkbox(f"Seleccionar caso {nro}", key=f"sel_{nro}", label_visibility="collapsed")
            c2.markdown(f"**N°{nro} | Área:** {caso['area']} | **Puesto:** {caso['puesto']}")
            c2.caption(f"**Tarea:** {caso['tarea']}")
        
        st.session_state.casos_seleccionados = [c for c in st.session_state.casos_filtrados if selection_states.get(c['nro'])]

        if st.session_state.casos_seleccionados:
            st.markdown("---")
            st.header("PASO 3: Realizar Evaluación ART")
            tabs = st.tabs([f"Evaluar N° {c['nro']}" for c in st.session_state.casos_seleccionados])
            for i, tab in enumerate(tabs):
                with tab:
                    caso = st.session_state.casos_seleccionados[i]
                    nro = caso['nro']
                    st.subheader(f"Evaluación para: {caso['puesto']} - {caso['tarea']}")
                    
                    results = calculate_art_evaluation(st.session_state, nro)

                    st.markdown("##### Resumen de Puntuación")
                    m1, m2 = st.columns(2)
                    m1.metric("Puntaje Exposición (Izquierdo)", f"{results['puntaje_exposicion']['izq']:.2f}")
                    m1.markdown(f"**Nivel de Riesgo:** {results['nivel_riesgo']['izq']}")
                    m2.metric("Puntaje Exposición (Derecho)", f"{results['puntaje_exposicion']['der']:.2f}")
                    m2.markdown(f"**Nivel de Riesgo:** {results['nivel_riesgo']['der']}")
                    st.markdown("---")

                    st.markdown("##### A. Frecuencia y Repetición")
                    opts_a1 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['a1_mov_brazo']['opciones']]
                    opts_a2 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['a2_repeticion']['opciones']]
                    a1, a2 = st.columns(2)
                    a1.selectbox("A1. Mov. brazo (Izq)", opts_a1, key=f"a1_izq_{nro}")
                    a1.selectbox("A2. Repetición (Izq)", opts_a2, key=f"a2_izq_{nro}")
                    a2.selectbox("A1. Mov. brazo (Der)", opts_a1, key=f"a1_der_{nro}")
                    a2.selectbox("A2. Repetición (Der)", opts_a2, key=f"a2_der_{nro}")
                    sub_a_izq = results['a1']['izq']['puntaje'] + results['a2']['izq']['puntaje']
                    sub_a_der = results['a1']['der']['puntaje'] + results['a2']['der']['puntaje']
                    st.info(f"Subtotal A: [ Izq: {sub_a_izq} ] / [ Der: {sub_a_der} ]")

                    st.markdown("##### B. Fuerza")
                    b1, b2 = st.columns(2)
                    b1.selectbox("Criterio (Izq)", ART_OPTIONS['b_fuerza']['opciones_fuerza'], key=f"b_fuerza_izq_{nro}")
                    b1.selectbox("Tiempo (Izq)", ART_OPTIONS['b_fuerza']['opciones_tiempo'], key=f"b_tiempo_izq_{nro}")
                    b2.selectbox("Criterio (Der)", ART_OPTIONS['b_fuerza']['opciones_fuerza'], key=f"b_fuerza_der_{nro}")
                    b2.selectbox("Tiempo (Der)", ART_OPTIONS['b_fuerza']['opciones_tiempo'], key=f"b_tiempo_der_{nro}")
                    st.info(f"Subtotal B: [ Izq: {results['b']['izq']['puntaje']} ] / [ Der: {results['b']['der']['puntaje']} ]")

                    st.markdown("##### C. Posturas Inadecuadas")
                    opts_c1 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c1_cabeza_cuello']['opciones']]
                    opts_c2 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c2_espalda']['opciones']]
                    st.selectbox("C1. Cabeza y cuello", opts_c1, key=f"c1_{nro}")
                    st.selectbox("C2. Espalda", opts_c2, key=f"c2_{nro}")
                    st.markdown("---")
                    opts_c3 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c3_brazos']['opciones']]
                    opts_c4 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c4_munecas']['opciones']]
                    opts_c5 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['c5_agarre']['opciones']]
                    c_col1, c_col2 = st.columns(2)
                    c_col1.selectbox("C3. Brazos (Izq)", opts_c3, key=f"c3_izq_{nro}")
                    c_col1.selectbox("C4. Muñecas (Izq)", opts_c4, key=f"c4_izq_{nro}")
                    c_col1.selectbox("C5. Agarre (Izq)", opts_c5, key=f"c5_izq_{nro}")
                    c_col2.selectbox("C3. Brazos (Der)", opts_c3, key=f"c3_der_{nro}")
                    c_col2.selectbox("C4. Muñecas (Der)", opts_c4, key=f"c4_der_{nro}")
                    c_col2.selectbox("C5. Agarre (Der)", opts_c5, key=f"c5_der_{nro}")
                    sub_c_izq = results['c1']['puntaje'] + results['c2']['puntaje'] + results['c3']['izq']['puntaje'] + results['c4']['izq']['puntaje'] + results['c5']['izq']['puntaje']
                    sub_c_der = results['c1']['puntaje'] + results['c2']['puntaje'] + results['c3']['der']['puntaje'] + results['c4']['der']['puntaje'] + results['c5']['der']['puntaje']
                    st.info(f"Subtotal C: [ Izq: {sub_c_izq} ] / [ Der: {sub_c_der} ]")

                    st.markdown("##### D. Factores Adicionales")
                    opts_d1 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['d1_pausas']['opciones']]
                    opts_d2 = [f"{o['label']} (+{o['puntaje']})" for o in ART_OPTIONS['d2_ritmo']['opciones']]
                    opts_d4 = [f"{o['label']} (x{o['multiplicador']:.2f})" for o in ART_OPTIONS['d4_duracion']['opciones']]
                    st.selectbox("D1. Pausas", opts_d1, key=f"d1_{nro}")
                    st.selectbox("D2. Ritmo", opts_d2, key=f"d2_{nro}")
                    st.multiselect("D3. Otros factores (Izq)", ART_OPTIONS['d3_otros']['opciones'], key=f"d3_izq_{nro}")
                    st.multiselect("D3. Otros factores (Der)", ART_OPTIONS['d3_otros']['opciones'], key=f"d3_der_{nro}")
                    st.selectbox("D4. Duración", opts_d4, key=f"d4_duracion_{nro}")
                    st.multiselect("D5. Factores Psicosociales", ART_OPTIONS['d5_psicosociales']['opciones'], key=f"d5_{nro}")

st.markdown("---")
st.caption("Desarrollado por Mauricio Andrés Reyes González - @profErgo.")