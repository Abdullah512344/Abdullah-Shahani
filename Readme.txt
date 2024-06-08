The Idea is to designed the DFS System. For Stage 23/3 

Idea: Distributed File system that will be implemented on the master server, Client and master server ill communicate in order to upload / download fil . The master server then saves the data and   distributes it in chunks to the chunks server from here it will retrieve in case of download. 
Communication s an important part of this project that will allow the server to run on different machines.

Completed Task: Client, master and Chunk Servers are implemented . chunk server is open for communication. Master Server is able to allocate chunks to the chunk’s server.


How to build the Project so far, Instructions below:

Open 4 terminals:

One Terminal for Master.py , one for Client .py and 2 for Chunk_server with different port number Localhost
Run Commands as describe in the bin file.

After running of the file , input file to be uploaded will be successfully uploaded on the chunk servers via master server Data file system that will create a file, upload a file , communicate with the chunks_ serevr to be able to distribute the chunks.
The File in DFS list can be viewed in the GUI of the Client and  can be selected to be able to download it from theier. Refresh list will delele all the fiels uploded via DFS. Number of Bytess transferred are viewed as well. Chunks of what sizr has been created are also oart of the funtions. 

Contribution:

Saima Ali MSCS22058: Deliverable 1 which is creating the functions for the proper functioning of the DFS system has been proposed by Saima Ali, work has successfully done. The Connection of the Chunk_server and Master has been in initial stage. Initially the command like prompt has been introduced for understanding and checking of the functions being properly run. I further work on the issue that the file size differs on client side and on master side . master is recieving less bytes from master than expected. i work really hard , tried every method of resolving the issue and finally resolved it by adding the delay and some debugging feautures at client side. created GUI interface for the client.
 
Abdullah Shahani MSCS22053: DFS system on the master end which includes the create file, Communication between chunk and master, uploading and retrieving of the file from and to  chunks server. We both worked on the errors that halted the sucessful running of code. We catter the communication issue, path of uploading and downloading has not been working properly.to counter this issue chunks need to be uploaded successfully, in order to do so , chunks now has been divided into two almost equal size of the toal size of the data. This approach is treid beacause data loss in chunks creation but now i think i can resolve it for infinite chunks as well but i stick to the basic of it as there are only two chunk servers and Sir told us that chunks can be two as well. interface the GUI with functions of the client. Testing an dDebugging of the Code to eradicate errors.

Future Implementations:

Project completed . As, for future reference the chunks sizes and number can be enhanced .  direct communication of th echunks and  clients can be implemented. 


