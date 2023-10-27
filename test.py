def get_tuples_by_document(document_name, relevant_data):
    tuples_for_document = []

    for word, tuples in relevant_data.items():
        for data_tuple in tuples:
            if document_name in data_tuple:
                tuples_for_document.append(data_tuple)

    return tuples_for_document

# Assuming you have the relevant_data dictionary
document_name = input("Enter the document name (e.g., 'D1'): ")
document_name = document_name.strip()  # Remove any leading/trailing spaces

if document_name in relevant_data:
    tuples_for_document = get_tuples_by_document(document_name, relevant_data)

    # Now, tuples_for_document contains all the tuples associated with the input document name
    for data_tuple in tuples_for_document:
        print(data_tuple)
else:
    print(f"Document '{document_name}' not found in relevant_data.")
