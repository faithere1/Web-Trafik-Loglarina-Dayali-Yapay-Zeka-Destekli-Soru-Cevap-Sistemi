import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import faiss
from transformers import AutoTokenizer, AutoModel
import torch


log_template = '{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status_code} {size}'

ips = ['127.0.0.1', '192.168.1.1', '10.0.0.1', '172.16.0.1']
methods = ['GET', 'POST']
urls = ['/index.html', '/about.html', '/contact.html', '/submit_form', '/products.html']
status_codes = [200, 404, 500]
sizes = [2326, 1024, 532, 182, 854]

start_time = datetime(2024, 8, 10, 13, 55, 36)

def generate_log_lines(num_lines):
    log_data = []
    for i in range(num_lines):
        ip = random.choice(ips)
        method = random.choice(methods)
        url = random.choice(urls)
        status_code = random.choice(status_codes)
        size = random.choice(sizes)
        timestamp = (start_time + timedelta(seconds=i*random.randint(15, 60))).strftime('%d/%b/%Y:%H:%M:%S')
        log_line = log_template.format(ip=ip, timestamp=timestamp, method=method, url=url, status_code=status_code, size=size)
        log_data.append(log_line)
    return log_data

num_lines = 100
log_data = generate_log_lines(num_lines)

                                  #DOSYA YOLU EKLENMELİ
with open("DOSYA YOlU EKLEYİN/web_traffic_large.log", "w") as file:
    file.write("\n".join(log_data))

                                # DOSYA YOLU EKLENMELİ
log_df = pd.read_csv("DOSYA YOLU EKLEYİN/web_traffic_large.log", sep=" ", header=None,
                     names=["IP", "dash1", "dash2", "Timestamp", "Request", "Response_Code", "Size"])
log_df = log_df.drop(columns=["dash1", "dash2"])
log_df['Timestamp'] = pd.to_datetime(log_df['Timestamp'], format='[%d/%b/%Y:%H:%M:%S]')
log_df[['Method', 'URL', 'Protocol']] = log_df['Request'].str.split(' ', expand=True)
log_df = log_df.drop(columns=["Request", "Protocol"])


tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def encode_text(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**inputs)
    return model_output.last_hidden_state[:, 0, :].cpu().numpy()

log_df['URL_vector'] = log_df['URL'].apply(lambda x: encode_text([x])[0])

d = log_df['URL_vector'].iloc[0].shape[0]
index = faiss.IndexFlatL2(d)
vectors = np.stack(log_df['URL_vector'].values)
index.add(vectors)

def search_faiss(query, k=5):
    query_vector = encode_text([query])[0]
    D, I = index.search(np.array([query_vector]), k)
    results = log_df.iloc[I[0]]
    return results


from transformers import T5Tokenizer, T5ForConditionalGeneration

t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

def generate_answer(question, context):
    input_text = f"question: {question} context: {context}"
    inputs = t5_tokenizer(input_text, return_tensors='pt', truncation=True, padding=True)
    outputs = t5_model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_new_tokens=100
    )
    answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def answer_question(question):
    search_results = search_faiss(question)
    if search_results.empty:
        return "Uygun bilgi bulunamadı."
    context = search_results['URL'].iloc[0]
    answer = generate_answer(question, context)
    return answer

def get_most_frequent_ip():
    return log_df['IP'].mode()[0]

def get_page_not_found():
    return log_df[log_df['Response_Code'] == 404]['URL'].mode()[0]

def get_page_with_most_hits():
    return log_df['URL'].mode()[0]

def get_ip_with_most_issues():
    return log_df[log_df['Response_Code'] == 500]['IP'].mode()[0]

def get_most_used_protocol():
    return log_df['Method'].mode()[0]

def answer_question_v2(question):
    question = question.lower()

    if "ip" in question and "en çok" in question:
        answer = get_most_frequent_ip()
    elif "sayfa bulunamadı" in question:
        answer = get_page_not_found()
    elif "sayfa bulunabildi" in question:
        answer = get_page_with_most_hits()
    elif "ip sorun çıkarıyor" in question:
        answer = get_ip_with_most_issues()
    elif "protokol en çok kullanılıyor" in question:
        answer = get_most_used_protocol()
    else:
        answer = "Bu soruya uygun bir yanıt bulunamadı."

    return answer


def main():
    while True:
        user_question = input("Soru girin (çıkmak için 'exit' yazın): ")
        if user_question.lower() == 'exit':
            print("Programdan çıkılıyor.")
            break
        response = answer_question_v2(user_question)
        print(f"Cevap: {response}")


if __name__ == "__main__":
    main()
