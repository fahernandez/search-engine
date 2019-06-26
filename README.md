# Search Engine project
Information retrieval search engine project.

# Functions
1. Standardize: Standardize url folders and files
2. Tokenizer: Tokenize information folders.
3. Build dictionary.

## Requirements
1. Install docker.
- [Docker](https://docs.docker.com/engine/installation/) 
2. Install git.
- [Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03)

# How to run the proyect
1. Clone this project.
```
git clone https://github.com/fahernandez/search-engine
```
2. Execute 
```
cd search-engine
docker run -ti -v $PWD/src:/src -v $PWD/../search-engine-data:/data fahernandez/search-engine:latest
```