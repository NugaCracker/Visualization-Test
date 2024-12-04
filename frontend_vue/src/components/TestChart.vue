<template>
<div>
    <svg ref="svgContainer" style="width:400px; height: 400px"></svg>
</div>
</template>

<script>
import * as d3 from 'd3';

export default {
name: 'PieChart',
data() {
    return {
    data: [
        { label: 'A', value: 25 },
        { label: 'B', value: 30 },
        { label: 'C', value: 45 },
    ],
    };
},
mounted() {
    const svgContainer = d3.select(this.$refs.svgContainer);

    const svgWidth = +svgContainer.attr('width');
    const svgHeight = +svgContainer.attr('height');

    const radius = Math.min(svgWidth, svgHeight) / 2;

    const g = svgContainer
    .append('g')
    .attr('transform', `translate(${svgWidth / 2},${svgHeight / 2})`);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const pie = d3
    .pie()
    .sort(null)
    .value(d => d.value);

    const path = d3
    .arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

    const label = d3
    .arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);

    const arc = g
    .selectAll('.arc')
    .data(pie(this.data))
    .enter()
    .append('g')
    .attr('class', 'arc');

    arc.append('path')
    .attr('d', path)
    .attr('fill', d => color(d.data.label));

    arc.append('text')
    .attr('transform', d => `translate(${label.centroid(d)})`)
    .attr('dy', '0.35em')
    .text(d => d.data.label);
},
};
</script>
