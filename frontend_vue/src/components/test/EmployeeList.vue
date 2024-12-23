<template>
    <div>
        <h1>직원 목록</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>이름</th>
                    <th>부서</th>
                    <th>성별</th>
                    <th>전화번호</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="employee in employees" :key="employee.id">
                    <td>{{ employee.id }}</td>
                    <td>{{ employee.username }}</td>
                    <td>{{ employee.dept }}</td>
                    <td>{{ employee.gender }}</td>
                    <td>{{ employee.phone }}</td>
</tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'EmployeeList',
    data() {
        return {
            employees: [], // 직원 데이터를 저장
        };
    },
    created() {
        // 컴포넌트가 생성되면 Flask API 호출
        axios.get('/api/emmap/employee')
            .then(response => {
                console.log("API Response:", response.data); // 응답 데이터를 출력
                this.employees = response.data.objects; // API 데이터를 employees에 저장
                console.log("Updated employees:", this.employees);
            })
            .catch(error => {
                console.error("Error fetching employee data:", error);
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