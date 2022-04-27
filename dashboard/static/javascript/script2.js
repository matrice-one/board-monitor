window.onload = function () {
    var json = {"nodes": ["{{ data_node | safe }}",
"links": ["{{ data_links | safe }"}]}
    var width = 960,
    height = 500;

    var color = d3.scale.category20();

    var force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
    .size([width, height]);

    var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)

    force.nodes(json.nodes)
    .links(json.links)
    .start();

    var link = svg.selectAll(".link")
    .data(json.links)
    .enter().append("line")
    .attr("class", function(d){ return ["link", d.source.name, d.target.name].join(" "); })
    .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    // Set up dictionary of neighbors
    var node2neighbors = {};
    for (var i =0; i < json.nodes.length; i++){
    var name = json.nodes[i].name;
    node2neighbors[name] = json.links.filter(function(d){
    return d.source.name == name || d.target.name == name;
    }).map(function(d){
    return d.source.name == name ? d.target.name : d.source.name;
    });
    }

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

    nodes.append("title")
    .text(function(d) { return d.name; });

    force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });

    nodes.attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; });
    });
}
