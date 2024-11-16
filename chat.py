from main import *

while True:
    query = input("Faça uma pergunta sobre o calendário UFC ou digite 'sair' para fechar o chat: \n")
    
    if query == 'sair':
        break
    else:    
        prompt = HumanMessage(content=custom_prompt(query))

        res = model.invoke([prompt])
        print(res.content)