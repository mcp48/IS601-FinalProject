# IS 601 Final Project
The goal of this project is to create a flask application that is based on the tutorial found at https://hackersandslackers.com/your-first-flask-application.  The scope and data for the project is based on an earlier project, found on my GitHub at https://github.com/mcp48/IS601-Project3.  The data from that project was modified to follow with the instructions in the tutorial mentioned in the above link.
<br>
<br>
Also, a note to the professor and TA's.  Rather than just modify my current project, I found it easier to create a new project from scratch, and copy and paste the original code from project 3 to start off, then modify that from there.  Before creating any new branches, all the commits and code I pasted in from project 3 was in the master branch.
<br>
<br>
I did it this way because I did not realize that when pushing changes to GitHub from PyCharm, it only pushes the current branch, and no branches prior to that.
<br>
<br>

## To run the project using the command line:
These are instructions on how to run the project:

1. Clone the GitHub repo located [here](https://github.com/mcp48/IS601-FinalProject) to a directory on your local machine, preferably a new directory.
2. Change into the directory that you just created the project in, using the command line
3. Run the command "docker-compose build" without the quotation marks.  Wait until the services finish building; it shouldn't take longer than a couple minutes.
4. Once the build is done, run the command "docker-compose up" to bring up the services.  Again, this should take about a minute.
5. Open a browser, and go to localhost:5000.  This will open the project, and you will be able to view it.  Note that in order to edit, add or delete records, you will need to be logged in.  Create an account at the top of the page, and then log in. 
6. When you are done, run "docker-compose down".  This will stop all the containers and remove the images.  Note that you may have to hit "Ctrl + C" on the keyboard in order to type anything on the command line.  Alternatively, you could open a new window or tab in the command line, or another CLI interface of your choice.  Personally, I use Windows Terminal, but there is also Terminal if you are using a Mac, or Windows PowerShell if you are on Windows.

This project is licensed under the GitHub MIT License.  See the license file, located [here](https://github.com/mcp48/IS601-FinalProject/blob/master/LICENSE) file for the full context of the license.