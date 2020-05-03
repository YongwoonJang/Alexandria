$(function() {
	  $('#search-text')
		.bind('keyup', function(e){
			if (e.keyCode == 13) {
				$.getJSON($SCRIPT_ROOT + '/_search', {
					text: $(this).val()
				}, function(data) {
					$("#result").text(data.result);
				});
			
				$.getJSON($SCRIPT_ROOT + '/_collect', {
					text: $(this).val()
				}, function(data) {
					console.log(data.result);
				});

				return false;	
			} else{
				$('#result').text("");
			}
		});
	$('#search')
		.bind('click', function(e){
				$.getJSON($SCRIPT_ROOT + '/_search', {
					text: $('#search-text').val()
				}, function(data) {
					$("#result").text(data.result);
				});
				
				$.getJSON($SCRIPT_ROOT + '/_collect', {
					text: $('#search-text').val()
				}, function(data) {
					console.log(data.result);
				});
				return false;	
		});
});
