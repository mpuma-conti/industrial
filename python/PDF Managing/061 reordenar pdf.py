#Reordenado de paginas (Páginas 1 y 4)(Páginas 3 y 6) (Páginas 5 y 8) Y así sucesivamente...

from PyPDF2 import PdfReader, PdfWriter

# Abrir el PDF original
input_path = "salida.pdf"
output_path = "archivo_ordenado.pdf"

reader = PdfReader(input_path)
writer = PdfWriter()

# Reordenar las páginas
pages = reader.pages
for i in range(0, len(pages), 2):
    writer.add_page(pages[i])  # Página impar
    if i + 3 < len(pages):
        writer.add_page(pages[i + 3])  # Página par, si existe

# Guardar el nuevo archivo
with open(output_path, "wb") as output_file:
    writer.write(output_file)

print("Archivo reordenado correctamente.")
