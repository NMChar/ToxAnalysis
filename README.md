# ToxAnalysis
The contains a small project for harvesting public toxicology data and using them to analyze toxicological properties of a molecule

The jupyter notebook (ToxAnalysis.ipynb) should be the entry point as I used its markdown to explain my thinking and demonstrate the tools I built/selected for the analysis I conducted. It should be pretty plug-and-play if you configure a virtual environment using the requirements file.

The trickiest bit will probably be the LLM that gets loaded from HuggingFace (BioGPT-Large). I used it to summarize key findings of harvested literature data -- turn it off if it's giving your computer too much of a headache.

Please make sure you add the .env file I emailed you to the operating directory of the notebook or you won't have your CTX API key!