import gradio as gr
import httpx
import pandas as pd
import plotly.express as px
from typing import Tuple

API_URL = "http://127.0.0.1:8000"

# --------------------------------------- DATA FETCHING (SAFE MODE) ------------------------------------------#

def fetch_authors() -> pd.DataFrame:
    try:
        response = httpx.get(f"{API_URL}/authors/", timeout=2.0)
        data = response.json()
        if not data:
            return pd.DataFrame(columns=["id", "name", "bio", "age", "country"])
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Author Fetch Error: {e}")
        return pd.DataFrame(columns=["id", "name", "bio", "age", "country"])

def fetch_books() -> pd.DataFrame:
    try:
        response = httpx.get(f"{API_URL}/books/", timeout=2.0)
        data = response.json()
        if not data:
            return pd.DataFrame(columns=["id", "title", "genre", "year_of_production", "author_id"])
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Book Fetch Error: {e}")
        return pd.DataFrame(columns=["id", "title", "genre", "year_of_production", "author_id"])

# --------------------------------------- LOGIC FUNCTIONS ------------------------------------------#

def add_author(name, bio, age, country):
    try:
        httpx.post(f"{API_URL}/authors/", json={"name": name, "bio": bio, "age": int(age), "country": country}, timeout=3.0)
        gr.Info(f"Author '{name}' added!")
    except:
        gr.Error("Failed to add author. Is the backend running?")
    return fetch_authors()

def delete_author(aid):
    try:
        httpx.delete(f"{API_URL}/authors/{int(aid)}", timeout=3.0)
        gr.Warning(f"Author ID {aid} deleted.")
    except:
        gr.Error("Delete failed.")
    return fetch_authors()

def add_book(title, genre, year, aid):
    try:
        res = httpx.post(f"{API_URL}/books/", json={"title": title, "genre": genre, "year_of_production": int(year), "author_id": int(aid)}, timeout=3.0)
        if res.status_code != 200 and res.status_code != 201:
            gr.Warning(f"Error: {res.text}")
        else:
            gr.Info(f"Book '{title}' added!")
    except:
        gr.Error("Connection error.")
    return fetch_books()

def delete_book(bid):
    try:
        httpx.delete(f"{API_URL}/books/{int(bid)}", timeout=3.0)
        gr.Warning(f"Book ID {bid} deleted.")
    except:
        gr.Error("Delete failed.")
    return fetch_books()

def make_charts():
    authors = fetch_authors()
    books = fetch_books()
    
    if books.empty or "genre" not in books.columns:
        empty_fig = px.scatter(title="No Data for Charts")
        return empty_fig, empty_fig

    # Pie Chart
    pie = px.pie(books, names='genre', title="Books by Genre", 
                 color_discrete_sequence=px.colors.sequential.Reds_r, hole=0.3)
    
    # Bar Chart (Counts per genre)
    counts = books['genre'].value_counts().reset_index()
    counts.columns = ['Genre', 'Count']
    bar = px.bar(counts, x='Genre', y='Count', title="Genre Popularity", color='Genre',
                 color_discrete_sequence=['#ff4b4b'])
    
    return pie, bar

# --------------------------------------- GRADIO UI ------------------------------------------#

custom_theme = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="gray",
    font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"],
)

with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("# 📚 Library Control Dashboard (Red Edition)")

    with gr.Tab("📊 Analytics"):
        with gr.Row():
            chart_pie = gr.Plot()
            chart_bar = gr.Plot()
        refresh_charts = gr.Button("🔄 Refresh Charts", variant="primary")
        
    with gr.Tab("✒️ Manage Authors"):
        with gr.Row():
            with gr.Column(scale=3):
                auth_table = gr.DataFrame(value=pd.DataFrame(columns=["id", "name", "bio", "age", "country"]), interactive=False)
                refresh_auth = gr.Button("🔄 Refresh Table")
            with gr.Column(scale=1):
                gr.Markdown("### Add New Author")
                in_name = gr.Textbox(label="Name")
                in_bio = gr.Textbox(label="Bio")
                in_age = gr.Number(label="Age", value=30)
                in_country = gr.Textbox(label="Country")
                btn_add_auth = gr.Button("Add Author", variant="primary")
                gr.Markdown("---")
                in_del_auth = gr.Number(label="ID to Delete")
                btn_del_auth = gr.Button("Delete Author", variant="stop")

    with gr.Tab("📖 Manage Books"):
        with gr.Row():
            with gr.Column(scale=3):
                book_table = gr.DataFrame(value=pd.DataFrame(columns=["id", "title", "genre", "year_of_production", "author_id"]), interactive=False)
                refresh_book = gr.Button("🔄 Refresh Table")
            with gr.Column(scale=1):
                gr.Markdown("### Add New Book")
                in_title = gr.Textbox(label="Title")
                in_genre = gr.Textbox(label="Genre")
                in_year = gr.Number(label="Year", value=2024)
                in_aid = gr.Number(label="Author ID", value=1)
                btn_add_book = gr.Button("Add Book", variant="primary")
                gr.Markdown("---")
                in_del_book = gr.Number(label="ID to Delete")
                btn_del_book = gr.Button("Delete Book", variant="stop")

    # --- EVENT LOGIC ---
    refresh_auth.click(fetch_authors, outputs=auth_table)
    btn_add_auth.click(add_author, inputs=[in_name, in_bio, in_age, in_country], outputs=auth_table)
    btn_del_auth.click(delete_author, inputs=[in_del_auth], outputs=auth_table)

    refresh_book.click(fetch_books, outputs=book_table)
    btn_add_book.click(add_book, inputs=[in_title, in_genre, in_year, in_aid], outputs=book_table)
    btn_del_book.click(delete_book, inputs=[in_del_book], outputs=book_table)
    
    refresh_charts.click(make_charts, outputs=[chart_pie, chart_bar])
    
    # Load data and charts on startup
    demo.load(fetch_authors, outputs=auth_table)
    demo.load(fetch_books, outputs=book_table)
    demo.load(make_charts, outputs=[chart_pie, chart_bar])

if __name__ == "__main__":
    demo.launch(server_port=7861)