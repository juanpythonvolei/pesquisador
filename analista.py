import requests
from bs4 import BeautifulSoup
from time import sleep
from analisador import analisar
import pandas as pd
import streamlit as st
from io import BytesIO



def pegar_infos_gerais_mercado_livre(link,produto):
    try:
        url = f"{link}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        info_geral = soup.find(class_='ui-pdp-description__content')
        vendedor = soup.find(class_="ui-pdp-color--BLACK ui-pdp-size--LARGE ui-pdp-family--SEMIBOLD ui-seller-data-header__title non-selectable")
        preco = soup.find(class_="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact")
        imagem = soup.find(class_="ui-pdp-gallery__column__variation-gallery")
        link_imagem = imagem.get("src")
        dict_mercado_livre = {'vendedor':vendedor.text,'preco':preco.text,'infos':info_geral.text,'produto':produto,'link':link,"link imagem":link_imagem}
        return dict_mercado_livre
    except:
        pass
def pesquisar_mercado_livre(produto):
    lista_mercado_livre = []
    url = f"https://lista.mercadolivre.com.br/{produto}"
    response = requests.get(url)
    pagina = BeautifulSoup(response.content, "html.parser")
    elemento_titulo = pagina.find(class_="ui-search-results ui-search-results--without-disclaimer")
    lista = elemento_titulo.find('ol')
    for item in lista:
            tags = item.find_all("a")
            for tag in tags:
                link = tag.get("href")
                dict = pegar_infos_gerais_mercado_livre(link,produto)
                if dict in lista_mercado_livre:
                     pass
                else:
                    lista_mercado_livre.append(dict)
    return lista_mercado_livre        

def pesquisar(produto):
    lista_dfs = []
    if produto:
            texto_mercado_livre = ''
            for item in pesquisar_mercado_livre(produto):
                try:
                    info_mercado_livre = f'''Vendedor: {item['vendedor']}
                    item: {item['infos']}
                    Preço: {item['preco']}
                    link: {item['link']}
                    Produto: {item['produto']}'''
                    texto_mercado_livre += info_mercado_livre
                    df_unico = pd.DataFrame(item,index=[1])

                    lista_dfs.append(df_unico)
                except:
                    pass               
            df_final = pd.concat(lista_dfs)         
            resposta = analisar("Qual é o produto mais vantajoso a ser comprado levando em consideração a qualidade tecnica e seu preço ?. Me diga além disso, o nome de seu vendedor,o link para o produto do site, e faça uma tabela decrescente em relação ao preço dos demais produtos,seus vendedores e seus links de compra",texto_mercado_livre)
            return {"resposta":resposta,"pesquisa":df_final}
    
@st.cache_data
def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data  
    