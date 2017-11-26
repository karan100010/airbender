

function getSiPm25(pm25){
	//console.log("PM25: "+pm25)
	if(pm25<=30){
		return pm25*50/30
	}
	else if(pm25>30 && pm25<=60){
		return 50+(pm25-30)*50/30;
	}
	else if(pm25>60 && pm25<=90){
		return 100+(pm25-60)*100/30;
	}				
	else if(pm25>90 && pm25<=120){
		return 200+(pm25-90)*(100/30);
	}
	else if(pm25>120 && pm25<=250){
		return 300+(pm25-120)*(100/130);
	}
	else if(pm25>250){
		return 400+(pm25-250)*(100/130);
	}

}
function getSiPm10(pm10){
	//console.log("PM10: "+pm10)
	if(pm10<=50){
		return pm10
	}
	else if(pm10>50 && pm10<=100){
		return pm10
	}
	else if(pm10>100 && pm10<=250){
		return 100+(pm10-100)*100/150;
	}
	else if(pm10>250 && pm10<=350){
		return 200+(pm10-250);
	}
	else if(pm10>350 && pm10<=430){
		return 300+(pm10-350)*(100/80);
	}
	else if(pm10>430){
		return 400+(pm10-430)*(100/80);
	}
}
		





function displayGraph(div,data=null){
	//console.log(div)
	parseTime=d3.timeParse("%Y-%m-%dT%H:%M:%SZ")
	//console.log(parseTime(data[0]['created_at']))
	//console.log(data[0]['created_at'])
	gheight=130
	//pm10={height: $("#pm10").height(), width:$("#pm10").width()}
	//aqi={height: $("#aqi").height(), width:$("#aqi").width()}
	//pm25={height: $("#pm25").height(), width:$("#pm25").width()}
	pm10={height: gheight, width:$("#pm10").width()}
	aqi={height: gheight, width:$("#aqi").width()}
	pm25={height: gheight, width:$("#pm25").width()}
	
	var svgpm25 = d3.select(div).select('#pm25').append("svg")
								.attr("width",pm25.width)
								.attr("height",pm25.height)
								.attr("id", "svgpm25")
		
	var svgpm10 = d3.select(div).select('#pm10').append("svg")
								.attr("width",pm10.width)
								.attr("height",pm10.height)
								.attr("id", "svgpm10")
	
	var svgaqi = d3.select(div).select('#aqi').append("svg")
								.attr("width",aqi.width)
								.attr("height",aqi.height)
								.attr("id", "svgaqi")
		
	//console.log(d3.time.hour.floor(new Date()))
	//console.log(d3.time.hour.ceil(new Date()))
		
	var x = d3.scaleTime().range([0, pm10.width-35]);  
	var y = d3.scaleLinear().range([gheight, 0]);


	height=gheight-25
	
	data.forEach(function(d) {
		d.created_at = parseTime(d.created_at);
		d.pm10 = +d.pm10;
		d.pm25 = +d.pm25;
		d.aqi = +d.aqi;
		d.sipm10=Math.round(getSiPm10(d.pm10));
		d.simp25=Math.round(getSiPm25(d.pm25));
		if(d.sipm10>d.sipm25){
			d.aqi=d.sipm10;
		}
		else{
			d.aqi=d.sipm25;
		}
		
    });
    
    x.domain(d3.extent(data, function(d) { return d.created_at; }));
    y.domain([0, d3.max(data, function(d) { return d.aqi; })]);

	
	
	
	
	d3.select(div).select("#svgpm10")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(20," + height + ")")
		.call(d3.axisBottom(x)
              .tickFormat(d3.timeFormat("%H:%M")))
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-35)");

	d3.select(div).select("#svgpm25")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(20," + height + ")")
		.call(d3.axisBottom(x)
              .tickFormat(d3.timeFormat("%H:%M")))
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-35)");

	d3.select(div).select("#svgaqi")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(20," + height + ")")
		.call(d3.axisBottom(x)
              .tickFormat(d3.timeFormat("%H:%M")))
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-35)");
        
    

}
