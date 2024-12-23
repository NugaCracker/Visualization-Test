<template>
  <div id="app">
      <FileUpload @send-title="handleTitle" />
      <div id="box1" class="container my-5 p-4 border shadow-sm bg-light rounded">
          <ChartManager :selected-title="selectedTitle" />
      </div>
  </div>
</template>

<script>
import ChartManager from './components/ChartManager.vue';
import FileUpload from './components/FileUpload.vue';

export default {
  name: 'App',
  components: { FileUpload, ChartManager },
  data() {
      return {
          selectedTitle: '', // FileUpload에서 전달받은 테이블 제목을 저장
      };
  },
  methods: {
      handleTitle(title) {
          console.log("받은 테이블 제목:", title); // 이벤트로 전달받은 제목 출력
          this.selectedTitle = title; // ChartManager로 전달하기 위해 저장
      },
  },
};
</script>
