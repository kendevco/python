import os

# Directory containing the text file
directory = r"C:\Users\kenne\Videos\Transcribe"
filename = "y2mate.is - EN VIVO _ Asamblea Pública para la Regulación de Fenómenos Aéreos Anómalos no Identificados-tu7Y0e_9HWU-720p-1694579769.txt"
file_path = os.path.join(directory, filename)

# Read the text file
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Break the text into 5000 character chunks
chunk_size = 5000
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Add delimiters between each chunk
delimiter = "\n\n\n"
translated_text = delimiter.join(chunks)

# Write the translated text to a new file
output_file_path = os.path.join(directory, "translated_text.txt")
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(translated_text)