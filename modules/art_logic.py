from docxtpl import RichText

# --- 1. BASE DE DATOS DE LA METODOLOGÍA ART ---
ART_OPTIONS = {
    "a1_mov_brazo": {
        "texto_justificacion": "Los movimientos de los brazos son {selection}, especialmente de {side}.",
        "opciones": [
            {"label": "Infrecuentes (Algunos movimientos intermitentes)", "puntaje": 0, "color": "V", "texto_justificacion": "infrecuentes y pausados"},
            {"label": "Frecuentes (Movimientos regulares con algunas pausas)", "puntaje": 3, "color": "A", "texto_justificacion": "constantes y fluidos"},
            {"label": "Muy Frecuentes (Movimiento casi continuo)", "puntaje": 6, "color": "R", "texto_justificacion": "muy frecuentes (casi continuos)"}
        ]
    },
    "a2_repeticion": {
        "texto_justificacion": "Se repite un patrón de movimiento similar del brazo y la mano: {selection}, especialmente de {side}.",
        "opciones": [
            {"label": "10 veces por minuto o menos", "puntaje": 0, "color": "V", "texto_justificacion": "10 veces por minuto o menos"},
            {"label": "11-20 veces por minuto", "puntaje": 3, "color": "A", "texto_justificacion": "entre 11 y 20 veces por minuto"},
            {"label": "Más de 20 veces por minuto", "puntaje": 6, "color": "R", "texto_justificacion": "más de 20 veces por minuto"}
        ]
    },
    "b_fuerza": {
        "texto_justificacion": "La fuerza ejercida con la mano es {selection_fuerza} durante {selection_tiempo}, especialmente de {side}.",
        "opciones_fuerza": ["Ligero", "Moderado", "Intenso", "Vigoroso"],
        "opciones_tiempo": ["Infrecuente", "Parte del tiempo (15-30%)", "Cerca de la mitad del tiempo (40-60%)", "Casi todo el tiempo (80% o más)"],
        "matriz_puntaje": {
            "Ligero":    {"Infrecuente": 0, "Parte del tiempo (15-30%)": 0, "Cerca de la mitad del tiempo (40-60%)": 0, "Casi todo el tiempo (80% o más)": 0},
            "Moderado":  {"Infrecuente": 1, "Parte del tiempo (15-30%)": 2, "Cerca de la mitad del tiempo (40-60%)": 4, "Casi todo el tiempo (80% o más)": 8},
            "Intenso":   {"Infrecuente": 6, "Parte del tiempo (15-30%)": 9, "Cerca de la mitad del tiempo (40-60%)": 10, "Casi todo el tiempo (80% o más)": 10},
            "Vigoroso":  {"Infrecuente": 10, "Parte del tiempo (15-30%)": 10, "Cerca de la mitad del tiempo (40-60%)": 10, "Casi todo el tiempo (80% o más)": 10}
        }
    },
    "c1_cabeza_cuello": {
        "texto_justificacion": "La cabeza o cuello está {selection}.",
        "opciones": [
            {"label": "Esta cerca de la postura neutral", "puntaje": 0, "color": "V", "texto_justificacion": "en una postura neutral"},
            {"label": "Doblada o rotada parte del tiempo (ej: 15-30%)", "puntaje": 1, "color": "A", "texto_justificacion": "doblado o rotado parte del tiempo"},
            {"label": "Doblada o rotada más de la mitad del tiempo", "puntaje": 2, "color": "R", "texto_justificacion": "doblado o rotado más de la mitad del tiempo"}
        ]
    },
    "c2_espalda": {
        "texto_justificacion": "La espalda esta {selection}.",
        "opciones": [
            {"label": "Esta cerca de la postura neutral", "puntaje": 0, "color": "V", "texto_justificacion": "en una postura neutral"},
            {"label": "Flectada, de lado o rotado parte del tiempo", "puntaje": 1, "color": "A", "texto_justificacion": "flectada hacia adelante parte del tiempo"},
            {"label": "Flectada, de lado o rotado durante más de la mitad del tiempo", "puntaje": 2, "color": "R", "texto_justificacion": "flectada hacia adelante más de la mitad del tiempo"}
        ]
    },
    "c3_brazos": {
        "texto_justificacion": "El codo está {selection}.",
        "opciones": [
            {"label": "Mantenido cerca del cuerpo o apoyado", "puntaje": 0, "color": "V", "texto_justificacion": "mantenido cerca del cuerpo"},
            {"label": "Levantado lejos del cuerpo parte del tiempo", "puntaje": 2, "color": "A", "texto_justificacion": "alejado del cuerpo parte del tiempo"},
            {"label": "Levantado lejos del cuerpo más de la mitad del tiempo", "puntaje": 4, "color": "R", "texto_justificacion": "alejado del cuerpo más de la mitad del tiempo"}
        ]
    },
    "c4_munecas": {
        "texto_justificacion": "La muñeca está {selection}, especialmente de {side}.",
        "opciones": [
            {"label": "Casi recto/en posición neutral", "puntaje": 0, "color": "V", "texto_justificacion": "en posición neutral"},
            {"label": "Flectada o desviada parte del tiempo", "puntaje": 1, "color": "A", "texto_justificacion": "en flexión, extensión o desviada parte del tiempo"},
            {"label": "Flectada o desviada más de la mitad del tiempo", "puntaje": 2, "color": "R", "texto_justificacion": "en flexión, extensión o desviada más de la mitad del tiempo"}
        ]
    },
    "c5_agarre": {
        "texto_justificacion": "Las manos o los dedos sostienen objetos con {selection}, especialmente de {side}.",
        "opciones": [
            {"label": "Agarre firme o no hay agarre incomodo", "puntaje": 0, "color": "V", "texto_justificacion": "un agarre firme y cómodo"},
            {"label": "Pinza o agarre amplio con los dedos durante parte del tiempo", "puntaje": 1, "color": "A", "texto_justificacion": "pinza o agarre amplio con los dedos durante parte del tiempo"},
            {"label": "Pinza o agarre amplio con los dedos más de la mitad del tiempo", "puntaje": 2, "color": "R", "texto_justificacion": "pinza o agarre amplio con los dedos más de la mitad del tiempo"}
        ]
    },
    "d1_pausas": {
        "texto_justificacion": "El trabajador puede realizar la tarea de forma continua sin interrupción por {selection}.",
        "opciones": [
            {"label": "Menos de una hora, o hay descansos frecuentes", "puntaje": 0, "color": "V", "texto_justificacion": "menos de una hora"},
            {"label": "1 hora a menos de 2 horas", "puntaje": 2, "color": "A", "texto_justificacion": "1, pero menos a 2 horas"},
            {"label": "2 horas a menos de 3 horas", "puntaje": 4, "color": "R", "texto_justificacion": "2, pero menos a 3 horas"},
            {"label": "3 horas a menos de 4 horas", "puntaje": 6, "color": "R", "texto_justificacion": "3, pero menos a 4 horas"},
            {"label": "4 horas o más", "puntaje": 8, "color": "R", "texto_justificacion": "4 horas o más"}
        ]
    },
    "d2_ritmo": {
        "texto_justificacion": "Al trabajador {selection} mantenerse al día con el trabajo.",
        "opciones": [
            {"label": "No es difícil mantenerse al día con el trabajo", "puntaje": 0, "color": "V", "texto_justificacion": "no le es difícil"},
            {"label": "A veces es difícil mantenerse al día con el trabajo", "puntaje": 1, "color": "A", "texto_justificacion": "a veces le es difícil"},
            {"label": "A menudo es difícil mantenerse al día con el trabajo", "puntaje": 2, "color": "R", "texto_justificacion": "a menudo le es difícil"}
        ]
    },
    "d3_otros": {
        "texto_justificacion": "Se identificaron los siguientes factores adicionales: {selection}.",
        "opciones": [
            "Los guantes afectan el agarre y dificultan la tarea de manipulación manual.",
            "Se utiliza una herramienta para golpear dos o más veces por minuto.",
            "La mano se utiliza como herramienta diez o más veces por hora.",
            "Las herramientas, la pieza o el puesto de trabajo provocan compresión de la piel.",
            "Las herramientas o piezas de trabajo causan molestias o calambres.",
            "La mano/brazo está expuesto a vibraciones.",
            "La tarea requiere movimientos finos y precisos.",
            "Los operadores están expuestos al frío o a corrientes de aire.",
            "Los niveles de iluminación son inadecuados."
        ]
    },
    "d4_duracion": {
        "texto_justificacion": "Duración de la tarea por un trabajador es: {selection}.",
        "opciones": [
            {"label": "Menos de 2 horas", "multiplicador": 0.5, "texto_justificacion": "menos de 2 horas"},
            {"label": "Entre 2 a menos de 4 horas", "multiplicador": 0.75, "texto_justificacion": "2 horas a menos de 4 horas"},
            {"label": "Entre 4 a 8 horas", "multiplicador": 1.0, "texto_justificacion": "4 a 8 horas"},
            {"label": "Más de 8 horas", "multiplicador": 1.5, "texto_justificacion": "más de 8 horas"}
        ]
    },
    "d5_psicosociales": {
        "opciones": [
            "Poco control sobre cómo el trabajo es realizado.",
            "Incentivos para saltarse los descansos o terminar temprano.",
            "Trabajo monótono.",
            "Altos niveles de atención y concentración.",
            "Plazos de entrega ajustados y frecuentes.",
            "Falta de apoyo de supervisores y/o compañeros de trabajo.",
            "Exigencias laborales excesivas y capacitación insuficiente."
        ]
    }
}

