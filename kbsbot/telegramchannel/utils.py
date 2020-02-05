from telegram import InlineKeyboardButton


def prepare_keyboard(options):
    keyboard = []

    for option in options:
        keyboard.append([InlineKeyboardButton(option["option"], callback_data=option["payload"])])

    return keyboard


def prepare_chatbot_cap(data):
    func_bot = data["description"]
    full_response = f"Hola, {func_bot} \nPuedo resolver las siguientes dudas:\n"
    for intent in data["intents"]:
        full_response += f"- {intent['description']} \n"
    return full_response


local_data = {
  "agent": "http://127.0.0.1/ockb/resources/OpenCampus",
  "description": "Este chatbot se encarga de resolver dudas sobre cursos de la plataforma Open Campus",
  "intents": [
    {
      "description": "Obtener las fechas importantes del curso",
      "intent": "ObtenerFechas"
    },
    {
      "description": "Obtener una breve descripcion del curso",
      "intent": "ObtenerInformacion"
    },
    {
      "description": "Obtener prerequisitos del curso",
      "intent": "ObtenerPrerequisitos"
    },
    {
      "description": "Obtener el precio del curso",
      "intent": "ObtenerPrecio"
    },
    {
      "description": "Obtener las fechas de inicio del curso",
      "intent": "ObtenerFechasInicio"
    },
    {
      "description": "Presentar la oferta actual de cursos",
      "intent": "listarCursos"
    },
    {
      "description": "Obtener los nombres de los docentes del curso",
      "intent": "ObtenerDocente"
    },
    {
      "description": "Obtener la duracion del curso",
      "intent": "ObtenerDuracion"
    },
    {
      "description": "Obtener los contenidos del curso",
      "intent": "ObtenerContenidos"
    }
  ]
}
# print(prepare_chatbot_cap(local_data))
