<template>
    <div>
        <h1>유동인구 전체표</h1>
        <table>
            <thead>
                <tr>
                    <th>날짜</th>
                    <th>요일</th>
                    <th>성별</th>
                    <th>나이대</th>
                    <th>지역</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="pop in populations" :key="pop.num">
                <td>{{ pop.dt }}</td>
                <td>{{ pop.day }}</td>
                <td>{{ pop.gender }}</td>
                <td>{{ pop.age }}</td>
                <td>{{ pop.sido }} {{ pop.sigun }}</td>
            </tr>

            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'PopulationInfo',
    data() {
        return {
            populations: [], // 직원 데이터를 저장
        };
    },
    created() {
    axios.get('/api/gyeonbuksportfestival/population')
        .then(response => {
            console.log("API Response:", response.data);
            this.populations = response.data.objects; // API 데이터 구조 확인
        })
        .catch(error => {
            console.error("Error fetching population data:", error);
        });
    }
};
</script>

<style>
table {
    border-collapse: collapse;
    width: 100%;
}

th,
td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
}
</style>