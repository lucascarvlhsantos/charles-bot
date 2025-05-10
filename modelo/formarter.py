import re, os

def format_results(results):
    formatted_data = ''
    font_num = 1
    fonts = []
    for doc, _ in results:
        formatted_data += doc.page_content.strip().replace("\n", " ")
        if doc.metadata.get('page'):
            page = str(doc.metadata["page"])
        else:
            page = '1'
        source = doc.metadata['source'].replace("data\\", "")
        fonts.append(f'fonte {font_num}: {source},página: {page} \n \n')
        font_num += 1
    return {'content': formatted_data, 'fonts': fonts}

def format_chunk_names(chunks):
    chunk_num = 1
    last_page = ''

    new_chunks = []

    for chunk in chunks:
        # CONVERTE DE 'data/filename.ext' para: 'filename'
        file_name = chunk.metadata['source']
        if chunk.metadata.get('page'):
            page = str(chunk.metadata["page"])
        else:
            page = '1'
            
        pre_formated = os.path.splitext(os.path.basename(file_name))[0]
        file_name = re.sub(r'[ -]+', '_', pre_formated).lower()
        space_and_page_correction = file_name + '/page/' + page

        if space_and_page_correction != last_page:
            chunk_num = 1
            formated_chunk = space_and_page_correction + "/chunk/" + str(chunk_num)
            new_chunks.append(formated_chunk)
            last_page = space_and_page_correction
            continue
        
        chunk_num += 1
        formated_chunk = space_and_page_correction + "/chunk/" + str(chunk_num)
        new_chunks.append(formated_chunk)
        last_page = space_and_page_correction

    return new_chunks