var cur_plot = 0;
var plot_data;

var times, values;

$(function() {
  $('a#requestTS').bind('click', function() {
  	d3.select("#error").text('');
	d3.select("#plotsvg").remove();
	d3.select("#result_table").remove();
    $.ajax({
	type: 'GET',
	url: '/meta/'+$('input[name="Index"]').val(),
    success: function(data) {
		meta = data.result[1][0];
		metatitle = "<h3>Meta Data</h3><br><br>"
		var metacontent = "<table id='result_table'> <tr id='first'> <th>Index</th> <th>ID</th><th>Blarg</th><th>Level</th><th>Mean</th><th>St. Dev.</th></tr>"
		metacontent += '<tr><td>' +  meta[0] + '</td><td>' + meta[1] + '</td><td>' + meta[2] + '</td><td>' + meta[3] + '</td><td>' + meta[4] + '</td><td>' + meta[5] + '</td></tr>';
		metacontent += "</table>";
		$("#tss").append(metatitle);
		$("#tss").append(metacontent);
		
		times = data.result[2]
		values = data.result[3]
		tstitle = "<br><br><h3>TimeSeries</h3>"
		
		var tscontent = "<table id='result_table2'> <tr id='first'> <th>Time</th> <th>Value</th></tr>"
		for(i=0; i<times.length; i++){
		    tscontent += '<tr><td>' +  times[i] + '</td><td>' + values[i] + '</td></tr>';
		}
		$("#tss2").append(tstitle);
		$("#tss2").append(tscontent);
		
    },
    error: function(xhr, status, error){
    	console.log(xhr.responseText);	
		var response = $.parseJSON(xhr.responseText);
    	$("#error").text(response);
    }
	});
    return false;
  addRowHandlers();
  });
});

$(function() {
  $('a#requestAll').bind('click', function() {
  	d3.select("#error").text('');
	d3.select("#result_table").remove();
    $.ajax({
	type: 'GET',
	url: '/meta/',
    success: function(data) {
		res = data.result[1];
		var content = "<table id='result_table'> <tr id='first'> <th>Index</th> <th>ID</th><th>Blarg</th><th>Level</th><th>Mean</th><th>St. Dev.</th></tr>"
		for(i=0; i<res.length; i++){
		    content += '<tr><td>' +  res[i][0] + '</td><td>' + res[i][1] + '</td><td>' + res[i][2] + '</td><td>' + res[i][3] + '</td><td>' + res[i][4] + '</td><td>' + res[i][5] + '</td></tr>';
		}
		content += "</table>";
		$("#tss").append(content);
    },
    error: function(xhr, status, error){
    	var response = $.parseJSON(xhr.responseText);
    	$("#error").text(response.message);
    }
	});
    return false;
  });
});

$(function() {
  $('a#requestFilter').bind('click', function() {
  	d3.select("#error").text('');
	d3.select("#result_table").remove();
    $.ajax({
	type: 'GET',
	url: '/meta/filter',
	data: {
      levels: $('input[name="levels"]').val(),
      mean_range: $('input[name="mean_range"]').val(),
      std_range: $('input[name="std_range"]').val()
    },
    success: function(data) {
		res = data.result[1];
		var content = "<table id='result_table'> <tr id='first'> <th>Index</th> <th>ID</th><th>Blarg</th><th>Level</th><th>Mean</th><th>St. Dev.</th></tr>"
		for(i=0; i<res.length; i++){
		    content += '<tr><td>' +  res[i][0] + '</td><td>' + res[i][1] + '</td><td>' + res[i][2] + '</td><td>' + res[i][3] + '</td><td>' + res[i][4] + '</td><td>' + res[i][5] + '</td></tr>';
		}
		content += "</table>";
		$("#tss").append(content);
    },
    error: function(xhr, status, error){
    	var response = $.parseJSON(xhr.responseText);
    	console.log(response.message);
    	$("#error").text(response.message);
    }
	});
    return false;
  addRowHandlers();
  });
});

