/*
 * SimpleModal Basic Modal Dialog
 * http://www.ericmmartin.com/projects/simplemodal/
 * http://code.google.com/p/simplemodal/
 *
 * Copyright (c) 2010 Eric Martin - http://ericmmartin.com
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Revision: $Id: basic.js 254 2010-07-23 05:14:44Z emartin24 $
 */

jQuery(function ($) {
	// Load dialog on page load
	//$('#basic-modal-content').modal();

	// Load dialog on click
	$('#basic-modal_1 .basic').click(function (e) {
		$('#basic-modal-content-1').modal();
		return false;
	});

	$('#basic-score-modal .basic').click(function (e) {
		$('#basic-score-modal-content').modal();
		$('#id_score1').val('20');
		$('#id_score2').val('20');
		$('#id_score21').val('40');
		$('#id_score3').val('40');
		$('#id_score31').val('60');
		$('#id_score4').val('60');
		$('#id_score_content_1').val('relatively normal, as-span accounts belong to life.');
		$('#id_score_content_2').val('indicate serious (stress) problems which may threaten the performance.');
		$('#id_score_content_3').val('indicate a serious problem. there is case of (threatening) overvoltage or psychiatric');
		$('#id_score_content_4').val('indicate a serious problem. there is case of (threatening) overvoltage or psychiatric');
		
		
		return false;
	});
	
	$('#basic-ques-modal .basic').click(function (e) {
		$('#basic-ques-modal-content').modal();
		return false;
	});	
	
	$('#sav_treat .basic').click(function (e) {
		
		var value = $("input:radio[name=type_of_answer]:checked").val();
		if (value == 'Text'){
			$('#text').show();
			$('#radio').hide();
			$('#check').hide();
			$('#slider').hide();
		}
		else if (value == 'Radio'){
			$('#text').hide();
			$('#check').hide();
			$('#slider').hide();
			$('#radio').show();
		}
		else if (value == 'Checkbox'){
			$('#text').hide();
			$('#radio').hide();
			$('#slider').hide();
			$('#check').show();
		}
		else if (value == 'Slider'){
			$('#text').hide();
			$('#radio').hide();
			$('#slider').hide();
			$('#check').hide();
			$( "#slider" ).show();
			$( "#slider" ).slider();
		    
		}
		if($('#id_module_name').val()=='1'){
			$('#title').text('Diary Module');
		}
		else if($('#id_module_name').val()=='2'){
			$('#title').text('Food Module');
		}
		else{
			$('#title').text('No Module selected');
		}
		$('#question').text($('#id_questions').val());
		$('#helptext').text($('#id_help_text').val());
		$('#answers').text($('#id_answers').val());
		$('#preview').modal();
		return false;
	});
});