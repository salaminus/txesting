import hashlib

def calculate_hash(text):
    # Создаем объект хеширования
    hash_object = hashlib.sha256()
    
    # Обновляем объект хеширования данными
    hash_object.update(text.encode('utf-8'))
    
    # Получаем хеш-сумму в шестнадцатеричном формате
    hash_sum = hash_object.hexdigest()
    
    return hash_sum

# # Пример использования
# input_text = "Привет, мир!"
# hash_sum = calculate_hash(input_text)
# print(f"Кеш-сумма текста '{input_text}': {hash_sum}")

# input_text2 = "Привет, мир!"
# hash_sum2 = calculate_hash(input_text2)
# print(f"Кеш-сумма текста '{input_text2}': {hash_sum2}")
# print(hash_sum == hash_sum2)
