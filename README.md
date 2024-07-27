## Roko Query

This naptha module answers user queries, leveraging a database of information from Roko's social media channels. 

### Prerequisites

To run this naptha module you need to first upload the vector database with the RAG data.

Note initial scripts to create the chroma vector db are in the `data-extractors` directory.

### Run

Once a chroma db with a "roko-telegram" collection has been created it can be zipped up and uploaded to a naptha node with:

```
naptha write_storage -i chromadb.zip
```

The returned id is used as the `input_dir` when running the node. For example:
```
naptha run roko_query -p "query='' input_dir='<id>'
```






