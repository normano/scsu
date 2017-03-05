# scsu
An implementation of the
[Standard Compression Scheme for Unicode](https://en.wikipedia.org/wiki/Standard_Compression_Scheme_for_Unicode) in
Python 3.

## Encoding comparisons

A file called **test.py** is included in the project to compare the encoding of several pieces of text. Languages are
chosen based on the number of people who speak it.

|            | UTF-8 | UTF-16 | UTF-32 | GB18030 | SCSU |
|:----------:|------:|-------:|-------:|--------:|-----:|
|  Mandarin  |    57 |     38 |     76 |      38 |   39 |
|   Spanish  |   244 |    468 |    936 |     246 |  234 |
|   English  |   156 |    312 |    624 |     156 |  156 |
|    Hindi   |   332 |    252 |    504 |     435 |  127 |
|   Arabic   |   261 |    284 |    568 |     499 |  143 |
| Portuguese |   145 |    286 |    572 |     147 |  143 |
|   Bengali  |   137 |     98 |    196 |     181 |   52 |
|   Russian  |   188 |    200 |    400 |     189 |  103 |
|  Japanese  |   132 |     88 |    176 |      88 |   80 |
|   Punjabi  |   307 |    234 |    468 |     402 |  120 |

Numbers are the length of the encoded string, in bytes. Byte signatures are not included.

## TODO

* I only wrote an encoder. A decoder needs to be written.
* The classes don't use the standard Python codec library.