<template>
  <div id="app">
    <header class="text-center py-4 bg-primary text-white">
      <h1 style="font-size: 3rem;">Visualization Test</h1>
      <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
      />
    </header>
    <div id="box1" class="container my-5 p-4 border shadow-sm bg-light rounded">
      <h3 class="mb-4 text-center">CSV 파일 업로드</h3>
      <div id="file" class="row g-3 justify-content-center align-items-center">
        <div class="col-md-4">
          <input v-model="fileTitle" type="text" class="form-control" placeholder="제목을 입력하세요" />
        </div>
        <div class="col-md-3">
          <input type="file" class="form-control" @change="handleFileUpload" />
        </div>
        <div class="col-md-auto">
          <button class="btn btn-success me-2" @click="addButton">확인</button>
          <button class="btn btn-secondary" @click="cancelFile">취소</button>
        </div>
      </div>
      <div id="buttonbar" class="mt-4 text-center">
        <div class="d-inline-flex flex-wrap gap-2">
          <button
            v-for="(button, index) in buttonList"
            :key="index"
            class="btn btn-outline-primary"
            @click="handleButtonClick(button)"
          >
            {{ button.title }}
          </button>
        </div>
      </div>
    </div>
    <div id="box1" class="container my-5 p-4 border shadow-sm bg-light rounded">
      <h3 class="mb-4 text-center">{{ selectedTitle || '[ 파일 제목 ]' }}</h3>
      <div id="box2" class="container my-5">
        <div class="row">
          <div class="col-md-6">
            <div class="chart-container p-3 border rounded shadow-sm bg-white">
              <h4 class="text-center text-primary">&lt; 원형 차트 &gt;</h4>
              <DoughnutChart :chartData="doughnutChartData" />
            </div>
<div class="row">
  <div class="col-md-6 text-center">
    <h5>현지인 합계: {{ localPopulation }}</h5>
  </div>
  <div class="col-md-6 text-center">
    <h5>외지인 합계: {{ nonLocalPopulation }}</h5>
  </div>
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
import BarChart from './components/chart/BarChart.vue';
import DoughnutChart from './components/chart/DoughnutChart.vue';

export default {
  name: 'App',
  components: { DoughnutChart, BarChart },
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

    const localPopulation = ref(0); // 현지인 합계
    const nonLocalPopulation = ref(0); // 외지인 합계

// Flask API 호출
  const fetchDoughnutData = async () => {
      try {
          const response = await axios.get('http://192.168.0.170:8081/api/doughnut-data');
          const doughnutdata = response.data;

          localPopulation.value = doughnutdata.local_population;
          nonLocalPopulation.value = doughnutdata.non_local_population;

          console.log("Fetched LocalPopulation:", localPopulation.value);
          console.log("Fetched NonLocalPopulation:", nonLocalPopulation.value);

          doughnutChartData.value = {
              labels: ["현지인", "외지인"],
              datasets: [
                  {
                      label: "비율",
                      backgroundColor: ["#FCC737", "#E73879"],
                      data: [doughnutdata.local_ratio, doughnutdata.non_local_ratio],
                  },
              ],
          };
      } catch (error) {
          console.error("Error fetching doughnut data:", error);
      }
  };


    // Fetch 데이터 onMounted 시 호출
    onMounted(async () => {
        await fetchDoughnutData(); // 데이터를 가져온 후 다음 코드를 실행
        console.log("Mounted: LocalPopulation:", localPopulation.value);
        console.log("Mounted: NonLocalPopulation:", nonLocalPopulation.value);
    });


// -----------------------------------------------------------------------------------------------------------

    // 바차트 데이터
    const barChartData = ref({
      labels: ["구미시", "칠곡군", "김천시", "안동시", "상주시", "영주시", "경산시", "영덕군", "etc"],
      datasets: [
        {
          backgroundColor: ["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#D4F0F0"],
          data: [15617, 588, 433, 330, 250, 248, 229, 229, 3492],
        },
      ],
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
    };
  },
};
</script>
