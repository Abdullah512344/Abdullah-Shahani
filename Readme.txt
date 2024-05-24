The Idea  is to designed the DFS System. For Stage 1/3 
Idea: Distributed File system that will be implemented on the master server, Client and master server ill communicate in order to upload / download file . The master server then save the data and   distributes it in chunks to the chunks server from here it will retrieve in case of download. 
Communication s an important part of this project that will allow the server to run on different machines.
Completed Task : Client , master and Chunk Servers are implemented . chunk server is open for communication. Master Server is able to allocate chunks to the chunks server.
How to build the Project so far, Instructions below:
Open 3 terminals :
run master.py using command python3 master.py
then run chunk_server.py in another terminal using command python3 chunk_server.py 8080( port number)
and lastly run Client.py in another terminal using command python3 client.py

answer the input terminals to upload the  file and to allocate the chunks.
Future Implementations:
DFS Metadata will be allocated , the functions has to be made.
Communications for the Master  Client and  chunk server.
Chunk functionalities of replication and retrieve data.
GUI for the Client master interaction.

 