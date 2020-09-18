from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import \
    Features, EntitiesOptions

from cgi import parse_multipart, parse_header
from io import BytesIO
from base64 import b64decode
import json, os

from numpy import sort,absolute

#
# CONTEXT main
#
###################################################################

saida_vazio={
            "recommendation": "",
            "entities": []
            }
            
saida_modelo_fora={
            "recommendation": "Ao parecer seu comentario fala sobre um modelo que não posso considerar",
            "entities": []
            }


def fun_natural_language_understanding(text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(version="2018-09-28",iam_apikey='        ',url='')
    features = Features(entities=EntitiesOptions(sentiment=True,model=""))
    response = natural_language_understanding.analyze(text = text,features=features).get_result()
    
    return response

# Chamando o STT  form_data_audio

def chamar_SpeechToTextV1():

    # Set the URL endpoint for your Watson STT client
    speech_service = SpeechToTextV1(
    url='',
    iam_apikey='')   
    
    
# Read audio file and call Watson STT API:
    with open(
        os.path.join(
            os.path.dirname(__file__), './.',
            'audio_sample.flac'
        ), 'rb'
    ) as audio_file:
        # Transcribe the audio.flac with Watson STT
        # Recognize method API reference: 
        # https://cloud.ibm.com/apidocs/speech-to-text?code=python#recognize
        stt_result = speech_service.recognize(
            audio=audio_file,
            content_type='audio/flac',
            model='pt-BR_BroadbandModel'
        ).get_result()
    
    return stt_result['results'][0]['alternatives'][0]['transcript']

# AUIXILIAR processar_entities
# 
#
#

def funcao_recomendacao_MULTIPLA(score_ordenado_etiquetas_MULTIPLA,score_ordenadoNEGATIVOS_MULTIPLA):
    return score_ordenado_etiquetas_MULTIPLA

# AUIXILIAR processar_entities
#
# 
#
#
def funcao_recomendacao(score_ordenado_etiquetas_UNICO,score_ordenadoNEGATIVOS_UNICO):
    saida={}
    saida['score_ordenado_etiquetas_UNICO']=score_ordenado_etiquetas_UNICO
    #score_ordenado_etiquetas_UNICO[0]
    saida['score_ordenadoNEGATIVOS_UNICO']=score_ordenadoNEGATIVOS_UNICO
    return "score_ordenado_etiquetas_UNICO"
#
# processar_entities
#

def processar_entities(data_ARRAY_entities):
    
    saida_entities=[]
    score_ACESSORIOS=0.0
    score_CONFORTO=0.0
    score_CONSUMO=0.0
    score_DESEMPENHO=0.0
    
    score_DESIGN=0.0
    score_MANUTENCAO=0.0
    score_MODELO=0.0
    score_SEGURANCA=0.0
    
    for elemento in data_ARRAY_entities:
    		score=elemento['sentiment']['score']
    		novo=[elemento['type'],elemento['text'],score]
    
    		if (elemento['type']=="ACESSORIOS"):
    			score_ACESSORIOS=score_ACESSORIOS+score
    		if (elemento['type']=="CONFORTO"):
    			score_CONFORTO=score_CONFORTO+score
    		if (elemento['type']=="CONSUMO"):
    			score_CONSUMO=score_CONSUMO+score
    		if (elemento['type']=="DESEMPENHO"):
    			score_DESEMPENHO=score_DESEMPENHO+score
    
    		if (elemento['type']=="DESIGN"):
    			score_DESIGN=score_DESIGN+score
    		if (elemento['type']=="MANUTENCAO"):
    			score_MANUTENCAO=score_MANUTENCAO+score
    		if (elemento['type']=="MODELO"):
    			score_MODELO=score_MODELO+score
    		if (elemento['type']=="SEGURANCA"):
    			score_SEGURANCA=score_SEGURANCA+score								
    
    		saida_entities.append(novo)    
    
    score_ordenado=[]
    score_ordenado_etiquetas=[]
    
    
    if score_SEGURANCA<0:	
    	score_ordenado.append(score_SEGURANCA)
    	score_ordenado_etiquetas.append("SEGURANCA")
    
    
    if score_CONSUMO<0:	
    	score_ordenado.append(score_CONSUMO)
    	score_ordenado_etiquetas.append("CONSUMO")
    
    	
    
    if score_DESEMPENHO<0:	
    	score_ordenado.append(score_DESEMPENHO)
    	score_ordenado_etiquetas.append("DESEMPENHO")
    
    	
    
    if score_MANUTENCAO<0:	
    	score_ordenado.append(score_MANUTENCAO)	
    	score_ordenado_etiquetas.append("MANUTENCAO")	
    
    
    
    if score_CONFORTO<0:	
    	score_ordenado.append(score_CONFORTO)	
    	score_ordenado_etiquetas.append("CONFORTO")	
    
    
    
    if score_DESIGN<0:	
    	score_ordenado.append(score_DESIGN)	
    	score_ordenado_etiquetas.append("DESIGN")	
    
    
    
    if score_ACESSORIOS<0:	
    	score_ordenado.append(score_ACESSORIOS)	
    	score_ordenado_etiquetas.append("ACESSORIOS")	

    score_ordenadoNEGATIVOS=sort(score_ordenado)
    		
    
    if len(score_ordenado_etiquetas)==1:
	    desempate_UNICA=funcao_recomendacao(score_ordenado_etiquetas,score_ordenadoNEGATIVOS)
    else:
	    desempate_UNICA=funcao_recomendacao_MULTIPLA(score_ordenado_etiquetas,score_ordenadoNEGATIVOS)
    return desempate_UNICA
    #return [score_ordenado,score_ordenado_etiquetas,score_ordenadoNEGATIVOS]
    #return "apenas230"


# AUIXILIAR processar_entities
#
# 
#
#

def saida_entidades_desafio_8(data):
    vetor_saida_entities=[]
    
    for elemento in data:
    	novo_sentimento={}
    
    	novo_sentimento['entity']=elemento['type']
    	
    	novo_sentimento['sentiment']=elemento['sentiment']['score']
    	
    	novo_sentimento['mention']=elemento['text']
    	
    	vetor_saida_entities.append(novo_sentimento)
    return vetor_saida_entities
    #return data
    
    
#
# processar_texto
#

def processar_texto(texto,modelos_removido_CAR):
    data=fun_natural_language_understanding(texto)
    
    media_score=0
    
    for elemento in data['entities']:
	    media_score=media_score+elemento['sentiment']['score']
	    
	    
    saida={}
    saida['recommendation']="ven"
    
    if(media_score>=0):
        return saida_vazio
    else:
        preRECOMENDACAO=processar_entities(data['entities'])
        saida_processar_entities=saida_entidades_desafio_8(data['entities'])
        saida_sentimento_negativo={ "recommendation": modelos_removido_CAR[0],"entities":saida_processar_entities}
        return saida_sentimento_negativo
    
#
# CONTEXT main
#
###################################################################


#
# MAIN
#
#

def main(args):
    c_type, p_dict = parse_header(args['__ow_headers']['content-type'])
    decoded_string = b64decode(args['__ow_body'])
    p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
    p_dict['CONTENT-LENGTH'] = len(decoded_string)
    form_data = parse_multipart(BytesIO(decoded_string), p_dict)

    
    ret = {}
    formulario_items=[]
    for key, value in form_data.items():
        ret[key] = len(value[0])
        formulario_items.append(key)
        
# Com CARRO....Tem menos de 2 elementos, resposta VAZIO
    if (len(formulario_items)<2):
        return saida_vazio
        
#verificar que tenha campo CAR
    try:
        car_index = formulario_items.index("car")
    except:
        car_index = -1

# Essencial ter CARRO
    if (car_index==-1):    
        return saida_vazio
    if (ret['car']==0):
            return saida_vazio
            
    modelos=["TORO","DUCATO","FIORINO","CRONOS","FIAT 500","MAREA","LINEA","ARGO","RENEGADE"]

# Este CARRO, tem que ser um dos modelos deste PROJETO
    try:
        modelo_index = modelos.index(form_data.get('car')[0]) 
    except:
        modelo_index = -1
#Verfica que se um MODELO deste projeto        
    if (modelo_index==-1):    
        return saida_modelo_fora
    else:
        modelos.remove(form_data.get('car')[0])

# verifca que tenha text
    try:
        text_index = formulario_items.index("text")
    except:
        text_index = -1
    
# verifca que tenha audio
    try:
        audio_index = formulario_items.index("audio")
    except:
        audio_index = -1
    
# Essencial ter TEXT
    if (text_index==-1):    
        if (audio_index==-1):        
            return saida_vazio
        else:
            if (ret['audio']>0):
                ret["processamento"]="Processar AUDIO form_data ?"
                
                fo = open("audio_sample.flac", 'wb')
                fo.write(form_data.get('audio')[0])
                fo.close()
                stt_result=chamar_SpeechToTextV1()
                ret["stt_result"]=stt_result
                #chamar_SpeechToTextV1()
                ret["SAIDA"]=processar_texto(stt_result,modelos)
                return ret["SAIDA"]
                
            else:
                ret["processamento"]="AUDIO zerado"
                return saida_vazio
                
    else:
        if (ret['text']>0):
            ret["processamento"]="Processar text"
            #ret["SAIDA"]=funcao_dicionario(form_data.get('text')[0])
            
            ret["SAIDA"]=processar_texto(form_data.get('text')[0],modelos)
            ret["melhorar"]="Passo STT"
            return ret["SAIDA"]
        else:
            ret["processamento"]="TEXT zerado"
            return saida_vazio

    return ret