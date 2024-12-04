<template>
    <div id="test-chart">
        <div>
            <Line :chart-options="chartOptions01" :chart-data="chartData01" :chart-id="chartId" :dataset-id-key="datasetIdKey"
                :plugins="plugins" :css-classes="cssClasses" :styles="styles" />
        </div>
    </div>
</template>

<script>
import {
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    Title,
    Tooltip
} from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale)

export default {
    components: {
        Line
    },

    props: {
        chartId: {
            type: String,
            default: 'line-chart'
        },
        datasetIdKey: {
            type: String,
            default: 'label'
        },
        cssClasses: {
            default: '',
            type: String
        },
        styles: {
            type: Object,
            default: () => { }
        },
        plugins: {
            type: Object,
            default: () => { }
        }
    },

    data() {
        return {
            // chart data
            chartData01: {
                labels: ['label 01', 'label 02', 'label 03', 'label 04'], // 축 라벨
                datasets: [
                    {
                        label: 'test chart 01',
                        backgroundColor: 'rgb(255,255,255, 0)',
                        pointBackgroundColor: '#64CCA2',
                        borderColor: '#64CCA2',
                        pointBorderColor: '#64CCA2',
                        data: [2, 4, 6, 8], // 라벨별 데이터
                        yAxisID: 'y1' // 차트 옵션에서 축 정의 지정
                    },

                    {
                        label: 'test chart 02',
                        backgroundColor: 'rgb(255,255,255, 0)',
                        pointBackgroundColor: '#1d4498',
                        borderColor: '#1d4498',
                        pointBorderColor: '#1d4498',
                        data: [-10, -8, -5, -2],
                        yAxisID: 'y2'
                    }
                ]
            },

            // chart option
            chartOptions01: {
                responsive: true, // 컨테이너 수행 시, 차트 컨버스의 사이즈 조정 여부
                maintainAspectRatio: false, // 크기를 조정할 때 원래 캔버스 종횡비(너비/높이) 유지 여부
                scales: { // 축 정의
                    y1: { // 축 이름
                        suggestedMin: 0, // 축 최소값
                        suggestedMax: 10,  // 축 최대값
                        ticks : {  // 축 바운더리 정의
                            stepSize: 2  // 축 간격
                        },
                        position: 'left', // 축 위치
                    },
                    y2: {
                        suggestedMin: -10,
                        suggestedMax: 0,
                        ticks : {
                            stepSize: 2
                        },
                        position: 'right',
                    }
                }
            },
        }
    }
}
</script>

<style lang="scss">
#test-chart {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
}
</style>