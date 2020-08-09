$(function() {
	  $('#search-text')
		.bind('keydown', function(e){
			if (e.keyCode == 13) {
				$.getJSON($SCRIPT_ROOT + '/_search', {
					text: $(this).val()
				}, function(data) {
					$("#result").append(data.result);
					if(data.result.length > 300){
						var bias_for_desktop = 60/3793;
						var size_for_desktop = data.result.length*bias_for_desktop;
						var em_size_for_desktop = size_for_desktop + 'em';
						
						var bias_for_mobile = 85/3793;
						var size_for_mobile = data.result.length*bias_for_mobile;
						var em_size_for_mobile = size_for_mobile + 'em';

						if($(window).width() <= 1000){
							$("#contents div div .wrap").css('top', em_size_for_mobile);
						}else{
							$("#contents div div .wrap").css('top', em_size_for_desktop);
						}
					}
				});
			
				$.getJSON($SCRIPT_ROOT + '/_collect', {
					text: $(this).val()
				}, function(data) {
					console.log(data.result);
				});
			
			} else{
				$('#result').text("");
				$('#contents div div .wrap').css('top', '50%');
			}
		});
	$('#search')
		.bind('click', function(e){
			$.getJSON($SCRIPT_ROOT + '/_search', {
				text: $('#search-text').val()
			}, function(data) {
				$("#result").append(data.result);
				console.log($(window).width());
				if(data.result.length > 300){
					var bias_for_desktop = 60/3793;
					var size_for_desktop = data.result.length*bias_for_desktop;
					var em_size_for_desktop = size_for_desktop + 'em';
					
					var bias_for_mobile = 85/3793;
					var size_for_mobile = data.result.length*bias_for_mobile;
					var em_size_for_mobile = size_for_mobile + 'em';

					if($(window).width() <= 1000){
						$("#contents div div .wrap").css('top', em_size_for_mobile);
					}else{
						$("#contents div div .wrap").css('top', em_size_for_desktop);
					}
				}
			});
		
			$.getJSON($SCRIPT_ROOT + '/_collect', {
				text: $('#search-text').val()
			}, function(data) {
				console.log(data.result);
			});

			return false;	
		});
});
