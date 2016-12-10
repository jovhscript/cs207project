

var i = 0;

$(function() {
  $('a#requestTS').bind('click', function() {
    $.getJSON("/search_index/results", {
      id: $('input[name="Index"]').val(),
      n: $('input[name="Number"]').val()
    }, function(data) {
		console.log(data.result);
		var content = "<table id='result_table'> <tr id='first'> <th>Index</th> <th>Distance</th><th></th></tr>"
		for(i=0; i<data.result.length; i++){
		    content += '<tr onclick="ChangeColor(this);"><td>' +  data.result[i][1] + '</td><td>' + data.result[i][0] + '</td><td><button onclick="LoadData()">Plot</button></td></tr>';
		}
		content += "</table>"
		
		
      $("#tss").append(content);
	  addRowHandlers();
	  console.log(data.result)
    });
    return false;
  });
});

function addRowHandlers() {
    var table = document.getElementById("result_table");
    var rows = table.getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = 
            function(row) 
            {
                return function() { 
                                        var cell = row.getElementsByTagName("td")[0];
                                        var id = cell.innerHTML;
                                        i = id;
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
		
var x = d3.scale.ordinal()
	.domain([1,100])
	.rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
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

svg.append("text")
	.attr("text-anchor", "middle")
	.attr("transform", "translate(390,435)")
	.text("Time");

var xlabel = svg.append("text");

function LoadData(){
	
	console.log(i)
}
