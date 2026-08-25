path = "http://127.0.0.1:8000/api/books/{book_id}"

path_ready = path.format(book_id=11111)

print(path_ready)