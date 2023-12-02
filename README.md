# chainkovsky
chainkovsky is a tiny Python package which helps with pipelining functions.

## Installation
For now, just copy chainkovsky.py into the root directory of your project.

## Overview
To start, just import `chain`:
```python
from chainkovsky import chain 
```

You can pipeline functions either using
```python
chain(func1, func2, func3, ...)
```
or if you're familiar with pipes in other languages like bash
```python
chain() | func1 | func2 | func3 | ...
```

Let's see a basic usage example! Imagine you have a vector (tuple of 3 floats in my case) and you need to calculate it's length (not count of elements!).
```python
vector = (0.4, 3.5, -2.1)
```
The length is calculated by getting the root of the sum of squared vector elements, so without chainkovsky the possible solution would look like something like that
```python
vector_length = sqrt(sum([e**2 for e in vector]))
```
It's pretty straightforward and quite easy to understand, why use chainkovsky? When using too many nested functions to process data, the code gets very difficult to read, write and understand.
chainkovsky aims to provide a simple yet powerful way of pipelining your data through functions, the same example above but in chainkovky is below:
```python
length = chain(lambda e: e**2, sum, sqrt)
vector_length = length(vector)
```
or if you prefer bash pipes:
```python
length = chain(lambda e: e**2) | sum | sqrt
vector_length = length(vector)
```
Quite clear, isn't it? The advantages show themselves even more when we deal with complex data processing.
The case we're gonna discussing is pipelining in machine learning. Let's imagine we have a text-processing model, which
doesn't accept text but it's number representations, so called embeddings.
The code to start with:
```python
tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
model = AutoModel.from_pretrained("cointegrated/rubert-tiny2")

def embed(model_output):
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()

text = "Привет, мир!"
``` 
Witout chainkovsky the process is shown below:
```python
model_output = model(**tokenizer(text, padding=True, truncation=True, return_tensors='pt'))
print(embeddings(model_output))
```
That's kinda complex, huh? Let's see what chainkovsky offers here:
```python
embeddings = chain() | tokenizer(text, padding=True, truncation=True, return_tensors='pt') | model | embed
print(embeddings(text))
```
Wow! I'm sure which code you're gonna prefer
