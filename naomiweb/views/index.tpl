% include('header.tpl', title='NetDIMM Loader')

<div class="container">
	% include('navbar.tpl', activePage='games')
	
	% if defined('games'):
	<div class="row">
	% for game in games:
		<div class="row">
			<div class="row">
	           	<span class="label label-default">{{round(game.size/float(1024*1024), 1)}} MB</span>
	           	{{game.name[region]}}
	    	</div>
	    	<div class="row">
        		<a href="load/{{game.__hash__()}}">
	          		<img src={{game.screenshot}} class="img-thumbnail" >
	        	</a>
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
