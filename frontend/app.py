import gradio as gr
import httpx
import pandas as pd

# The address of our backend
API_URL = "http://127.0.0.1:8000"

# --- HELPER FUNCTIONS ---

def fetch_authors():
    try:
        response = httpx.get(f"{API_URL}/authors/", timeout=2)
        data = response.json()
        # "Functionalities" mapped to Authors
        return pd.DataFrame(data, columns=["id", "name", "bio", "age", "country"])
    except:
        return pd.DataFrame(columns=["id", "name", "bio", "age", "country"])

def fetch_books(choice='All'):
    try:
        response = httpx.get(f"{API_URL}/books/", timeout=2)
        data = response.json()
        # "Robots" mapped to Books
        dataframe = pd.DataFrame(data, columns=["id", "title", "genre", "year_of_production", "author_id"])
        if choice == 'All' or dataframe.empty:
            return dataframe
        return dataframe[dataframe['genre'] == choice]
    except:
        return pd.DataFrame(columns=["id", "title", "genre", "year_of_production", "author_id"])

def create_author(name, bio, age, country):
    payload = {
        "name": name,
        "bio": bio,
        "age": int(age),
        "country": country
    }
    httpx.post(f"{API_URL}/authors/", json=payload)
    return fetch_authors()

def create_book(title, genre, year, author_id):
    payload = {
        "title": title,
        "genre": genre,
        "year_of_production": int(year),
        "author_id": int(author_id)
    }
    httpx.post(f"{API_URL}/books/", json=payload)
    return fetch_books()

def update_book(title, genre, author_id):
    # Mapping "update_robot" logic to books
    payload = {
        "title": title,
        "genre": genre,
        "author_id": int(author_id)
    }
    httpx.put(f"{API_URL}/books/", json=payload)
    return fetch_books()

# --- THE RED THEME ---
red_theme = gr.themes.Soft(primary_hue='red', secondary_hue='gray')

with gr.Blocks(theme=red_theme) as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("# 📚 Library Control Dashboard")
            gr.Markdown(f"### Track books, add authors, and manage library data. The UI reads from {API_URL}")
        
        with gr.Column():
            gr.Markdown("### API Status")
            gr.Markdown(f'Connected to {API_URL}')
            # Safety checks for stats
            try:
                num_books = len(fetch_books())
                num_authors = len(fetch_authors())
            except:
                num_books, num_authors = 0, 0
            gr.Markdown(f" - Books loaded: {num_books}")
            gr.Markdown(f" - Authors loaded: {num_authors}")

    with gr.Tab("Overview"):
        with gr.Row():
            gr.Markdown("## Current Library Setup")
        with gr.Row():
            with gr.Column():
                # We use a static list or fetch safely to prevent startup freeze
                genre_dropdown = gr.Dropdown(label="Filter by Genre", choices=['All'], value='All', interactive=True)
            with gr.Column():
                refresh_btn = gr.Button("Refresh Overview", variant="primary")
        
        with gr.Column():
            gr.Markdown("### Books (Robots)")
            book_table = gr.DataFrame(fetch_books(), interactive=False)
            gr.Markdown("### Authors (Functionalities)")
            author_table = gr.DataFrame(fetch_authors(), interactive=False)
            
            refresh_btn.click(fetch_books, outputs=book_table)
            refresh_btn.click(fetch_authors, outputs=author_table)

    with gr.Tab("Add Book"):
        gr.Markdown("## Insert a new book")
        with gr.Row():
            title_input = gr.Textbox(label="Title", placeholder="Enter book title")
            genre_input = gr.Textbox(label="Genre", placeholder="Enter genre")
            year_input = gr.Number(label="Year", value=2024)
            auth_id_input = gr.Number(label="Author ID", value=1)
        with gr.Row():
            add_book_btn = gr.Button("Create Book", variant="primary")
            add_book_btn.click(create_book, inputs=[title_input, genre_input, year_input, auth_id_input], outputs=book_table)

    with gr.Tab("Add Author"):
        gr.Markdown("## Insert a new author")
        with gr.Row():
            name_input_auth = gr.Textbox(label="Name", placeholder="Enter author name")
            bio_input_auth = gr.Textbox(label="Bio", placeholder="Enter bio")
            age_input_auth = gr.Number(label="Age", value=30)
            country_input_auth = gr.Textbox(label="Country", placeholder="Enter country")
        with gr.Row():
            add_author_btn = gr.Button("Create Author", variant="primary")
            add_author_btn.click(create_author, inputs=[name_input_auth, bio_input_auth, age_input_auth, country_input_auth], outputs=author_table)

    with gr.Tab("Manage Book Author"):
        gr.Markdown("## Update the author of a book")
        with gr.Row():
            # Using simple text/number inputs to prevent the dropdown startup freeze
            book_title_update = gr.Textbox(label="Book Title")
            new_author_id = gr.Number(label="New Author ID", value=1)
            book_genre_update = gr.Textbox(label="Genre")
        with gr.Row():
            update_btn = gr.Button("Update Relationship", variant="primary")
            update_btn.click(update_book, inputs=[book_title_update, book_genre_update, new_author_id], outputs=book_table)

if __name__ == "__main__":
    demo.launch()