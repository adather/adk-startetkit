from google.adk.agents import Agent
from google.adk.tools import google_search

def buenos_dias(name):
    return f"Buenos dias {name}, hoy me siento fantastico"

def buenas_tardes(name):
    return f"Buenas tardes {name}, ya estoy un poco cansado"


root_agent = Agent(
    name="mi_primer_Agente",
    model="gemini-2.5-flash",
    description="Respondes preguntas generales ", #que hace este agente, es util porque en sistemas multiagente 
    # description="Respondes la pregunta usando tu conocimiento sobre el tema",
    instruction="""Respondes las preguntas usando tu conocimiento sobre el tema, primero preguntas el nombre de la persona, si el usuario
    te dice buenos dias, usas la funcion buenos_dias, si te dice buenas tardes, usas la funcion buenas_tardes""", #como lo hace
    tools=[buenos_dias, buenas_tardes]
    )