# --- 2. LÓGICA DE CÁLCULO Y FORMATO ---

COLOR_MAP = {
    "V": "A9D08E",  # Verde
    "A": "FFD966",  # Amarillo
    "R": "F4B183"   # Rojo (Naranja suave para mejor lectura)
}

def get_b_fuerza_color_char(score):
    if score == 0: return "V"
    if score in [1, 2, 4, 8]: return "A"
    return "R"
    
def get_d3_color_char(score):
    if score == 0: return "V"
    if score == 1: return "A"
    return "R"

def get_nivel_riesgo(score):
    # Aproximar al entero más cercano antes de comparar
    score = round(score)
    if score <= 11: return "Bajo"
    if score <= 21: return "Medio"
    return "Alto"

def get_nivel_accion(score):
    """Determina el nivel de acción basado en el puntaje de exposición."""
    score = round(score)
    if score <= 11: 
        return 0  # Verde - Bajo
    elif score <= 21: 
        return 1  # Amarillo - Medio
    else: 
        return 2  # Rojo - Alto

def calcular_maximos_caso(art_evaluation):
    """
    Calcula los valores máximos (nivel de acción, puntuación y nivel de riesgo) 
    para un caso específico comparando lado izquierdo y derecho.
    
    Args:
        art_evaluation (dict): Resultado de calculate_art_evaluation
        
    Returns:
        dict: Diccionario con los valores máximos
    """
    puntaje_izq = art_evaluation['puntaje_exposicion']['izq']
    puntaje_der = art_evaluation['puntaje_exposicion']['der']
    
    # Determinar valores máximos
    puntaje_maximo = max(puntaje_izq, puntaje_der)
    nivel_riesgo_maximo = get_nivel_riesgo(puntaje_maximo)
    nivel_accion_maximo = get_nivel_accion(puntaje_maximo)
    
    return {
        'nivel_accion_maximo': nivel_accion_maximo,
        'puntuacion_maxima': round(puntaje_maximo, 2),
        'nivel_riesgo_maximo': nivel_riesgo_maximo,
        'lado_critico': 'izquierdo' if puntaje_izq >= puntaje_der else 'derecho'
    }

