import nbformat as nbf
import re
import sys

if __name__ == '__main__':

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r') as file, open(output_path, 'w') as output_file:

        nb = nbf.v4.new_notebook()
        cells = []

        text = file.read()
        text = re.sub(r'---\n(.|\n)*---\n', '', text)

        is_open = False
        cursor = 0
        blocks = []

        open_marker = '```python'
        close_marker = '```'

        while cursor < len(text):
            last_cursor = cursor
            if is_open:
                cursor = text.find(close_marker, cursor)
                if cursor == -1: break
                contents = text[last_cursor:cursor].strip()
                cursor += len(close_marker)
                cells.append(nbf.v4.new_code_cell(contents))
            else:
                cursor = text.find(open_marker, cursor)
                if cursor == -1: break
                contents = text[last_cursor:cursor].strip()
                cursor += len(open_marker)
                cells.append(nbf.v4.new_markdown_cell(contents))
            is_open = not is_open

        nb["cells"] = cells
        nbf.write(nb, output_file)
