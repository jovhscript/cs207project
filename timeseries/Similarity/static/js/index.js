

var cur_plot = 0;
var plot_data;

$(function() {
  $('a#requestTS').bind('click', function() {
    $.getJSON("/search_index/results", {
      id: $('input[name="Index"]').val(),
      n: $('input[name="Number"]').val()
    }, function(data) {
		var content = "<table id='result_table'> <tr id='first'> <th>Index</th> <th>Distance</th><th></th></tr>"
		for(i=0; i<data.result.length; i++){
		    content += '<tr><td>' +  data.result[i][1] + '</td><td>' + data.result[i][0] + '</td><td><button onclick="">Plot</button></td></tr>';
		}
		content += "</table>"
		cur_plot=+data.result[0][1].substr(data.result[0][1].length - 1);
		console.log(data.result);
		var times = data.result[0][2].times
		var values = data.result[0][2].values
		initPlot(times, values);
      $("#tss").append(content);
	  addRowHandlers();
	  plot_data = data.result;
    });
    return false;
  addRowHandlers();
  });
  
});

i_array = []

function addRowHandlers() {
    var table = document.getElementById("result_table");
    var rows = table.getElementsByTagName("tr");
    for (i = 2; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = 
            function(row) 
            {
                return function() { 
                                        var cell = row.getElementsByTagName("td")[0];
                                        var id = cell.innerHTML;
                                        i = id;
										i_array.push(i)
										LoadData();
                                 };
            };

        currentRow.onclick = createClickHandler(currentRow);
    }
}

var margin = {top: 40, right: 40, bottom: 60, left: 60};

var width = 670 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;

var svg = d3.select("#chart-area").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		
var x = d3.scale.linear()
	.domain([0,.99])
	.range([0, width]);

var y = d3.scale.linear()
	.domain([-0.2,3.2])
	.range([height, 0]);

var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left");

var yAxisGroup = svg.append("g")
	.attr("class", "y-axis axis");

var xAxis = d3.svg.axis()
	.scale(x)
	.orient("bottom");

var xAxisGroup = svg.append("g")
	.attr("transform", "translate(0," + height + ")")
	.attr("class", "x-axis axis");
				
function initPlot(times, values){

	svg.append("text")
		.attr("text-anchor", "middle")
		.attr("transform", "translate(390,435)")
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

function LoadData(){
	
	result_arrays = []
	i_array.forEach(function(i){
		plot_data.forEach(function(d){
			if(d[1] == i){
				values = d[2].values
				times = d[2].times
				resultarray = toObject(times, values);
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
	/*var path2 = svg.selectAll(".line")
		.data(resultarray);
	path2.enter().append("path")
		.attr("class","line");	
	path2.transition()
		.duration(800)
		.attr("d",pathline(resultarray));
		
	path2.exit()
		.transition()
		.duration(800)
		.style('fill-opacity', 1e-6)
		.remove();*/
				
	/*var circle = svg.selectAll("circle")
		.data(resultarray);
	circle.enter().append("circle").attr("fill", "steelblue");
	circle.transition().duration(800)
		.attr("r",2.5)
		.attr("cx", function(d) { return x(d.time); })
		.attr("cy", function(d) { return y(d.value)});
				
	circle.exit().transition().duration(800).remove();*/

}
