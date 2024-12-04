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
              <DoughnutChart :chart-data="doughnutData" :chart-options="doughnutOptions" />
            </div>
          </div>
          <div class="col-md-6">
            <div class="chart-container p-3 border rounded shadow-sm bg-white">
              <h4 class="text-center text-primary">&lt; 막대 그래프 &gt;</h4>
              <BarChart :chart-data="barData" :chart-options="barOptions" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script>
import { ref } from 'vue';
import BarChart from './components/chart/BarChart.vue';
import DoughnutChart from './components/chart/DoughnutChart.vue';

export default {
  name: 'App',
  components: { BarChart, DoughnutChart },
  setup() {
    const fileTitle = ref('');
    const buttonList = ref([]);
    const selectedTitle = ref('');
    const doughnutData = ref({
      labels: ['Category A', 'Category B', 'Category C'],
      datasets: [
        {
          label: 'Doughnut Data',
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
          data: [30, 50, 20],
        },
      ],
    });
    const doughnutOptions = ref({
      responsive: true,
      plugins: { legend: { position: 'top' }, title: { display: true, text: 'Doughnut Chart' } },
    });
    const barData = ref({
      labels: ['January', 'February', 'March'],
      datasets: [
        {
          label: 'Bar Data',
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          data: [10, 20, 30],
        },
      ],
    });
    const barOptions = ref({
      responsive: true,
      plugins: { legend: { position: 'top' }, title: { display: true, text: 'Bar Chart' } },
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
      doughnutData,
      doughnutOptions,
      barData,
      barOptions,
      handleFileUpload,
      addButton,
      cancelFile,
      handleButtonClick,
    };
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', 'Helvetica', 'Arial', sans-serif;
  background-color: #f8f9fa;
}
.chart-container {
  min-height: 300px;
}
</style>
