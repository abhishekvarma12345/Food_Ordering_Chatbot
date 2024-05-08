# Food Ordering Chatbot with Open Source LLM (Meta Llama3)

Requirements:
- RAM of atleat 16GB.
- Mid range CPU will suffice.

1. Download Ollama setup from: [Ollama](https://ollama.com/library/llama3)
2. Run `ollama run llama3` command to pull the model from ollama models repository.
3. create two custom models by using `Modelfile` and `Modelfile1`.
```bash
ollama create foodorderbot -f ./Modelfile
ollama create endoforder -f ./Modelfile1
```
4. Create new conda environment with python 3.8 and install requirements

```bash
conda create -n orderbot python=3.8 -y
conda/source activate orderbot
```

5. Run the command `streamlit run app.py`



