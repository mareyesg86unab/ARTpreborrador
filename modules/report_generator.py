from docxtpl import DocxTemplate
from io import BytesIO

TEMPLATE_PATH = "templates/plantilla_ART_evaluacion.docx"

def generar_informe(contexto_final):
    """
    Genera un informe Word (.docx) a partir de una plantilla y un contexto de datos.

    Args:
        contexto_final (dict): Diccionario con todos los datos para renderizar en la plantilla.

    Returns:
        BytesIO: El documento Word generado en memoria, listo para ser descargado.
                 Retorna None si la plantilla no se encuentra.
    """
    try:
        # DEBUG: Imprimir la estructura del contexto
        print("DEBUG - CONTEXTO ENVIADO A JINJA2:")
        print(f"Claves principales: {list(contexto_final.keys())}")
        if 'informe' in contexto_final:
            print(f"Claves en 'informe': {list(contexto_final['informe'].keys())}")
            if 'datos_generales' in contexto_final['informe']:
                print(f"Claves en 'datos_generales': {list(contexto_final['informe']['datos_generales'].keys())}")
        print("-----")
        
        # Cargar la plantilla desde el path especificado
        doc = DocxTemplate(TEMPLATE_PATH)
        
        # Renderizar el contexto en la plantilla
        doc.render(contexto_final)
        
        # Guardar el documento en un buffer de memoria
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0) # Mover el cursor al inicio del buffer
        
        return file_stream
        
    except FileNotFoundError:
        # Este error se puede mostrar en la UI de Streamlit
        print(f"Error: No se encontró la plantilla en la ruta: {TEMPLATE_PATH}")
        return None
    except Exception as e:
        # Captura de otros posibles errores durante la renderización
        print(f"Error inesperado al generar el informe: {e}")
        return None
