# RAG fundamentals

Retrieval-Augmented Generation (RAG) is a design pattern that combines information retrieval with text generation. Before a language model writes an answer, the application searches an external knowledge source for information relevant to the user's question and supplies the retrieved information as context.

RAG is useful when an application needs answers informed by private, specialized, or frequently updated information that may not be present in a model's training data. RAG can make answers more relevant and easier to trace to source material, but it does not guarantee correctness. Retrieval can return irrelevant or incomplete passages, and a language model can still misunderstand or misrepresent the supplied context.

A typical RAG workflow has an indexing stage and a question-answering stage. During indexing, source documents are loaded, split into smaller passages called chunks, converted into numerical representations called embeddings, and stored in a searchable index or vector database. Chunking makes large documents easier to search and allows the system to retrieve focused passages.

An embedding is a list of numbers that represents aspects of the meaning of a piece of text. Texts with similar meanings often have embeddings that are close under a similarity measure. A vector database can search these numerical representations to find chunks that are semantically related to a question.

At question time, the user's question is also converted into an embedding. The retriever searches the index and returns the most relevant chunks. The application places those chunks alongside the question in the prompt sent to a language model. This step is often called context injection or context augmentation. The language model then generates a response using the question and retrieved context.

RAG is not the same as fine-tuning. Fine-tuning changes model parameters through additional training. RAG usually leaves the model unchanged and provides relevant external information at inference time. RAG systems need careful document preparation, retrieval evaluation, access control, source freshness, and safeguards against irrelevant or malicious retrieved content.

A practical example is a university support assistant. The university stores policy documents and student guides in an index. When a student asks about the refund deadline, the system retrieves relevant policy passages and provides them to the language model. The model uses those passages to compose an answer and can identify which policy source informed the response.
