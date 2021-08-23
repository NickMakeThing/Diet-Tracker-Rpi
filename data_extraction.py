def get_tables(response):
    blocks=response['Blocks']
    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)
    if len(table_blocks) <= 0:
        return None
    else:
        tables = {
            'blocks_map': blocks_map,
            'table_blocks': table_blocks 
        }
        return tables

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        rows[row_index] = {}
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text

def get_macronutrients(row,last_column,data):
    nutrients = ['energy','protein','fat','carbs','carbohydrate','sugars']
    for nutrient in nutrients:
        if nutrient in row[1].lower():
            amount = validate_data(row[last_column])
            if amount['error']:
                amount['content']+= '| row:'+nutrient
                return amount
            else:
                if nutrient == 'carbohydrate':
                    nutrient = 'carbs'
                data[nutrient] = amount['content']
                break
    return data

def validate_data(amount):
    original = amount
    for i in ['kj','g','cal','kcal','(',')',' ','k','j','/']:
        amount = amount.lower().replace(i,'')
    if amount.isnumeric() or isfloat(amount):
        return {'error': None, 'content': amount}
    else:
        return {'error':'bad data', 'content': original}

def isfloat(string): #very sad that python does not have this utility built in.
    try:
        if isinstance(float(string),float):
            return True
        else: return False
    except:
        return False

def get_last_column(label):
    last_column = None
    for row in label:
        for column in label[row]:
            if 'per 100' in label[row][column].lower():
                last_column=column
                break
    return last_column

def get_label_data(response):
    data = {
        'energy':0,
        'protein':0,
        'fat':0,
        'carbs':0,
        'sugars':0
    }
    tables = get_tables(response)
    if not tables:
        return  {'error':'no tables detected'}
    blocks_map = tables['blocks_map']
    table_blocks = tables['table_blocks']
    for index, table in enumerate(table_blocks):
        label=get_rows_columns_map(table, blocks_map)
        last_column = get_last_column(label)
        if last_column:
            break
    if not last_column:
        return {'error':'could not find \'per 100g\' column'}

    for row in label:
        data = get_macronutrients(label[row],last_column,data)
        if 'error' in data:
            return data
    return data