$(function() {
    $('#submit_upload').click(function() {
		d3.select("#error").text('');
		d3.select("#result_table").remove();
        event.preventDefault();
        var form_data = new FormData($('#postts')[0]);
        $.ajax({
            type: 'POST',
            url: '/meta/',
            data: form_data,
            processData: false,
            contentType: false,
            success: function(data) {
				meta = data.result[1][0];
				metatitle = "<h3>Meta Data</h3><br><br>"
				var metacontent = "<table id='result_table'> <tr id='first'> <th>Index</th> <th>ID</th><th>Blarg</th><th>Level</th><th>Mean</th><th>St. Dev.</th></tr>"
				metacontent += '<tr><td>' +  meta[0] + '</td><td>' + meta[1] + '</td><td>' + meta[2] + '</td><td>' + meta[3] + '</td><td>' + meta[4] + '</td><td>' + meta[5] + '</td></tr>';
				metacontent += "</table>";
				$("#tss").append(metatitle);
				$("#tss").append(metacontent);
		
				times = data.result[2]
				values = data.result[3]
				tstitle = "<br><br><h3>TimeSeries</h3>"
		
				var tscontent = "<table id='result_table2'> <tr id='first'> <th>Time</th> <th>Value</th></tr>"
				for(i=0; i<times.length; i++){
				    tscontent += '<tr><td>' +  times[i] + '</td><td>' + values[i] + '</td></tr>';
				}
				$("#tss2").append(tstitle);
				$("#tss2").append(tscontent);
    },
    error: function(xhr, status, error){
    	var response = $.parseJSON(xhr.responseText);
    	console.log(response.message);
    	$("#error").text(response.message);
    }
	});
    return false;
  	addRowHandlers();
        });
}); 

i_array = []

function reset_chart() {
	d3.select("#plotsvg").remove();
	svg = initPlot(times, values);
	addRowHandlers(svg);
}

function addRowHandlers(svg) {
	i_array = []
    var table = document.getElementById("result_table");
    var rows = table.getElementsByTagName("tr");
    for (i = 1; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = 
            function(row) 
            {
                return function() { 
                                        var cell = row.getElementsByTagName("td")[0];
                                        var id = cell.innerHTML;
                                        i = id;
										i_array.push(i)
										LoadData(svg);
                                 };
            };

        currentRow.onclick = createClickHandler(currentRow);
    }
}

var margin = {top: 40, right: 40, bottom: 60, left: 60};

var width = 670 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;
		
var x = d3.scale.linear()
	.domain([0,.99])
	.range([0, width]);

var y = d3.scale.linear()
	.domain([-0.2,3.2])
	.range([height, 0]);

var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left");

var xAxis = d3.svg.axis()
	.scale(x)
	.orient("bottom");

				
function initPlot(times, values){
	
	var svg = d3.select("#chart-area").append("svg")
			.attr("id","plotsvg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
			
	var yAxisGroup = svg.append("g")
		.attr("class", "y-axis axis");

	var xAxisGroup = svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.attr("class", "x-axis axis");

	svg.append("text")
		.attr("text-anchor", "middle")
		.attr("transform", "translate(-35,220)rotate(-90)")
		.text("TS Value");
		
	svg.append("text")
		.attr("text-anchor", "middle")
		.attr("transform", "translate(280,435)")
		.text("Time");

	var xlabel = svg.append("text");	
	
	resultarray = toObject(times, values)
	
	pathline = d3.svg.line()
		.interpolate("linear")
		.x(function(d) {return x(d.time)})
		.y(function(d) {return y(d.value)});
		
	svg.select(".y-axis")
		.transition().duration(800)
		.call(yAxis);
	svg.select(".x-axis")
		.transition().duration(800)
		.call(xAxis);
					
	svg.append("path")
		.attr("class","firstline")
		.attr("d",pathline(resultarray))
		
	return svg
}

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

$("#first").remove()

function LoadData(svg){
	console.log('hi')
	result_arrays = []
	i_array.forEach(function(i){
		plot_data.forEach(function(d){
			if(d[1] == i){
				values2 = d[2].values
				times2 = d[2].times
				resultarray = toObject(times2, values2);
				result_arrays.push(resultarray)
			}
		})	
	})
	console.log(result_arrays)
			
	pathline = d3.svg.line()
		.interpolate("linear")
		.x(function(d) {return x(d.time)})
		.y(function(d) {return y(d.value)});
			
	result_arrays.forEach(function(d){
		svg.append("path")
			.attr("class","line")
			.attr("d",pathline(d))
		
	})

}
