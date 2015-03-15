# Tournament_Planner
The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

The core of the database schema is the function playerStandings() found inside of tournament.sql. This function returns a list of the players and their win records, sorted by wins. Each row returned contains: id, name, number of wins, and number of matches played.

In order to run the code, please follow the folowing pre-steps taken from the Udacity project details page:

          Install Vagrant, http://vagrantup.com/,  and VirtualBox - https://www.virtualbox.org/
          Clone the fullstack-nanodegree-vm repository - http://github.com/udacity/fullstack-nanodegree-vm
          Launch the Vagrant VM

Inside of the tournament directory create the DB with the following command, 'psql tournament'. When the DB opens up use the following command to import the sql file into it, '\i tournament.sql' 

Run the test script with the following command, 'python tournament-test.py'
