from healthcareapp.rag import search_knowledge


result = search_knowledge(
    "What are symptoms of heart disease?",
    domain="medical"
)


for doc in result:

    print("--------------------------------")
    print(doc.page_content)