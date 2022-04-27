window.onload = function () {

    var width = 800,
        height = 600;

    var radius = 15;

    var sourceNodes = "{{ data_node | safe }}";

    var links = "{{ data_links | safe }}";

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    
    var simulation = d3.forceSimulation(sourceNodes)
        .force("charge", d3.forceManyBody(-100))
        .force("link", d3.forceLink(links).distance(80))
        .force("center", d3.forceCenter().x(width / 3).y(height / 2));

    var svg = d3.select('body')
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    var lines = svg.selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .style("stroke", "#ccc")
        .style("stroke-width", 1);

    var circlesGroup = svg.selectAll("g")
        .data(sourceNodes)
        .enter()
        .append("g");

    var circles = circlesGroup
        .append("circle")
        .attr("r", 7.5)
        .style("fill", function (d, i) {
            return color(d.group);
        })
        
        .call(d3.drag()
            .on("start", function (d) {
                simulation.alphaTarget(0.25).restart();
                d.x = Math.max(0, Math.min(width, d.x))
                d.fx = d.x;
                d.y = Math.max(0, Math.min(height, d.y))
                d.fy = d.y;
            })
            .on("drag", function (d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            })
            .on("end", function (d) {
                simulation.alphaTarget(0);
                d.x = Math.max(0, Math.min(width, d.x))
                d.fx = d.x;
                d.y = Math.max(0, Math.min(height, d.y))
                d.fy = d.y;
            }));
    
    
    

    var text = circlesGroup.append("text").text(function (d) { return d.name; })
        .attr("fill", function (d, i) {
            return color(d.group);
        })
        .attr("font-size", 10)
        .attr("font-weight", "bold");

    var clickableNodes = ["Node1"];

var nodes = svg.selectAll(".node")
	.data(json.nodes)
	.enter().append("circle")
	.attr("class", "node")
	.attr("id", function(n){ return n.name; })
	.attr("r", 5)
	.style("fill", function(d) { return color(d.group); })
	.call(force.drag)

nodes.filter(function(n){ return clickableNodes.indexOf(n.name) != -1; })
    .on("click", function(n){
        // Determine if current node's neighbors and their links are visible
        var active   = n.active ? false : true // toggle whether node is active
        , newOpacity = active ? 0 : 1;

        // Extract node's name and the names of its neighbors
        var name     = n.name
        , neighbors  = node2neighbors[name];

        // Hide the neighbors and their links
        for (var i = 0; i < neighbors.length; i++){
            d3.select("circle#" + neighbors[i]).style("opacity", newOpacity);
            d3.selectAll("line." + neighbors[i]).style("opacity", newOpacity);
        }
        // Update whether or not the node is active
        n.active = active;
    });


    simulation.on("tick", function () {

        circles.attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; });

        lines.attr("x1", function (d) { return d.source.x; })
            .attr("y1", function (d) { return d.source.y; })
            .attr("x2", function (d) { return d.target.x; })
            .attr("y2", function (d) { return d.target.y; });

        text.attr("x", function (d) { return d.x + radius; })
            .attr("y", function (d) { return d.y + radius; });
    });
}