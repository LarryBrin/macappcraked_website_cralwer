d3.json("./app_name_and_viewed_number.json", function(data) {
  // console.log(data);
  dataset = data;
  dataset = [5, 10, 15, 20, 25];
  var w = 500;
  h = 50;

  // d3.select("body")
  //   .selectAll("svg")
  //   .data(dataset)
  //   .enter()
  //   .append("p")
  //   .text(function(d) {return "the value is: " + d;})
  //   .style("color", function(d) {
  //     if (d[1] > 400) {
  //       return "red"
  //     } else {
  //       return "orange"
  //     }
  //   });
  // dataset = [ 5, 10, 15, 20, 25 ];
  d3.select("body")
    .append("br")
    .append("br")
    .data(dataset)
    .enter()
    .append("div")
    .attr("class", "bar")
    .style("height", function(d) {
      return d[1] / 20 + "px";
    });
  svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);
  circles = svg.selectAll("circle")
      .data(dataset)
      .enter()
      .append("circle");
  circles.attr("cx", function(d, i) {
              return (i * 50) + 25;
          })
          .attr("cy", h/2)
          .attr("r", function(d) {
            return d;
          })
          .attr("fill", "yellow")
          .attr("stroke", "orange")
          .attr("stroke-width", function(d) {
            return d/5;
          });
});

var dataset = [ 5, 10, 13, 19, 21, 25, 22, 18, 15, 13,
                    11, 12, 15, 20, 18, 17, 16, 18, 23, 25 ];

d3.select("body")
  .selectAll("div")
  .data(dataset)
  .enter()
  .append("div")
  .attr("class", "bar")
  .style("height", function(d) {
    var barHeight = d * 5;
    return barHeight + "px";
  });

var w = 600;
var h = 250;
var barPadding = 1;

var svg = d3.select("body")
            .append("svg")
            .attr("width", w)
            .attr("height", h);

svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
      return i * (w / dataset.length);
    })
    .attr("y", function(d) {
      return h - d * 4;
    })
    .attr("width", w / dataset.length - barPadding)
    .attr("height", function(d) {
      return d * 4;
    })
    // .style("color", "red")
    .attr("fill", function(d) {
      return "rgb(0, 0, " + (d * 5) + ")";
    })
    .append("br");

svg.selectAll("text")
    .data(dataset)
    .enter()
    .append("text")
    .text(function(d) {
      return d;
    })
    .attr({"font-family": "sans-serif",
            "font-size": "11px",
            "fill": "white",
            "text-anchor": "middle",
            "x": function(d, i) {return i * (w / dataset.length) + (w / dataset.length - barPadding) / 2;},
            "y": function(d) {return h - (d * 4) + 15;},
    });

console.log(Math.PI)

var dataset = [[5, 20], [480, 90], [250, 50], [100, 33], [330, 95],
                [410, 12], [475, 44], [25, 67], [85, 21], [220, 88],
              [600, 150]];
var dataset = [];
var numDataPoints = 50;
var xRange = Math.random() * 1000;
var yRange = Math.random() * 1000;
for (var i = 0; i < numDataPoints; i++) {
    var newNumber1 = Math.floor(Math.random() * xRange);
    var newNumber2 = Math.floor(Math.random() * yRange);
    dataset.push([newNumber1, newNumber2]);
}
var padding = 30;
var xScale = d3.scale.ordinal()
                .domain(d3.range(dataset.length))
                .rangeRoundBands([0, w], 0.02);
var yScale = d3.scale.linear()
                .domain([0, d3.max(dataset, function(d) {return d[1];})])
                .range([h - padding, padding]);
var rScale = d3.scale.linear()
                .domain([0, d3.max(dataset, function(d) {return d[1];})]).range([2, 5])
var aScale = d3.scale.sqrt()
                .domain([0, d3.max(dataset, function(d) {return d[1];})])
                .range([0, 10]);
var svg = d3.select("body")
            .append("svg")
            .attr("width", w)
            .attr("height", h);
svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
      return xScale(i);
    })
    .attr("width", xScale.rangeBand());
svg.selectAll("rect")
    .data(dataset)
    .attr("y", function(d) {
      return h - yScale(d);
    })
    .attr("height", function(d) {
      return yScale(d);
    });
d3.select("p")
    .on("click", function() {
      alert("Hey, don't click on taht!");
    });
svg.selectAll("circle")
    .data(dataset)
    .enter()
    .append("circle")
    .attr({
      "cx": function(d) {return xScale(d[0]);},
      "cy": function(d) {return yScale(d[1]);},
      "r": function(d) {return aScale(d[1]);},
    });
svg.selectAll("text")
    .data(dataset)
    .enter()
    .append("text")
    .text(function(d) {
      return d[0] + "," + d[1];
    })
    .attr({
      "x": function(d) {return xScale(d[0])},
      "y": function(d) {return yScale(d[1])},
      "font-family": "sans-serif",
      "font-size": "11px",
      "fill": "red",
    });

var dataset = [100, 200, 300, 400, 500];
// var scale = d3.scaleLinear();
// scale(2.5);
// scale.domain([100, 500]);
// scale.range([10, 350]);
var scale = d3.scale.linear()
              .domain([100, 500])
              .range([10, 350]);


console.log(scale(100), scale(300), scale(350), scale(500))
var parseTime = d3.time.format("%m/%d/%y");
console.log(parseTime.parse("02/07/15"))


var xAixs = d3.svg.axis()
              .scale(xScale)
              .orient("bottom")
              .ticks(10);
var yAxis = d3.svg.axis()
                  .scale(yScale)
                  .orient("left")
                  .ticks(10);
// var formatAsPercentage = d3.format("0.1%");
// xAixs.tickFormat(formatAsPercentage)
svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0, " + (h - padding) + ")")
    .call(xAixs);
svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + padding + ", 0)")
    .call(yAxis)


var dataset = [ 5, 10, 13, 19, 21, 25, 22, 18, 15, 13, 11, 12, 15, 20, 18, 17, 16, 18, 23, 25 ];
var w = 600;
var h = 250;
var xScale = d3.scale.ordinal()
                      .domain(d3.range(dataset.length))
                      .rangeRoundBands([0, w], 0.05);
svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
      return xScale(i);
    })
    .attr("width", xScale.rangeBands());

d3.select("p")
  .on("click", function() {
    alert("Hey, don't click that!");
  });
svg.selectAll("reac")
    .data(dataset)
    .attr("y", function(d) {
      return h - yScale(d);
    });
d3.select("p")
  .on("click", function() {
    dataset = [ 11, 12, 15, 20, 18, 17, 16, 18, 23, 25,
                        5, 10, 13, 19, 21, 25, 22, 18, 15, 13 ];
    svg.selectAll("rect")
        .data(dataset)
        .attr("y", function(d) {
          return h - yScale(d);
        })
        .attr("height", function(d) {
          return yScale(d);
        });
  });
