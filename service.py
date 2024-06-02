import pandas as pd
import os

PATIENT_PATH = 'pacientes/'
FOOD_PATH = 'food_db'


def get_all_patients():
    listFile = os.listdir(PATIENT_PATH)
    listPatientName = []

    for file in listFile:
        listPatientName.append(file.replace('.csv', '').title())

    return listPatientName


def read_patient_file(patient):
    patient_file = pd.read_csv(PATIENT_PATH+patient+'.csv', delimiter=';')
    food_list = pd.read_csv(FOOD_PATH+'.csv', delimiter=';')

    # Adiciona informação de calorias de acordo com a food_list na patient_file usando left join
    return pd.merge(patient_file, food_list, on='comida', how='left')


def generate_diet_plan(patient, diet_type):
    # Carregar os dados das planilhas em dataframes
    patient_file = read_patient_file(patient)
    food_list = pd.read_csv(FOOD_PATH+'.csv', delimiter=';')

    # Mesclar as tabelas para obter as calorias das food_list do histórico
    lookup_patient_food_database = pd.merge(patient_file, food_list, on=[
        'comida', 'comida'], suffixes=('', '_drop'))

    # Obter as sugestões
    sugestoes = analyze_suggestions(
        lookup_patient_food_database, food_list, diet_type)

    return sugestoes


def analyze_suggestions(lookup_patient_food_database, food_list, diet_type):
    sugestoes = []

    # Identificar as 10 food_list que a pessoa mais comeu, filtrando de acordo com o diet_type
    if (diet_type == 'perder'):
        top_10_comidas = lookup_patient_food_database.nlargest(10, 'calorias')
    else:
        top_10_comidas = lookup_patient_food_database.nsmallest(10, 'calorias')

    for _, row in top_10_comidas.iterrows():
        comida_atual = row['comida']
        comida_caloria_atual = row['calorias']

        tipo_refeicao = row['refeicao']
        categoria = row['categoria']
        calorias_atuais = row['calorias']

        # Filtrar as food_list do mesmo tipo de refeição que não estão na lista das top 10 food_list
        if diet_type == 'ganhar':
            sugestoes_possiveis = food_list[(food_list['categoria'] == categoria) & (
                food_list['comida'] != comida_atual) & (food_list['calorias'] > comida_caloria_atual)]
        else:
            sugestoes_possiveis = food_list[(food_list['categoria'] == categoria) & (
                food_list['comida'] != comida_atual) & (food_list['calorias'] <= comida_caloria_atual)]

        # Adicionar a sugestão ao dataframe de sugestões
        if not sugestoes_possiveis.empty:
            sugestao = sugestoes_possiveis.sample(1).iloc[0]
            calorias_sugeridas = sugestao['calorias']
            diferenca_calorica = calorias_sugeridas - calorias_atuais

            sugestoes.append({
                'tipo refeicao': tipo_refeicao,
                'comida atual': comida_atual,
                'comida sugerida': sugestao['comida'],
                'categoria': categoria,
                'diferença calorica': diferenca_calorica
            })
    return pd.DataFrame(sugestoes)
