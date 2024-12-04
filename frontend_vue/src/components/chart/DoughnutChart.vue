<template>
    <div class="chart-container">
        <Doughnut :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from 'chart.js';
import { Doughnut } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend);

export default {
    name: 'DoughnutChart',
    props: {
        chartData: { type: Object, required: true },
        chartOptions: { type: Object, required: true },
    },
    components: { Doughnut },
};
</script>

<style scoped>
    .chart-container {
    height: 400px;
    }
</style>
