<template>
    <div>
        <canvas ref="pieChart"></canvas>
    </div>
</template>

<script>
import { ArcElement, Chart, Legend, PieController, Tooltip } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { ref, onMounted, watch } from 'vue';

Chart.register(ArcElement, Tooltip, Legend, PieController, ChartDataLabels);

export default {
    props: {
        chartData: {
            type: Object,
            required: true,
        },
    },
    setup(props) {
        const pieChart = ref(null);
        let chart = null;

        const initChart = () => {
            const ctx = pieChart.value.getContext("2d");
            chart = new Chart(ctx, {
                type: 'pie',
                data: props.chartData,
                options: {
                    responsive: false,
                    animation: {
                        animateScale: true,
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: '현지인 및 외지인 비율',
                            font: {
                                size: 30,
                            },
                            padding: {
                                bottom: 20,
                            },
                        },
                        legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                                font: {
                                    size: 20,
                                },
                                color: 'black',
                                padding: 40,
                            },
                        },
                        datalabels: {
                            color: '#000',
                            font: {
                                size: 22,
                            },
                            formatter: (value, ctx) => {
                                const total = ctx.chart.data.datasets[0].data.reduce((acc, curr) => acc + curr, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${percentage}%\n(${value}명)`;
                            },
                            anchor: 'center',
                            align: 'center',
                        },
                    },
                    layout: {
                        padding: {
                            top: 20,
                            bottom: 50,
                        },
                    },
                },
            });
        };

        onMounted(() => {
            initChart();
        });

        watch(() => props.chartData, (newData) => {
            if (chart) {
                chart.data = newData;
                chart.update();
            }
        }, { deep: true });

        return {
            pieChart
        };
    }
};
</script>

<style scoped>
canvas {
    display: block;
    margin: 0 auto;
    padding-top: 20px;
    width: 100%;
    height: 100%;
}
</style>
