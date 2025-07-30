<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3">
          <i class="fas fa-user-circle me-2"></i>Welcome, {{ adminName || 'Admin' }}
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin">
                <i class="fas fa-home me-1"></i>Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin_summary">
                <i class="fas fa-chart-bar me-1"></i>Summary
              </router-link>
            </li>
          </ul>
          <form class="d-flex me-3">
            <input class="form-control me-2" type="search" placeholder="Search..." />
            <button class="btn btn-light" type="submit"><i class="fas fa-search"></i></button>
          </form>
          <router-link to="/login" class="btn btn-outline-light">
            <i class="fas fa-sign-out-alt me-1"></i>Logout
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Summary Content -->
    <div class="container mt-5">
      <div class="text-center mb-4">
        <h1 class="display-5 text-primary">Admin Summary</h1>
        <p class="text-muted">Overview of top scorers and subjects attempted</p>
      </div>
      <div class="row g-4 justify-content-center">
        <div class="col-md-6">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white text-center">
              <h5 class="mb-0">Top Scorer by Subject</h5>
            </div>
            <div class="card-body">
              <Bar :data="bardata" :options="baroptions" :key="chartKey" />
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-lg">
            <div class="card-header bg-success text-white text-center">
              <h5 class="mb-0">Subject-wise User Attempt</h5>
            </div>
            <div class="card-body">
              <Pie :data="piedata" :options="pieoptions" :key="chartKey" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Bar, Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

export default {
  components: { Bar, Pie },
  setup() {
    const chartKey = ref(0);
    const bardata = ref({ labels: [], datasets: [] });
    const piedata = ref({ labels: [], datasets: [] });

    const baroptions = ref({
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Top Scorer by Subject' },
      },
    });

    const pieoptions = ref({
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Subject-wise User Attempt' },
      },
    });

    onMounted(async () => {
      const response = await fetch('http://127.0.0.1:5000/admin_summary', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token'),
        },
      });
      const data = await response.json();
      if (response.ok) {
        bardata.value.labels = data.bar_labels;
        bardata.value.datasets = [{
          label: 'Score',
          data: data.bar_data,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        }];

        piedata.value.labels = data.pie_labels;
        piedata.value.datasets = [{
          label: 'Number of attempts',
          data: data.pie_data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
          ],
          borderWidth: 1,
        }];
        chartKey.value++;
      } else {
        console.error('Error fetching data:', data.error);
      }
    });

    return { bardata, piedata, baroptions, pieoptions, chartKey };
  },
};
</script>

<style scoped>
.chart-container {
  max-width: 100%;
  height: 400px;
  margin: 20px auto;
}
</style>
