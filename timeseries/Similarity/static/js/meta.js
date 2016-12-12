

var cur_plot = 0;
var plot_data;

var times, values;

$(function() {
  $('a#requestTS').bind('click', function() {
	d3.select("#plotsvg").remove();
	d3.select("#result_table").remove();
    $.getJSON("/search_index/results", {
      id: $('input[name="Index"]').val(),
      n: $('input[name="Number"]').val()
    }, function(data) {
		var content = "<table id='result_table'> <tr id='first'> <th>TS</th> <th>"+$('input[name="Index"]').val()+"</th><th></th></tr>";
		content += '<tr><td>Mean: </td><td>' + data.result[0] + '</td></tr>';
		content += '<tr><td>St. Deviation: </td><td>' + data.result[1] + '</td></tr>';
		content += '<tr><td>Levels: </td><td>' + data.result[2] + '</td></tr>';
		content += "</table>";
		console.log(typeof data.result);
		console.log(data.result);
		times = data.result[0][2]['times'];
		values = data.result[0][2]['values'];
		//svg = initPlot(times, values);
      $("#tss").append(content);
	  //addRowHandlers(svg);
	  //plot_data = data.result;
    });
    return false;
  });
});



function toObject(times, values) {
    var resultarray = []
	var result = {};
    for (var i = 0; i < values.length; i++) {
		 result = {}
		 result.time = times[i]
		 result.value = values[i];
    	 resultarray.push(result);
	}
	return resultarray
}
