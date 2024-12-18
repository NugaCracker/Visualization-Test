<template>
    <div>
        <header class="text-center py-4 bg-primary text-white">
            <h1 style="font-size: 3rem;">Visualization Test</h1>
            <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
            rel="stylesheet"
            />
        </header>

        <div id="box1" class="container my-5 p-4 border shadow-sm bg-light rounded">
        <h3 class="mb-4 text-center">CSV 파일 업로드</h3>

        <!-- 상단: 시도와 시군구 선택 -->
        <div class="row g-3 justify-content-center align-items-center mb-3">
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

        <!-- 하단: 제목과 파일 업로드 -->
        <div class="row g-3 justify-content-center align-items-center mb-3">
            <div class="col-md-4">
                <input v-model="fileTitle" type="text" class="form-control" placeholder="제목을 입력하세요" />
            </div>
            <div class="col-md-3">
                <input type="file" class="form-control filebox" @change="handleFileUpload" />
            </div>
        </div>

        <!-- 버튼 -->
        <div class="row g-3 justify-content-center">
            <div class="col-md-auto">
                <button class="btn btn-success me-2" @click="addButton">확인</button>
                <button class="btn btn-secondary" @click="cancelFile">취소</button>
            </div>
        </div>

        <!-- 생성된 버튼 -->
        <div id="buttonbar" class="mt-4 text-center">
            <div class="d-inline-flex flex-wrap gap-2">
                <button
                    v-for="(button, index) in buttonList"
                    :key="index"
                    class="btn btn-outline-primary"
                >
                    {{ button.title }}
                    <span @click="removeButton(index)" style="cursor: pointer; color: red;">&times;</span>
                </button>
            </div>
        </div>
        </div>
    </div>
</template>




<script>
import axios from 'axios';
import { computed, ref } from 'vue';
import { citiesByProvince, provinces } from '../data/sigun';

export default {
setup() {
    const fileTitle = ref('');
    const buttonList = ref([]);
    const uploadedFile = ref(null);

    const selectedProvince = ref("");
    const selectedCity = ref("");

    // 필터링된 시군구 목록
    const filteredCities = computed(() => {
        return citiesByProvince[selectedProvince.value] || []; // 기본값 빈 배열 처리
    });

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', uploadedFile.value);
        formData.append('table_name', fileTitle.value);
        formData.append('province', selectedProvince.value);
        formData.append('city', selectedCity.value);  // city 값 추가

        console.log("FormData 내용:");
        for (let pair of formData.entries()) {
            console.log(`${pair[0]}: ${pair[1]}`);
        }

        try {
            const response = await axios.post('/api/upload-csv-to-festival', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            console.log("서버 응답:", response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('파일 업로드에 실패했습니다.');
        }
    };


    const addButton = () => {
        if (!selectedProvince.value) return alert("시도를 선택하세요.");
        if (!selectedCity.value) return alert("시군구를 선택하세요.");
        if (!fileTitle.value.trim()) return alert('제목을 입력하세요.');
        if (!uploadedFile.value) return alert('파일을 선택해주세요');
        if (buttonList.value.some(button => button.title === fileTitle.value)) {
            return alert('중복된 제목입니다.');
        }

        const formData = new FormData();
        formData.append('file', uploadedFile.value);
        formData.append('table_name', fileTitle.value);
        formData.append('province', selectedProvince.value);
        formData.append('city', selectedCity.value);

        console.log("FormData 내용:");
        for (let pair of formData.entries()) {
            console.log(`${pair[0]}: ${pair[1]}`);
        }

        // 입력 초기화
        buttonList.value.push({ title: fileTitle.value });
        fileTitle.value = '';
        uploadedFile.value = null;

        const fileInput = document.getElementsByClassName("filebox")[0];
        if (fileInput) fileInput.value = ""; // 파일 선택 초기화
    };

    const removeButton = (index) => {
        buttonList.value.splice(index, 1);
    };

    const cancelFile = () => {
        fileTitle.value = '';
        selectedProvince.value = "";
        selectedCity.value = "";
    };

    return {
        provinces,
        selectedProvince,
        selectedCity,
        filteredCities,
        fileTitle,
        uploadedFile,
        handleFileUpload,
        addButton,
        cancelFile,
        removeButton,
    };
    },
};
</script>
