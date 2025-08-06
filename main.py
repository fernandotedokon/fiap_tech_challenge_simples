from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

app = FastAPI(title="API Biblioteca")

BASE_URL = "https://books.toscrape.com/"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "books.csv")

os.makedirs(DATA_DIR, exist_ok=True)

def extrair_books(pages=1):
    books = []
    next_url = BASE_URL + "catalogue/page-1.html"

    for i in range(pages):
        print(f"Extraindo página {i+1}: {next_url}")
        response = requests.get(next_url)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar a página: {next_url}")
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = article.select_one(".price_color").text.strip()
            availability_text = article.select_one(".availability").text.strip()
            rating = article.p.get("class")[1]
            image_url = BASE_URL + article.img["src"].replace("../", "")
            book_url = BASE_URL + "catalogue/" + article.h3.a["href"].replace("../", "")
            
            # Detalhes adicionais da página do livro
            book_resp = requests.get(book_url)
            book_soup = BeautifulSoup(book_resp.text, "html.parser")
            disponibility = book_soup.select_one("table.table.table-striped tr:nth-child(6) td").text.strip()
            category = book_soup.select("ul.breadcrumb li a")[-1].text.strip()

            books.append({
                "id": len(books) + 1,
                "title": title,
                "price": price,
                "availability": availability_text,
                "rating": rating,
                "disponibility": disponibility,
                "category": category,
                "image": image_url
            })

        next_link = soup.select_one("li.next a")
        if next_link:
            next_url = BASE_URL + "catalogue/" + next_link["href"]
        else:
            break

    return books

def salvar_csv(books):
    df = pd.DataFrame(books)
    df.to_csv(CSV_PATH, index=False)

def carregar_books():
    if not os.path.exists(CSV_PATH):
        return []
    return pd.read_csv(CSV_PATH).to_dict(orient="records")

@app.get("/api/v1/health")
def health_check():
    exists = os.path.exists(CSV_PATH)
    return {
        "status": "ok",
        "data_file_exists": exists,
        "books_count": len(carregar_books()) if exists else 0
    }

@app.get("/api/v1/extrair/{pages}")
def extrair_e_salvar(pages: int):
    try:
        if (pages >= 0 and pages <= 5) or pages == 50:
            books = extrair_books(pages=pages)
        else:
            raise HTTPException(status_code=400, detail="Número de páginas deve ser entre 1 e 5 ou 50 para extrair todas as paginas")
        #if pages < 0 or pages > 5 or pages != 50:
        #    raise HTTPException(status_code=400, detail="Número de páginas deve ser entre 1 e menor que 5 ou 50 para extrair todas as paginas")
        #else:
        #    books = extrair_books(pages=pages)
        salvar_csv(books)
        return {"message": f"{len(books)} livros salvos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/books")
def listar_books():
    books = carregar_books()
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")
    return {"books": books}

@app.get("/api/v1/books/{id}")
def obter_livro_por_id(id: int):
    books = carregar_books()
    for book in books:
        if int(book["id"]) == id:
            return book
    raise HTTPException(status_code=404, detail=f"Livro com ID {id} não encontrado.")

@app.get("/api/v1/books/search")
def buscar_livros(title: str = Query(None), category: str = Query(None)):
    books = carregar_books()
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum dado disponível.")

    resultado = books
    if title:
        resultado = [b for b in resultado if title.lower() in b["title"].lower()]
    if category:
        resultado = [b for b in resultado if category.lower() in b["category"].lower()]

    if not resultado:
        raise HTTPException(status_code=404, detail="Nenhum livro corresponde aos critérios.")
    return {"results": resultado}

@app.get("/api/v1/categories")
def listar_categorias():
    books = carregar_books()
    if not books:
        raise HTTPException(status_code=404, detail="Dados não encontrados.")
    categorias = sorted(set(book["category"] for book in books))
    return {"categories": categorias}
