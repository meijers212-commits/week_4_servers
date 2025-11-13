import json
from curses.ascii import isalpha

from fastapi import FastAPI, HTTPException, Body
import uvicorn
from pydantic import BaseModel

app = FastAPI()


def lode_data(file_name):
    try:
        with open(f"{file_name}.json","r",encoding="utf-8") as json_file:
            return json.load(json_file)

    except FileNotFoundError:
        with open(f"{file_name}.json","w",encoding="utf-8") as json_file:
            return json.load(json_file)

def save_data(data,file_name):
    with open(f"{file_name}","w",encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def update_data(data, fil_name):
    json_data = lode_data(fil_name)
    json_data.append(data)
    with open("data.json","w",encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)


@app.get("/test/")
def root():
    return {"msg": "hi from test"}

@app.get("/test/{name}")
def root(name):
    data = lode_data("names.txt")
    data.append(name)
    save_data(data,name)
    return f"msg:saved user{name}"

class Caesar(BaseModel):
    text: str
    offset: int
    mode: str

@app.post("/caesar")
def caesar_endpoint(caesar: Caesar):
    alfa = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",]
    text = caesar.text
    offset = caesar.offset
    mode = caesar.mode
    text = text.lower()
    result = ""
    if mode == "encrypt":
        for ch in text:
            if not ch.isalpha():
                result += ch
                continue
            new_index = (alfa.index(ch) + offset) % 26
            result += alfa[new_index]
        return {"encrypt_text": result}

    elif mode == "decrypt":
        for ch in text:
            if not ch.isalpha():
                result += ch
                continue
            new_index = (alfa.index(ch) - offset) % 26
            result += alfa[new_index]
        return {"decrypt_text": result}

    else:
        return "mode must be 'encrypt' or 'decrypt'"

@app.get("/fence/encrypt")
def crypt_fence_cipher_endpoints(text: str):
    decrypted_text = text.lower()
    decrypted_text = decrypted_text.replace(" ","")
    even = ""
    odd = ""
    for idx,ch in enumerate(decrypted_text):
        if  idx % 2 == 0:
            even += ch
        else:
            odd += ch
    return {"encrypted_tex": even + odd}

@app.post("/fence/decrypt")
def decrypt_fence_cipher_endpoints(encrypted_text: str):
    half = len(encrypted_text) // 2
    even = encrypted_text[:half]
    odd = encrypted_text[half:]
    result = ""
    i = 0
    while i < half:
        result += even[i]
        if i < len(odd):
            result += odd[i]
        i += 1
    if len(encrypted_text) % 2 != 0:
        result += odd[-1]
    return {"decrypted_text": result}




if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)









