
# Starter kit del ADK para el desarrollo de agentes
**Pedro Gallegos, mayo 2026** 


El Agent Ddevelopment Kit (ADK) es un  framework desarrollado por Google para la creación, conección, desarrollo y despliege de soluciones basadas en agentes. Este framework se integra de forma sencilla con el resto de soluciones de Google (GCP, , LLMs como Gemini, etc).   

El objetivo de este manual es informar sobre los pasos necesarios para desarrollar una solución agentica.

La documentación del proyecto se encuentra disponible en [adk.dev](https://adk.dev/).

## Instalación

 Al momento de la creación del presente manual nos encontramos en la versión 1.28.x. Para instalar la libreria usando pip se ejecuta el siguiente comando:

```
pip install google-adk 
```

```

```
### Mi primer agente

En este momento y por practicidad usaremos un llm propio de Google, por lo cual es necesario obtener un "GEMINI_API_KEY" que se almacena en el archivo .env

Para obtene reste string es mediante la creación de una cuenta en [GCP](https://console.cloud.google.com/) y mediante una cuenta de facturación, se crea el proyecto y se le asignan los recursos necesarios. A continuación se anexan algunos links que deben de consultarse para evaluar opciones de modelos:

* [Precios](https://ai.google.dev/gemini-api/docs/pricing?hl=es-419#gemini-2.5-flash)


A continuación se describe el código minimo necesario para generar nuestro primer agente, es necesrio recarcar que para 

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    name="mi_primer_Agente",
    model="gemini-2.5-flash",
    description="Respondes preguntas generales ",
    instruction="""Respondes las preguntas usando tu conocimiento sobre el tema"""
    )
```

#### Parametros de la función *Agent*


|Parametro   | Obligatorio | Pregunta | Función|
|------------|-------------|------------|----------|
| name       | ✓           |  ¿Como se llama?| Es el nombre del agente |
| model      | ✓           |  ¿Cúal es su cerebro? | El llm que usa como base el agente |
|description |            | ¿Qué hace este agente? | útil en sistemas multiagente para identificar cual consumir|
|instruction |            | ¿Cómo lo hace este agente? | Permite entende el como portarse y responder (si se necesita una respuesta en tipo json, o con un tono en especifico) |

El agente lo puedes levantar desde su interfaz web (aunque a  veces el navegador puede bloquearlo por temas de seguridad). La otra opcion es mediante  el comando  en terminal hacia la carpeta donde se encuentra el archivo.
```bash
adk run my_first_agent/
```
![alt text](image.png)


## Métodos de implementación
Cuando hemos desarrollado nuestro agente, la pregunta natural es ¿como puedo interactuar con el?. El ADK tiene 3 opciones, desde una version que ya tiene una interfaz gráficoca para comunicarse con  el chat, hasta una version con API REST para hacer peticciones y conectarlo a nuestro front. Los 3 métodos son los siguientes
| Método  | ¿Que hace?      | Uso recomendado |
|---------|-----------------|-----------------|
| adk web | Abre una interfaz grafica   | Visualziación rápida |
| adk run | Abre una terminal           | Pruebas rápidas, secuencias de comandos, etc  |  
| adk apir_server   | Ejecuta en forma de API REST | Integración de agentes en aplicaciones web, priebas de producción, etc. |

## Generación de agentes mediante un archivo YAML
Si estamos desarrollando un agente con un equipo que no esta especialmente preparado en programación, existe una solución donde ellos pueden aportar y desarrolar agentes a partir de texto sin necesidad de hacer uso del lenguaje python. A continuación se muestra un ejemplo de como generar un agente usando el archivo  *root_agent.yaml*

```yaml
name: assistant_agent 
model: gemini-2.5-flash 
description: Un asistente útil 
instruction: Eres un asistente útil. 
```


## Tools
