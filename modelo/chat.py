import ollama
from modefile import modelfile
from repository import get_results

def get_informations(prompt):
   informations = get_results(prompt)
   global quest_informations
   quest_informations = informations['content']
   if quest_informations == "Não foi possível achar informações pertinentes.":
      final_conversation = {'prompt': 'erro', 'fonts': '', 'data': ''}
   
      return final_conversation

   final_prompt = f"""
    Você é um assistente virtual do CEFET-MG (Centro Federal de Educação Tecnológica), campus Araxá. E fornece informações sobre a instituição. Você deve ser objetivo, amigável e profissional. Suas respostas devem ter no máximo 200 caracteres.
    Você deve responder cordialmente e objetivamente a mensagem do usuário com base nas informações a seguir: 
    {informations['content']}
    
    FIM DAS INFORMAÇÕES


    Você deve responder, com base no que foi fornecido, responda a seguinte mensagem: {prompt}
   """
   conversation = {
         'role': 'user',
         'content': final_prompt,
      }
   
   final_conversation = {'prompt': conversation, 'fonts': informations['fonts'], 'data': informations['content']}

   return final_conversation

e = 1

def enviar_mensagem(prompt):
   quest_informations = ''

   ollama.create(model="mistral", modelfile=modelfile)
   resposta_modelo = ""

   informations = get_informations(prompt)

   if informations["prompt"] == "erro":
      prompt_new = "Forneça uma resposta culta ao usuário baseado: Não possuo informações suficientes no meu banco de dados para responder à esta pergunta. Por favor, consulte um servidor da instituição."
      response = ollama.generate(model="chatbot", 
      prompt=prompt_new,
      stream=False
      )
      
      resposta_modelo = {"resposta": response['response'], "fonts": "", "data": ""}
      return resposta_modelo

   response = ollama.generate(model="chatbot", 
   prompt=informations['prompt']['content'],
   stream=False
   )

   # for chunk in response:
   #    resposta = chunk['message']['content']
   #    resposta_modelo += resposta
   #    print(resposta, end='', flush=True)
   
   print("\n fontes:")
   fonts = ""

   for font in informations['fonts']:
      fonts += font.replace('\n \n', '') + '. '
      print(font.replace('\n \n', '') + '. ')
   
   resposta_modelo = {"resposta": response['response'], "fonts": fonts, "data": informations["data"]}
   
   return resposta_modelo

   historico_mensagens.append({
      'role': 'user',
      'content': prompt
   })

   historico_mensagens.append({
      'role': 'assistant',
      'content': resposta_modelo
   })
   