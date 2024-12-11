<template>
    <div>
        <canvas ref="barChart"></canvas>
    </div>
</template>

<script>
import { BarController, BarElement, CategoryScale, Chart, Legend, LinearScale, Title, Tooltip } from 'chart.js';
import { onMounted, ref, watch } from 'vue';

Chart.register(BarElement, BarController, Tooltip, CategoryScale, LinearScale, Title, Legend);

export default {
    props: {
        chartData: {
            type: Object,
            required: true,
        },
    },
    setup(props) {
        const barChart = ref(null);
        let chart = null;
        const initChart = () => {
            const ctx = barChart.value.getContext("2d");
            chart = new Chart(ctx, {
                type: 'bar',
                data: props.chartData,
                options: {
                    indexAxis: 'y', // 가로 막대 설정
                    responsive: true, // 반응형 설정
                    maintainAspectRatio: false, //가로세로 비율유지 해제
                    plugins: {
                        title: {
                            display: true,
                            text: '시군구별 방문 인구 TOP8', // 차트 제목
                            font: {
                                size: 30
                            },
                            padding: 20
                        },
                        tooltip: {
                            enabled: false // 기본 툴팁 비활성화
                        },
                        legend: {
                            display: false // 데이터셋 레이블 제거
                        },
                        datalabels: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            min: 0, // 최소값 설정
                            max: 20000, // 최대값 설정
                            ticks: {
                                stepSize: 2000, // 2000 단위로 설정
                                callback: function (value) {
                                    return value.toLocaleString(); // 값에 천 단위 콤마 추가
                                },
                                color: 'black'
                            },
                            title: {
                                display: true,
                                text: '방문인구(명)', // X축 제목
                                font: {
                                    size: 18, // 폰트 크기
                                },
                                color: 'black' // 폰트 색상
                            }
                        },
                        y: {
                            maxBarThickness: 50, // 차트 바 두께 조정
                            ticks: {
                                font: {
                                    size: 15 // 세로 라벨 크기 증가
                                },
                                color: 'black' // 모든 레이블을 검은색으로 설정
                            }
                        }
                    }
                },
                plugins: [
                    {
                        id: 'dataLabelPlugin',
                        afterDatasetsDraw(chart) {
                            const { ctx } = chart;
                            chart.data.datasets.forEach((dataset, i) => {
                                const meta = chart.getDatasetMeta(i);
                                meta.data.forEach((bar, index) => {
                                    const value = dataset.data[index].toLocaleString(); // 값에 천 단위 콤마 추가
                                    ctx.fillStyle = 'black';
                                    ctx.font = '15px Arial';
                                    ctx.textAlign = 'center';
                                    ctx.fillText(value, bar.x + 25, (bar.y + bar.height / 2) - 12);
                                });
                            });
                        }
                    }
                ]
            });
        }

        onMounted(() => {
            initChart();
        });
        
        watch(() => props.chartData, (newData) =>{
            if(chart) {
                chart.data = newData;
                chart.update();
            }
        }, { deep: true });
        return{
            barChart
        };
    }

};
</script>

<style scoped>
canvas {
    display: block;
    margin: 0 auto;
    width: 100%;
    height: 610px;
}
</style>
