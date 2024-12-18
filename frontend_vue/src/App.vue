<template>
  <div id="app">
    <FileUpload />
    <div id="box1" class="container my-5 p-4 border shadow-sm bg-light rounded">
      <h3 class="mb-4 text-center">{{ selectedTitle || '[ 파일 제목 ]' }}</h3>
      <div id="box2" class="container my-5">
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
    </div>
  </div>
</template>


<!-- ----------------------------------------------------------------------------------------------------------- -->

<script>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import FileUpload from './/components/FileUpload.vue';
import BarChart from './components/chart/BarChart.vue';
import DoughnutChart from './components/chart/DoughnutChart.vue';

export default {
  name: 'App',
  components: { DoughnutChart, BarChart, FileUpload },
  setup() {
    const fileTitle = ref('');
    const buttonList = ref([]);
    const selectedTitle = ref('');

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

    const total_population = ref(0); // 총인구 합계
    const localPopulation = ref(0); // 현지인 합계
    const nonLocalPopulation = ref(0); // 외지인 합계

// Flask API 호출
    // const fetchDoughnutData = async () => {
    //     try {
    //         const response = await axios.get('/api/doughnut-data');
    //         const doughnutdata = response.data;

    //         total_population.value = doughnutdata.total_population;
    //         localPopulation.value = doughnutdata.local_population;
    //         nonLocalPopulation.value = doughnutdata.non_local_population;

    //         console.table("doughnutdata:",doughnutdata)

    //         doughnutChartData.value = {
    //             labels: ["현지인", "외지인"],
    //             datasets: [
    //                 {
    //                     label: "비율",
    //                     backgroundColor: ["#FCC737", "#E73879"],
    //                     data: [doughnutdata.local_ratio, doughnutdata.non_local_ratio],
    //                     customData : [localPopulation.value, nonLocalPopulation.value]
    //                 },
    //             ],
    //         };
    //     } catch (error) {
    //         console.error("Error fetching doughnut data:", error);
    //     }
    // };


    // Fetch 데이터 onMounted 시 호출
    onMounted(async () => {
        // await fetchDoughnutData(); // 데이터를 가져온 후 다음 코드를 실행
        // console.log("Mounted: LocalPopulation:", localPopulation.value);
        // console.log("Mounted: NonLocalPopulation:", nonLocalPopulation.value);
    });


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
    // const fetchBarData = async () => {
    //     try {
    //         const response = await axios.get('http://192.168.0.170:8081/api/bar-data');
    //         const bardata = response.data;

    //         bardata.sort((a,b)=> {
    //           if(a.sigun ==="그 외") return 1;
    //           if(b.sigun ==="그 외") return -1;
    //           return 0;
    //         })
    //         console.log("bardata : ", bardata);

    //         // ref의 value를 업데이트
    //         sigun.value = bardata.map(item => item.sigun);
    //         sigun_pop.value = bardata.map(item => item.visitors);

    //         console.log("sigun : ", sigun.value);
    //         console.log("sigun_pop : ", sigun_pop.value);

    //         barChartData.value = {
    //             labels: sigun.value,
    //             datasets: [
    //               {
    //                 backgroundColor: ["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#D4F0F0"],
    //                 data: sigun_pop.value,
    //               },
    //             ],
    //         };
    //     } catch (error) {
    //         console.error("Error fetching doughnut data:", error);
    //     }
    // };


    // Fetch 데이터 onMounted 시 호출
    onMounted(async () => {
        // await fetchBarData(); // 데이터를 가져온 후 다음 코드를 실행
    });








    const handleFileUpload = (event) => {
      console.log('Uploaded file:', event.target.files[0]);
    };

    const addButton = () => {
      if (!fileTitle.value.trim()) return alert('제목을 입력하세요.');
      buttonList.value.push({ title: fileTitle.value });
      fileTitle.value = '';
    };

    const cancelFile = () => {
      fileTitle.value = '';
    };

    const handleButtonClick = (button) => {
      selectedTitle.value = button.title;
    };

    return {
      fileTitle,
      buttonList,
      selectedTitle,
      doughnutChartData,
      barChartData,
      handleFileUpload,
      addButton,
      cancelFile,
      handleButtonClick,
      nonLocalPopulation,
      localPopulation,
      total_population,
      sigun,
      sigun_pop
    };
  },
};
</script>
