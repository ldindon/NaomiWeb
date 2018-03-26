/* TODO check why event does not work
var source = new EventSource("/status");
source.onmessage = function(event)
{
	var json = $.parseJSON(event.data);
	$("#status").html(json.message);
	console.log(json.message)
};*/

setInterval(function() {
	$.ajax
	({
		url: '/status',
		type: 'get',
		success: function(result)
		{
			var json = $.parseJSON(result)
			$('#status').html("<div class=\"row\"><span class=\"label label-default\">" + json.message + "</span></div>");
		}
	});
}, 1000);