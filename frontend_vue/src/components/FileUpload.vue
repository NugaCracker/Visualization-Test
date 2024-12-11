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
    </div>
    
</template>

<script>
import { ref } from 'vue';

export default{
    setup() {
    const fileTitle = ref('');
    const buttonList = ref([]);
    const selectedTitle = ref('');

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
        handleFileUpload,
        addButton,
        cancelFile,
        handleButtonClick,
    }


    }
}

</script>




