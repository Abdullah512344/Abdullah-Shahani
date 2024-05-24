The Idea  is to designed the DFS System. For Stage 2/3 
Idea: Distributed File system that will be implemented on the master server, Client and master server ill communicate in order to upload / download file . The master server then save the data and   distributes it in chunks to the chunks server from here it will retrieve in case of download. 
Communication s an important part of this project that will allow the server to run on different machines.
Completed Task : Client , master and Chunk Servers are implemented . chunk server is open for communication. Master Server is able to allocate chunks to the chunks server.
How to build the Project so far, Instructions below:
Open 4 terminals :
One Terminal for Master.py , one for Client .py and 2 for Chunk_server with different port number Localhost
Run Commands as describe in the bin file.
After runninf of the file , inout file to be uploaded will be successfully uploaded on the chunk servers via master server Data file system that will create a file, upload a file , commnuicate witht he chunks_ serevr to be able to distribute the chunks.
In this deliverable , We have implement ed the successful communication between Client  and master as well as the Master and Chunk server.
The uploading file and  downloading file are in place.
Contribution:
Saima Ali MSCS22058 : Deliverable 1 which is creating the functions for the proper functioning of the DFS system ahs been proposed by Saima Ali, work has successfully done. The Connection of the Chunk_server and Master has been in intial stage. Intially the command like prompt has been introduced for undersatnading and checking of the functions being properly run. 
Abdullah Shahani MSCS22053: DFS system on the m,aster end  which includes the create file, Communication betwen chunk and master, uploading and retrieving of the file from and to  chunks server. We both worked on the errors that halted the sucessful running of code. We catter the communication issue, path of uploading and downloading has not been working properly.

Future Implementations:
There are few  glitches that can be better. Our focu would be ont he GUI end of the Client that will connect the  running oif the Function irrepsective of the running the commands. SEcondly , we a re confident that the file  can be commnuivate via IP address and Port number using the socket that we have been using. We will  work further on that. That concludes our project just in time.

 
