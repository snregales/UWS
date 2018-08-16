Sharlon Regales
Senior Project Proposal 
<h1>Underwater Rugby Logging System</h1>

<h2>Introduction</h2>
<p>For the past year I have become part of a niche sport, Underwater Rugby (UWR). During this time I got the opportunity to travel and compete against multiple states and countries. At the time, i was curious of the technologies they use to document each event. And with each competition I felt like that there are improvements that could be make to advance the sport forward.</p>

<p>UWR is three-dimensional team sport played in a pool with a depth of 3.5-5 meters. The objective of the game is to cooperatively to place a negatively buoyant ball, filled with salt water, in the opposing team's basket.</p>

<h3>A tournament, witch this project will be focused on, is done as follow:</h3> 
<ul>
<li><ul><h4>Tournament</h4>
<li>A tournament can last multiple days, usually two days </li>
<li>A tournament consists of multiple teams</li>
<li>A tournament consists of multiple matches</li>
<li>Opperlevel tournaments have multiple brackets</li></ul></li>
<li><ul><h4>Match</h4>
<li>A match consist of two teams( Black, and White team)</li>
<li>A match lasts 30 min, two halves of 15 min with a halftime of 5 min
Opperlevel tournaments, winner of match moves into winning bracket
Must have four referees, two water, a deck, and a logging ref</li></ul></li>
<li><ul><h4>Team</h4>
<li>A team can have a max of 12 players, excluding the coach</li>
<li>A team can have a max of 6 players in the pool at any time</li></ul></li>
</ul>
<h2>Goal of the Project</h2>
<p>Currently In the tournaments that have participated at, either all data is recorded manually, or logged temporarily during a match and then printed. When the next match is initialize all data of the previous match is lost on the system.</p>

<p>Furthermore, due to this convention, is that a tournament day is split in half in order for the organizers to query and integrate the next matches accordingly based on the winning and losing.</p>

<p>Finally, athlete and coaches don’t know who they will be facing until almost match time making it harder for a team to come with a strategy. In other words there is a lack of communication between organizers/referees and players.
The problem I will try to solve with this project is to log all essential data of the matches in a tournament. And make these data point available to players/athletes/observers.</p>
 
<h2>Plan of Attack</h2>
<p>This project consist of to interaction points, referees logging to the system, and observers looking at the data that was logged. Other than those to endpoints the system will have a data structure to store all essential information.</p>

<h4><i>Interaction points</i></h4>
<p>Both will be a web UI, one where register referees can sign in and record the game. And the other end open publicly to observers. (might have level accessibility for register observers)</p>

<h4><i>Data structure</i></h4>
<p>The structure should execute CRUD commands, and at the same time, not allow authorized users manipulate data points. Quarrying data should have fairly low latency</p>

<h2>Tools And Utilities</h2>
<h4><i>Version Control</i></h4>
<p>I find this to be one of the most important piece to a project. Managing your project is as important as creating it. Multiple before I have wrote code that worked perfectly, but than later stopped working, and would be unable to go back to the previous version that did (last years senior project). Thus i will be using Git along with gitHub to push and pull my repository</p>

<h4><i>Browser</i></h4>
Don’t know if behavior of a web application would differ from browser to browser, but to be safe, development of this project will be focused solely on one browser. With the limited amount of time I have, I opt to out any notion of  multi platform integration. Browser of choice will be Chrome, since it's so widely popular, I can assume that my end user will have it on there system.

<h4><i>Server Side Language</i></h4>
<p>For this I choose Python, the readability of this language is great, since im cut for time rapid deployment is also , integration in the past year, and most of all beautiful documentation it has. Which gets me to my next point framework.</p>

<h4><i>Framework</i></h4>
<p>The framework I plan to use to develop the project is Django. This was suggested by Randy last year after I first learned bottle in server side programing and wanted to us it through my senior project. I decided to do the following Randy’s suggestion and read up on the documentation, which is really nice and understandable. I would like to point out, since reading the documentation, 1.8 LTS last year, the have moved on 4 iterations and will stop extended support for 1.8 in April. The next LTS support is 1.11.9, but they radical changes when they moved to 2.0.1 in December of 2017. So I’m contemplated which Django release to use.</p>
<h4><i>Data Structure</i></h4>
<p>As a default Django uses a SQL database as its data structure, I’m plan to develop the project using MongoDB a NoSQL database. MongoDB is easily deployed, can be scale nicely and uses JSON notation which is simple. Now the django documentation list the possibility of using different data structure instead of the base one (SQLite), but does not list MongoDB among them.  That said, I found on the django community: 
<i>“The official ​MongoDB documentation recommends using ​Djongo which is specifically meant for connecting the original Django ORM (instead of a non-rel flavor) to MongoDB. Using the Django admin app one can add and modify documents in MongoDB. Other contrib modules such as auth and sessions also work without any changes.”</i>
I plan to use this guide documented on this page to implement/port MongoDB to the project.</p>

<h3>Side Notes</h3>
<ul>
<li>It is possible to AJAXfy a django project. So up to this point I don't feel any need for JavaScript, but this can change in the future.</li>
<li>Django framework has a well integrated unit and integration testing, but not to long ago I also stumble upon, Cypress, testing unit for anything that runs in the browser.</li>
<li>This project won't pay attention to design outside of functional design, therefore, I opt to use bootstrap in its base form to model/design the front end sections</li> 
</ul>

