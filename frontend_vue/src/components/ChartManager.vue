<template>
    <h3 class="mb-4 text-center">{{ selectedTitle ? '[ ' + selectedTitle + ' ]' : '[ 파일 제목 ]' }}</h3>
    <div id="box2" class="container my-5">

        <div class="container p-3  rounded shadow-sm" id ="sigun">
            <!-- 상단: 시도와 시군구 선택 -->
            <div class="row g-3 justify-content-center align-items-center" >
                <div class="col-md-3">
                    <select class="form-control" v-model="selectedProvince" @change="onProvinceChange">
                        <option disabled value="">시도를 선택하세요</option>
                        <option v-for="province in provinces" :key="province" :value="province">
                            {{ province }}
                        </option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-control" v-model="selectedCity">
                        <option disabled value="">시군구를 선택하세요</option>
                        <option v-for="city in filteredCities" :key="city" :value="city">
                            {{ city }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="chart-container p-3 border rounded shadow-sm bg-white">
                <h4 class="text-center text-primary">&lt; 원형 차트 &gt;</h4>
                <DoughnutChart :chartData="doughnutChartData" />
                <h5 style="text-align: center;">전체 방문 인구 : {{ total_population.toLocaleString() }} 명</h5>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container p-3 border rounded shadow-sm bg-white">
                <h4 class="text-center text-primary">&lt; 막대 그래프 &gt;</h4>
                <BarChart :chartData="barChartData" />
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="css">
    #sigun{
        margin-bottom: 20px;
        margin-top: 20px;
        background-color: dodgerblue;
    }
    
    
</style>


<!-- ----------------------------------------------------------------------------------------------------------- -->

<script>
import axios from 'axios';
import { computed, onMounted, ref, watch } from 'vue';
import { citiesByProvince, provinces } from '../data/sigun';
import BarChart from './chart/BarChart.vue';
import DoughnutChart from './chart/DoughnutChart.vue';

export default {
    components: { DoughnutChart, BarChart },
    props: {
        selectedTitle: {
            type: String,
            required: false,
            default: '',
        }
    },
    setup(props) {

        const selectedProvince = ref("");
        const selectedCity = ref("");
        const total_population = ref(0); // 총인구 합계
        const localPopulation = ref(0); // 현지인 합계
        const nonLocalPopulation = ref(0); // 외지인 합계

        //바로 시작(데이터를 가져온 후 다음 코드를 실행)
        onMounted(async () => {
            if(props.selectedTitle){
                await fetchBarData();
            }
            if(selectedCity.value&selectedProvince.value&props.selectedTitle){
                await fetchDoughnutData();
            }
        });

        //변경을 감지하면 실행
        watch(
            [() => props.selectedTitle, () => selectedCity.value],
            ([newTitle, newCity]) => {
                if (newTitle) {
                    fetchBarData(); // selectedTitle이 변경될 때 실행
                }
                if (newTitle && newCity) {
                    fetchDoughnutData(); // selectedCity가 변경될 때 실행
                }
            }
        );

// -----------------------------------------------------------------------------------------------------------
// 도넛차트 데이터
        
        const doughnutChartData = ref({
        labels: ["현지인", "외지인"],
        datasets: [
            {
            label: "비율",
            backgroundColor: ["#FCC737", "#E73879"],
            data: [],
            },
        ],
        });

    // Flask API 호출
        const fetchDoughnutData = async () => {
            try {
                const title = props.selectedTitle;

                const doughnutData = {
                    table_name: title,
                    province: selectedProvince.value,
                    city: selectedCity.value
                }
                console.log("doughnutData :", doughnutData)
                const response = await axios.post('/api/doughnut-data', {doughnutData: doughnutData});
                const doughnut = response.data;

                total_population.value = doughnut.total_population;
                localPopulation.value = doughnut.local_population;
                nonLocalPopulation.value = doughnut.non_local_population;

                console.table("doughnutdata:",doughnut)

                doughnutChartData.value = {
                    labels: ["현지인", "외지인"],
                    datasets: [
                        {
                            label: "비율",
                            backgroundColor: ["#FCC737", "#E73879"],
                            data: [doughnut.local_ratio, doughnut.non_local_ratio],
                            customData : [localPopulation.value, nonLocalPopulation.value]
                        },
                    ],
                };
            } catch (error) {
                console.error("Error fetching doughnut data:", error);
            }
        };



// -----------------------------------------------------------------------------------------------------------
// 바차트 데이터
        
        const barChartData = ref({
        labels: [],
        datasets: [
            {
            backgroundColor: ["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#D4F0F0"],
            data: [],
            },
        ],
        });

        const sigun = ref([]); // 시군 이름 배열
        const sigun_pop = ref([]); // 시군별 방문 인구 배열

        // Flask API 호출
        const fetchBarData = async () => {
            try {
                const title = props.selectedTitle;
                const response = await axios.post('/api/bar-data', {table_name: title});
                const bardata = response.data;

                bardata.sort((a,b)=> {
                    if(a.sigun ==="그 외") return 1;
                    if(b.sigun ==="그 외") return -1;
                    return 0;
                })
                console.log("bardata : ", bardata);

                // ref의 value를 업데이트
                sigun.value = bardata.map(item => item.sigun);
                sigun_pop.value = bardata.map(item => item.visitors);

                console.log("sigun : ", sigun.value);
                console.log("sigun_pop : ", sigun_pop.value);

                barChartData.value = {
                    labels: sigun.value,
                    datasets: [
                        {
                            backgroundColor: ["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#D4F0F0"],
                            data: sigun_pop.value,
                        },
                    ],
                };
            } catch (error) {
                console.error("Error fetching doughnut data:", error);
            }
        };


// -----------------------------------------------------------------------------------------------------------
//기타 등등

        // 필터링된 시군구 목록
        const filteredCities = computed(() => {
            return citiesByProvince[selectedProvince.value] || []; // 기본값 빈 배열 처리
        });

        return {
        doughnutChartData,
        barChartData,
        fetchBarData,
        fetchDoughnutData,
        nonLocalPopulation,
        localPopulation,
        total_population,
        sigun,
        sigun_pop,
        provinces,
        selectedProvince,
        selectedCity,
        filteredCities,
        };
    }
};

</script>
