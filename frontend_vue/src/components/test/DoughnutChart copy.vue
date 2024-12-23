<template>
    <div>
        <canvas id="pie-chart2"></canvas>
    </div>
</template>

<script>
import { ArcElement, Chart, Legend, PieController, Title, Tooltip } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

// Chart.js 플러그인 및 컨트롤러 등록
Chart.register(Title, Tooltip, Legend, ArcElement, PieController, ChartDataLabels);

export default {
    name: 'TestChart2',
    mounted() {
        // 캔버스 엘리먼트를 가져옴
        const ctx = document.getElementById("pie-chart2").getContext("2d");

        // 도넛 차트 생성
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ["현지인", "외지인"],
                datasets: [
                    {
                        label: "비율",
                        backgroundColor: ["#FCC737", "#E73879"],
                        data: [60, 40]
                    }
                ]
            },
            options: {
                responsive: false, // 반응형 활성화 (크기 고정X)
                plugins: {
                    title: {
                        display: true,
                        text: '현지인 및 외지인 비율', // 차트 제목
                        font: {
                            size: 30 // 제목 글자 크기
                        },
                        padding: {
                            bottom: 20 // 제목과 차트 사이 간격
                        }
                    },
                    legend: {
                        display: true,
                        position: 'bottom', // 범례 아래쪽 배치
                        labels: {
                            font: {
                                size: 20 // 범례 글자 크기
                            },
                            color: 'black',
                            padding : 40,
                        },
                        padding: 80 // 범례와 차트 사이 간격 (더 띄움)
                    },
                    datalabels: {
                        color: '#000', // 라벨 색상
                        font: {
                            size: 22 // 데이터 라벨 기본 글자 크기
                        },
                        formatter: (value, ctx) => {
                            const total = ctx.chart.data.datasets[0].data.reduce((acc, curr) => acc + curr, 0);
                            const percentage = ((value / total) * 100).toFixed(1); // 백분율 계산
                            return `${percentage}%\n(${value}명)`; // 값 형식: 40%\n(40명)
                        },
                        anchor: 'center', // 중앙 정렬
                        align: 'center', // 중앙 정렬
                        clamp: true
                    }
                },
                layout: {
                    padding: {
                        top: 20,
                        bottom: 50 // 차트와 범례 사이 간격 추가 조정
                    }
                }
            }
        });
    }
};
</script>

<style scoped>
/* 캔버스 스타일 */
canvas {
    display: block;
    margin: 0 auto;
    padding-top: 20px; /* 상단 여백 추가 */
    width: 100%; /* 차트 너비 */
    height: 100%; /* 차트 높이 */
}
</style>
