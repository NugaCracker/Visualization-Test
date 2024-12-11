<template>
    <div>
        <canvas ref="pieChart"></canvas>
    </div>
</template>

<script>
import { ArcElement, Chart, Legend, PieController, Tooltip } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { onMounted, ref, watch } from 'vue';

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
                                const index = ctx.dataIndex; // 현재 데이터의 인덱스
                                const ratio = value.toFixed(1); // ratio 값
                                const pop = ctx.dataset.customData[index]; // population 값
                                const population = pop.toLocaleString();
                                return `${ratio}%\n(${population}명)`; // ratio + population 표시
                            },
                            anchor: 'center',
                            align: 'center',
                            textAlign: 'center'
                        },
                    },
                    layout: {
                        padding: {
                            top: 20,
                            bottom: 40,
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
    width: 100%;
    height: 100%;
}
</style>
