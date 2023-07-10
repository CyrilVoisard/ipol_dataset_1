$(document).ready(function () {
	const max = [6, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 6, 6, 6, 6, 6];

	$("#number_subject, #range_subject").on('change input', changeSubjectHandler);

	function changeSubjectHandler() {
		let subject = parseInt(params.subject);
		let subjectsMax = max[subject - 1];
		$("#number_trial, #range_trial").attr({ "max": subjectsMax });
		$("#maxmin-1 > span:nth-child(1)").html("Max: " + subjectsMax);
		if (parseInt(params.trial) >= subjectsMax) $("#number_trial, #range_trial").val(subjectsMax);
		params.trial = $("#range_trial").val();
	}

	$("#number_trial, #range_trial").on('change input', function () {
		let subject = parseInt(params.subject);
		let subjectsMax = max[subject - 1];
		if (parseInt(params.trial) >= subjectsMax) $("#number_trial, #range_trial").val(subjectsMax);
	});
});
