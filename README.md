Names: 
- Abdulmajed Al Chekha: aboabdo@csu.fullerton.edu
- Juli Nazzario: jnazzario@csu.fullerton.edu
-
-
-
Language used: Python

## To run the program:
The server is invoked as: `python server.py`<br>
    The server is set to be at port nummber 1234 always.

The ftp client is invoked as: `python client.py <server machine> <server port>`
- For example: `python client.py localhost 1234`
 - server machine is the domain name of the server (localhost).
 - server port is the port number of the server (1234)
    
Upon connecting to the server, the client prints out ftp>, which allows the user to execute the following commands:  
- `ftp> get <filename> (downloads file <file name> from the server)`
- `ftp> put <filename> (uploads file <file name> to the server)`
- `ftp> ls (lists all files located on the server)`
- `ftp> quit (disconnects from the server and exits)`
