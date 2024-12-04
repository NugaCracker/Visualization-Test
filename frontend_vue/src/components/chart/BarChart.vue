<template>
    <div class="chart-container">
        <Bar :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(BarElement, Tooltip, Legend, CategoryScale, LinearScale);

export default {
    name: 'BarChart',
    props: {
        chartData: { type: Object, required: true },
        chartOptions: { type: Object, required: true },
    },
    components: { Bar },
};
</script>

<style scoped>
    .chart-container {
    height: 400px;
    }
</style>