def calculate_art_evaluation(user_selections, nro_caso):
    def find_selected_option(key, options_list):
        raw_selection = user_selections.get(f"{key}_{nro_caso}", "").split(' (')[0]
        print(f"DEBUG - Buscando clave: {key}_{nro_caso}, valor: '{raw_selection}'")
        
        # Buscar coincidencia exacta primero
        for option in options_list:
            if option['label'] == raw_selection:
                return option
        
        # Si no encuentra coincidencia exacta, buscar por coincidencia parcial
        for option in options_list:
            if raw_selection in option['label'] or option['label'].startswith(raw_selection):
                print(f"DEBUG - Encontrado por coincidencia parcial: {option['label']}")
                return option
        
        print(f"DEBUG - No encontrado, usando por defecto: {options_list[0]['label']}")
        return options_list[0]

    # 1. Procesar todas las selecciones
    a1_izq = find_selected_option("a1_izq", ART_OPTIONS['a1_mov_brazo']['opciones'])
    a1_der = find_selected_option("a1_der", ART_OPTIONS['a1_mov_brazo']['opciones'])
    a2_izq = find_selected_option("a2_izq", ART_OPTIONS['a2_repeticion']['opciones'])
    a2_der = find_selected_option("a2_der", ART_OPTIONS['a2_repeticion']['opciones'])
    c1 = find_selected_option("c1", ART_OPTIONS['c1_cabeza_cuello']['opciones'])
    c2 = find_selected_option("c2", ART_OPTIONS['c2_espalda']['opciones'])
    c3_izq = find_selected_option("c3_izq", ART_OPTIONS['c3_brazos']['opciones'])
    c3_der = find_selected_option("c3_der", ART_OPTIONS['c3_brazos']['opciones'])
    c4_izq = find_selected_option("c4_izq", ART_OPTIONS['c4_munecas']['opciones'])
    c4_der = find_selected_option("c4_der", ART_OPTIONS['c4_munecas']['opciones'])
    c5_izq = find_selected_option("c5_izq", ART_OPTIONS['c5_agarre']['opciones'])
    c5_der = find_selected_option("c5_der", ART_OPTIONS['c5_agarre']['opciones'])
    d1 = find_selected_option("d1", ART_OPTIONS['d1_pausas']['opciones'])
    d2 = find_selected_option("d2", ART_OPTIONS['d2_ritmo']['opciones'])
    d4 = find_selected_option("d4_duracion", ART_OPTIONS['d4_duracion']['opciones'])

    fuerza_sel_izq = user_selections.get(f"b_fuerza_izq_{nro_caso}", ART_OPTIONS['b_fuerza']['opciones_fuerza'][0])
    tiempo_sel_izq = user_selections.get(f"b_tiempo_izq_{nro_caso}", ART_OPTIONS['b_fuerza']['opciones_tiempo'][0])
    b_izq_score = ART_OPTIONS['b_fuerza']['matriz_puntaje'][fuerza_sel_izq][tiempo_sel_izq]
    b_izq_color = get_b_fuerza_color_char(b_izq_score)
    
    fuerza_sel_der = user_selections.get(f"b_fuerza_der_{nro_caso}", ART_OPTIONS['b_fuerza']['opciones_fuerza'][0])
    tiempo_sel_der = user_selections.get(f"b_tiempo_der_{nro_caso}", ART_OPTIONS['b_fuerza']['opciones_tiempo'][0])
    b_der_score = ART_OPTIONS['b_fuerza']['matriz_puntaje'][fuerza_sel_der][tiempo_sel_der]
    b_der_color = get_b_fuerza_color_char(b_der_score)

    d3_izq_sel = user_selections.get(f"d3_izq_{nro_caso}", [])
    d3_izq_score = 0 if not d3_izq_sel else (1 if len(d3_izq_sel) == 1 else 2)
    d3_der_sel = user_selections.get(f"d3_der_{nro_caso}", [])
    d3_der_score = 0 if not d3_der_sel else (1 if len(d3_der_sel) == 1 else 2)
    
    # 2. Calcular puntajes finales (LÓGICA DE SUMA DIRECTA)
    # DEBUG: Imprimir valores individuales para verificar
    print(f"DEBUG - Caso {nro_caso} - Valores Izq:")
    print(f"DEBUG - Buscando a1_izq_{nro_caso}: '{user_selections.get(f'a1_izq_{nro_caso}', 'NO_ENCONTRADO')}'")
    print(f"DEBUG - Buscando c1_{nro_caso}: '{user_selections.get(f'c1_{nro_caso}', 'NO_ENCONTRADO')}'")
    print(f"  A1: {a1_izq['puntaje']}, A2: {a2_izq['puntaje']}, B: {b_izq_score}")
    print(f"  C1: {c1['puntaje']}, C2: {c2['puntaje']}, C3: {c3_izq['puntaje']}, C4: {c4_izq['puntaje']}, C5: {c5_izq['puntaje']}")
    print(f"  D1: {d1['puntaje']}, D2: {d2['puntaje']}, D3: {d3_izq_score}")
    
    score_izq = (
        a1_izq['puntaje'] + a2_izq['puntaje'] + b_izq_score + 
        c1['puntaje'] + c2['puntaje'] + c3_izq['puntaje'] + c4_izq['puntaje'] + c5_izq['puntaje'] + 
        d1['puntaje'] + d2['puntaje'] + d3_izq_score
    )
    print(f"  TOTAL CALCULADO: {score_izq}")
    exposure_izq = score_izq * d4['multiplicador']

    score_der = (
        a1_der['puntaje'] + a2_der['puntaje'] + b_der_score + 
        c1['puntaje'] + c2['puntaje'] + c3_der['puntaje'] + c4_der['puntaje'] + c5_der['puntaje'] + 
        d1['puntaje'] + d2['puntaje'] + d3_der_score
    )
    exposure_der = score_der * d4['multiplicador']
    
    # 3. Preparar subtotales para la UI (LÓGICA DE SUMA DIRECTA)
    subtotal_a_izq = a1_izq['puntaje'] + a2_izq['puntaje']
    subtotal_a_der = a1_der['puntaje'] + a2_der['puntaje']
    subtotal_c_izq = c1['puntaje'] + c2['puntaje'] + c3_izq['puntaje'] + c4_izq['puntaje'] + c5_izq['puntaje']
    subtotal_c_der = c1['puntaje'] + c2['puntaje'] + c3_der['puntaje'] + c4_der['puntaje'] + c5_der['puntaje']

    # 4. Construir el diccionario final
    def build_result(option, score=None, color_char=None):
        puntaje = score if score is not None else option['puntaje']
        color = color_char if color_char is not None else option['color']
        return {'puntaje': puntaje, 'color': color, 'color_hex': COLOR_MAP.get(color, "FFFFFF")}

    results = {
        'a1': { 'izq': build_result(a1_izq), 'der': build_result(a1_der), 'texto': ART_OPTIONS['a1_mov_brazo']['texto_justificacion'].format(selection=a1_der['texto_justificacion'], side='EESS Derecha')},
        'a2': { 'izq': build_result(a2_izq), 'der': build_result(a2_der), 'texto': ART_OPTIONS['a2_repeticion']['texto_justificacion'].format(selection=a2_der['texto_justificacion'], side='EESS Derecha')},
        'b':  { 'izq': build_result(None, b_izq_score, b_izq_color), 'der': build_result(None, b_der_score, b_der_color), 'texto': ART_OPTIONS['b_fuerza']['texto_justificacion'].format(selection_fuerza=fuerza_sel_der.lower(), selection_tiempo=tiempo_sel_der.lower(), side='EESS Derecha')},
        'c1': { **build_result(c1), 'texto': ART_OPTIONS['c1_cabeza_cuello']['texto_justificacion'].format(selection=c1['texto_justificacion'])},
        'c2': { **build_result(c2), 'texto': ART_OPTIONS['c2_espalda']['texto_justificacion'].format(selection=c2['texto_justificacion'])},
        'c3': { 'izq': build_result(c3_izq), 'der': build_result(c3_der), 'texto': ART_OPTIONS['c3_brazos']['texto_justificacion'].format(selection=c3_der['texto_justificacion'])},
        'c4': { 'izq': build_result(c4_izq), 'der': build_result(c4_der), 'texto': ART_OPTIONS['c4_munecas']['texto_justificacion'].format(selection=c4_der['texto_justificacion'], side='EESS Derecha')},
        'c5': { 'izq': build_result(c5_izq), 'der': build_result(c5_der), 'texto': ART_OPTIONS['c5_agarre']['texto_justificacion'].format(selection=c5_der['texto_justificacion'], side='EESS Derecha')},
        'd1': { **build_result(d1), 'texto': ART_OPTIONS['d1_pausas']['texto_justificacion'].format(selection=d1['texto_justificacion'])},
        'd2': { **build_result(d2), 'texto': ART_OPTIONS['d2_ritmo']['texto_justificacion'].format(selection=d2['texto_justificacion'])},
        'd3': { 'izq': {**build_result(None, d3_izq_score, get_d3_color_char(d3_izq_score)), 'factores_seleccionados': d3_izq_sel}, 'der': {**build_result(None, d3_der_score, get_d3_color_char(d3_der_score)), 'factores_seleccionados': d3_der_sel}},
        'd4': { 'multiplicador': d4['multiplicador'], 'texto': ART_OPTIONS['d4_duracion']['texto_justificacion'].format(selection=d4['texto_justificacion'])},
        'd5': { 'factores_seleccionados': user_selections.get(f"d5_{nro_caso}", [])},
        'subtotales': {
            'a': {'izq': subtotal_a_izq, 'der': subtotal_a_der},
            'b': {'izq': b_izq_score, 'der': b_der_score},
            'c': {'izq': subtotal_c_izq, 'der': subtotal_c_der}
        },
        'puntaje_tarea': {'izq': score_izq, 'der': score_der},
        'puntaje_exposicion': {'izq': round(exposure_izq, 2), 'der': round(exposure_der, 2)},
        'nivel_riesgo': {'izq': get_nivel_riesgo(exposure_izq), 'der': get_nivel_riesgo(exposure_der)}
    }
    return results
