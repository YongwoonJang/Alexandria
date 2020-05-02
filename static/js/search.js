$(function() {
	  $('#search-text')
		.bind('keyup', function(e){
			if (e.keyCode == 13) {
				$.getJSON($SCRIPT_ROOT + '/_search', {
					text: $(this).val()
				}, function(data) {
					console.log($SCRIPT_ROOT);
					console.log(data.result);
					$("#result").text(data.result);
				});
			
				$.getJSON($SCRIPT_ROOT + '/_collect', {
					text: $(this).val()
				}, function(data) {
					console.log(data.result);
				});

				return false;	
			} else{
			//	$('#result').text("  작성중...");
			}
		});
	$('#search')
		.bind('click', function(e){
				$.getJSON($SCRIPT_ROOT + '/_search', {
					text: $(this).val()
				}, function(data) {
					console.log($SCRIPT_ROOT);
					console.log(data.result);
					$("#result").text(data.result);
				});
				
				$.getJSON($SCRIPT_ROOT + '/_collect', {
					text: $(this).val()
				}, function(data) {
					console.log(data.result);
				});
				return false;	
		});
});
