% include('header.tpl', title='NetDIMM Loader')

<div class="container">
	% include('navbar.tpl', activePage='games')
	
	% if defined('games'):
	<div class="row">
	% for game in games:
		<div class="row">
			<div class="row">
				% if game.isAtomiswave:
	           	<img src=./static/images/atomiswave.png class="img-thumbnail">
	           	% else:
	           	<img src=./static/images/naomi.png class="img-thumbnail">
	           	% end
		    	<span class="label label-default">{{round(game.size/float(1024*1024), 1)}} MB</span>
	    	    <span class="label label-default">{{game.name[region]}}</span>
	    	</div>
	    	<div class="row">
	    		% for screenshot in game.screenshots:
        		<a href="load/{{game.__hash__()}}">
	          		<img src={{screenshot}} class="img-thumbnail" >
	        	</a>
	        	% end
	        </div>
        </div>
	% end
	</div>
	% end

	% if not defined('games'):
	<div class="alert alert-danger"><span class="glyphicon glyphicon-warning-sign"></span> No games were found! Verify that the directory set on the configuration screen exists and contains valid NAOMI games.</div>
	% end

</div>

% include('footer.tpl')
