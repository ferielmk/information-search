import nltk
import math
from collections import defaultdict

def load_documents():
    
    directory_path = "./"
    file_list = ["/d1.txt", "/d2.txt", "/d3.txt", "/d4.txt","/d5.txt","/d6.txt"]
    document_data = {}

    for idx, filename in enumerate(file_list, 1):       
        file = open(directory_path + filename)
        file_content = file.read()
        file.close()
        document_data[f'D{idx}'] = file_content
    return document_data

print(load_documents())

def preprocess_data(document_data,tokenise,normalise):
    processed_data = {}
    for doc_id, content in document_data.items():
        # Tokenization
        if (tokenise=="Split"):
            tokens=content.split()
        else:
            ExpReg = nltk.RegexpTokenizer('(?:[A-Z]\.)+|\d+(?:\.\d+)?DA?|\w+|\.{3}')
            tokens = ExpReg.tokenize(content)
        # Remove stopwords
        motsvides = nltk.corpus.stopwords.words('english')
        tokens_without_stopw = [token for token in tokens if token.lower() not in motsvides]

        # Stemming using the Lancaster stemmer
        if (normalise=="Lancaster"):
            Lancaster = nltk.LancasterStemmer()
            termes_normalization = [Lancaster.stem(terme) for terme in tokens_without_stopw]
        else:
            Porter = nltk.PorterStemmer()
            termes_normalization = [Porter.stem(terme) for terme in tokens_without_stopw]

        processed_data[doc_id] = termes_normalization

    return processed_data
def calculate_term_frequencies(processed_data):
    term_frequencies = {}
    for doc_id, terms in processed_data.items():
        term_frequencies[doc_id] = defaultdict(int)
        for term in terms:
            term_frequencies[doc_id][term] += 1

    return term_frequencies

def calculate_term_weights(term_frequencies, processed_data, num_documents):
    term_weights = {}
    for doc_id, terms in processed_data.items():
        max_term_freq = max(term_frequencies[doc_id].values())
        term_weights[doc_id] = {}
        for term, freq in term_frequencies[doc_id].items():
            term_weights[doc_id][term] = (freq / max_term_freq) * math.log(num_documents / (1 + sum(1 for d in processed_data if term in processed_data[d])))

    return term_weights

def create_inverted_index(processed_data):
    inverted_index = defaultdict(list)
    term_frequencies = calculate_term_frequencies(processed_data)

    for doc_id, terms in processed_data.items():
        for term in terms:
            inverted_index[term].append(doc_id)

    return inverted_index, term_frequencies

def descriptorfile(processed_data, term_weights):
    all_descriptors = []
    for doc_id, terms in processed_data.items():
        for term in terms:
            frequency = term_weights[doc_id][term]
            all_descriptors.append(f"{doc_id}: {term} - Frequency: {term_frequencies[doc_id][term]} - Weight: {frequency}")

    return all_descriptors

def save_to_file(filename, data):
    with open(filename, "w") as text_file:
        for line in data:
            text_file.write(f"{line}\n")


document_data=load_documents()
processed_data = preprocess_data(document_data,"Split","Lancaster")
num_documents = len(document_data)
term_frequencies = calculate_term_frequencies(processed_data)
term_weights = calculate_term_weights(term_frequencies, processed_data, num_documents)
"""
inverted_index, term_frequencies = create_inverted_index(processed_data)
all_descriptors = descriptorfile(processed_data, term_weights)

# Save the inverted index and descriptors to files
with open("inverted_index.txt", "w") as text_file:
    for term, doc_list in inverted_index.items():
        text_file.write(f"{term}:\n")
        for doc_id in doc_list:
            term_freq = term_frequencies.get(doc_id, {}).get(term, 0)
            term_weight = term_weights.get(doc_id, {}).get(term, 0.0)
            text_file.write(f"  {doc_id}: Frequency: {term_freq} - Weight: {term_weight}\n")

"""
# Now you have saved both the inverted index and descriptors in separate files.
def descriptor(processed_data, term_weights, term_frequencies):
    all_descriptors = []
    for doc_id, terms in processed_data.items():
        for term in terms:
            frequency = term_weights[doc_id][term]
            doc_term_tuple = (doc_id, term, term_frequencies[doc_id][term], frequency)
            all_descriptors.append(doc_term_tuple)

    return all_descriptors

def inverted_index(processed_data, term_frequencies, term_weights):
    inverted_index = defaultdict(list)

    for doc_id, terms in processed_data.items():
        for term in terms:
            term_freq = term_frequencies.get(doc_id, {}).get(term, 0)
            term_weight = term_weights.get(doc_id, {}).get(term, 0.0)
            term_doc_tuple = (term, doc_id, term_freq, term_weight)
            inverted_index[term].append(term_doc_tuple)

    return inverted_index
desc=descriptor(processed_data, term_weights, term_frequencies)
inv=inverted_index(processed_data, term_frequencies, term_weights)
print(desc)
print(inv)