# paper-text-mining

**Paper search, download, parse, segmentation.**

> The project attempts to search, download, parse and segment papers through the website interface (Elsa. API, IEEE Xplore API etc.).  
> Currently only supports **Sciencedirect**.  
> IEEE Xplore will be added in the future.

## Elsevier

### Prerequisites

- An API key from [http://dev.elsevier.com](http://dev.elsevier.com)
- elsapy >= 0.5.0. You can install it by run ```pip install elsapy``` in your command line.

### Configuration

Since accessing Elsevier's API requires API Key ([available here](https://dev.elsevier.com/)), you need to follow the steps to configure it:
- In the folder in which exampleProg.py resides, create a file called 'config.json'
- Open 'config.json' in a file editor, and insert the following:
  ```json
  {
      "apikey": "ENTER_APIKEY_HERE",
      "insttoken": "ENTER_INSTTOKEN_HERE_IF_YOU_HAVE_ONE_ELSE_DELETE"
  }
  ```
- Paste your APIkey in the right place
- If you don't have a valid insttoken (which you would have received from Elsevier support staff), delete the placeholder text. If you enter a dummy value, your API requests will fail.

The '.gitignore' file lists 'config.json' as a file to be ignored when committing elsapy to a GIT repository, which is to prevent your APIkey from being shared with the world. Make similar provisions when you change your configuration setup.