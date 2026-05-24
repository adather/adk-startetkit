import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool
from google.adk.tools.skill_toolset import SkillToolset
from tavily import TavilyClient

# 1. AGENTE: Investigador Google (Usa herramientas nativas del ADK)
google_search_investigador = Agent(
    name="google_search_investigador",
    model="gemini-2.5-flash",
    description="Investiga usando Google sobre noticias de precios de semillas.",
    instruction="""Realizas una búsqueda en internet usando 'google_search' sobre noticias relacionadas al 
    precio de semillas como frijol, arroz, soja, etc.""",
    tools=[google_search]
)

# ==============================================================================================================
# 2. CONFIGURACIÓN DE TAVILY Y SU FUNCIÓN COVERTIDA A TOOL
# ==============================================================================================================
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
def tavily_search(query: str) -> str:
    """
    Úsala para buscar noticias de última hora en internet sobre precios de semillas 
    (frijol, arroz, soja, maíz, etc.). Toma como argumento una query corta de palabras clave.
    """
    try:
        response = tavily_client.search(query=query, include_answer="basic", search_depth="advanced")
        resultados = response.get("results", [])
        
        if not resultados:
            return f"No se encontraron noticias recientes en internet para la consulta: '{query}'."
            
        texto_limpio = ""
        for item in resultados:
            texto_limpio += f"Título: {item.get('title')}\n"
            texto_limpio += f"Contenido/Contexto: {item.get('content')}\n"
            texto_limpio += f"Fuente URL: {item.get('url')}\n\n"
            
        return texto_limpio
        
    except Exception as e:
        return f"Error al ejecutar la búsqueda en Tavily: {str(e)}"

# Envolvemos la función usando FunctionTool para que el ADK genere el esquema automáticamente
tavily_tool = FunctionTool(func=tavily_search)

tavily_search_investigador = Agent(
    name="tavily_search_investigador",
    model="gemini-2.5-flash",
    description="Agente especialista encargado de monitorear y recolectar precios de mercado de granos y semillas en la web vía Tavily.",
    instruction="""Eres un analista de mercado agrícola de alta precisión. 
    Tu objetivo es investigar los precios actuales de semillas como frijol, arroz, soja, etc.
    
    Reglas de operación:
    1. Transforma las solicitudes conversacionales en queries de búsqueda optimizadas para motores de búsqueda (ej: si te piden saber del frijol, busca 'precio tonelada frijol mercado internacional 2026').
    2. Ejecuta la herramienta 'tavily_search' tantas veces como sea necesario para cubrir las semillas solicitadas.
    3. Al responder, estructura la información de manera clara, citando brevemente la fuente o el link proporcionado por la herramienta. No inventes datos que no estén explícitamente en los resultados web.
    """,
    tools=[tavily_tool] 
)



# ==============================================================================================================
# 5. ORQUESTADOR CENTRAL
# ==============================================================================================================
root_agent = Agent( 
    model="gemini-2.5-flash",
    name="agente_busqueda_centralizado",
    description="Eres el agente orquestador central de búsquedas.",
    instruction=(
        "Eres un agente supervisor de búsqueda en internet.\n\n"
        "Tu trabajo es delegar la consulta al agente especialista más adecuado:\n"
        "- Usa **google_search_investigador** para búsquedas generales en Google.\n"
        "- Usa **tavily_search_investigador** para búsquedas profundas o de última hora optimizadas.\n\n"
        "Siempre respondes de manera educada, directa y consolidando los reportes de tus agentes sin inventar información."
    ),
)