<template>
    <div>
        <canvas id="bar-chart"></canvas>
    </div>
</template>

<script>
import { BarController, BarElement, CategoryScale, Chart, Legend, LinearScale, Title, Tooltip } from 'chart.js';

// Chart.js 플러그인 및 컨트롤러 등록
Chart.register(Title, Tooltip, Legend, BarElement, BarController, CategoryScale, LinearScale);

export default {
    name: 'TestChart3',
    mounted() {
        // 캔버스 엘리먼트를 가져옴
        const ctx = document.getElementById("bar-chart").getContext("2d");

        // 가로 바 차트 생성
        new Chart(ctx, {
            type: 'bar', // 바 차트 유형
            data: {
                labels: ["구미시", "칠곡군", "김천시", "안동시", "상주시", "영주시", "경산시", "영덕군", "etc"],
                datasets: [
                    {
                        backgroundColor: ["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#D4F0F0"],
                        data: [15617, 588, 433, 330, 250, 248, 229, 229, 3492]
                    }
                ]
            },
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
                        padding: 30
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
                            callback: function(value) {
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
                                ctx.fillText(value, bar.x + 25, (bar.y + bar.height / 2) -12);
                            });
                        });
                    }
                }
            ]
        });
    }
};
</script>


<style scoped>
/* 캔버스 스타일 */
canvas {
    display: block;
    margin: 0 auto;
    padding-bottom: 20px; /* 상단 여백 추가 */
    width: 100%; /* 차트 너비 */
    height: 576.8px; /* 차트 높이 증가 */
}
</style>
