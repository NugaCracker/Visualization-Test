<template>
    <div>
        <header class="text-center py-4 bg-primary text-white">
            <h1 style="font-size: 3rem;">Visualization Test</h1>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
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
                    <input v-model="fileTitle" type="text" class="form-control" placeholder="제목을 입력하세요(영어만 가능)" />
                </div>
                <div class="col-md-3">
                    <input type="file" class="form-control filebox" @change="selectFile" />
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
                    <button v-for="(button, index) in buttonList" :key="index" class="btn btn-outline-primary">
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
import Swal from 'sweetalert2';
import 'sweetalert2/src/sweetalert2.scss';
import { computed, ref } from 'vue';
import '../assets/sweetalert.css'; // CSS 파일 불러오기
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

        //파일 객체는 개별적으로 저장
        const selectFile = (event) => {
            const file = event.target.files[0]; // 사용자가 선택한 첫 번째 파일
            if (file) {
                uploadedFile.value = file;
                console.log("selectFile:", uploadedFile.value);

            } else {
                console.error("파일이 선택되지 않았습니다.");
                fileInputclear()
            }
        };


        //모든 데이터 append 후 서버 요청
        const handleFileUpload = async () => {
            console.log("handleFileUpload", uploadedFile.value)

            if (!uploadedFile.value) {
                console.error("업로드된 파일이 없습니다.");
                alert("파일을 선택해주세요.");
                fileInputclear()
                return;
            }

            const formData = new FormData();
            formData.append("file", uploadedFile.value); // 파일 객체 추가
            formData.append("table_name", fileTitle.value);
            formData.append("province", selectedProvince.value);
            formData.append("city", selectedCity.value);

            console.log("FormData 내용:");
            for (let pair of formData.entries()) {
                console.log(`${pair[0]}: ${pair[1]}`);
            }

            //sweetalert 로딩시작
            Swal.fire({
                title: '데이터 업로드 중',
                html: '잠시만 기다려 주세요...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                },
            });

            try {
                const response = await axios.post("/api/upload-csv-to-festival", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });
                console.log("서버 응답:", response.data);

                //서버응답 성공
                Swal.fire({
                    icon: 'success',
                    title: '업로드 성공!',
                    text: '데이터가 성공적으로 업로드되었습니다.',
                });

            } catch (error) {
                console.error("Error uploading file:", error);

                 // 서버 응답 실패
                Swal.fire({
                    icon: 'error',
                    title: '업로드 실패!',
                    text: '데이터 업로드 중 오류가 발생했습니다.',
                });
                fileInputclear()
            }
        };

        //확인버튼 눌렀을때
        const addButton = () => {
            if (!selectedProvince.value) {
                alert("시도를 선택하세요.");
            } else if (!selectedCity.value) {
                alert("시군구를 선택하세요.");
            } else if (!fileTitle.value.trim()) {
                alert('제목을 입력하세요.');
            } else if (!uploadedFile.value) {
                alert('파일을 선택해주세요');
            } else {
                handleFileUpload();
            }
            cancelFile()

        };
        // 파일 input칸 초기화
        const fileInputclear = () => {
            const fileInput = document.getElementsByClassName("filebox")[0];
            if (fileInput) fileInput.value = "";
        }

        // 버튼 제거
        const removeButton = (index) => {
            buttonList.value.splice(index, 1);
        };

        //입력초기화
        const cancelFile = () => {
            fileTitle.value = ''; // 시각화 제목
            uploadedFile.value = null; //업로드 된 파일
            selectedProvince.value = ""; // 시도
            selectedCity.value = ""; // 시군구
            fileInputclear() // 파일 input창 초기화
        };

        return {
            provinces,
            selectedProvince,
            selectedCity,
            filteredCities,
            fileTitle,
            uploadedFile,
            buttonList,
            handleFileUpload,
            addButton,
            cancelFile,
            removeButton,
            selectFile,
        };
    },
};
</script>
