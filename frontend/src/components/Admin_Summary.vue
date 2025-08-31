<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">Admin Panel</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-link"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/admin_summary" class="nav-link active"><i class="fas fa-chart-bar me-2"></i>Summary</router-link>
        <router-link to="/manage_quiz" class="nav-link"><i class="fas fa-clipboard-list me-2"></i>Manage Quizzes</router-link>
        <router-link to="/admin_user" class="nav-link"><i class="fas fa-users-cog me-2"></i>Manage Users</router-link>
        <router-link to="/manage_subject" class="nav-link"><i class="fas fa-book me-2"></i>Manage Subjects</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <div>
          <h2 class="fw-bold">Analytics Summary</h2>
          <p class="text-muted">An overview of quiz performance and user engagement.</p>
        </div>
      </header>

      <section class="mt-4">
        <div class="row g-4">
          <div class="col-lg-6">
            <div class="data-card h-100">
              <h5 class="fw-bold mb-3 text-center">Top Scorer by Subject</h5>
              <div class="chart-container">
                <Bar :data="bardata" :options="baroptions" :key="chartKey" />
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="data-card h-100">
              <h5 class="fw-bold mb-3 text-center">Subject-wise User Attempts</h5>
              <div class="chart-container">
                <Pie :data="piedata" :options="pieoptions" :key="chartKey" />
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
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

    // --- NEW, IMPROVED COLOR PALETTE ---
    const primaryColor = '#4F46E5'; // Your primary brand color
    const primaryColorTransparent = 'rgba(79, 70, 229, 0.2)';

    // A modern, cohesive palette for the Pie chart
    const pieChartColors = [
      '#4F46E5', // Primary Indigo
      '#34D399', // Emerald Green
      '#FBBF24', // Amber Yellow
      '#6366F1', // Lighter Indigo
      '#FB7185', // Rose Pink
      '#818CF8', // Lightest Indigo
    ];

    const baroptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: { display: false },
      },
      scales: {
        y: { grid: { color: '#e5e7eb' } },
        x: { grid: { display: false } },
      }
    });

    const pieoptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true, pointStyle: 'circle' } },
        title: { display: false },
      },
    });

    onMounted(async () => {
      const response = await fetch('https://quiz-app-v2-py9b.onrender.com/admin_summary', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token'),
        },
      });
      const data = await response.json();
      if (response.ok) {
        // Bar Chart Data (uses the clean primary color)
        bardata.value.labels = data.bar_labels;
        bardata.value.datasets = [{
          label: 'Score',
          data: data.bar_data,
          backgroundColor: primaryColorTransparent,
          borderColor: primaryColor,
          borderRadius: 4,
          borderWidth: 2,
        }];

        // Pie Chart Data (uses the new, better color palette)
        piedata.value.labels = data.pie_labels;
        piedata.value.datasets = [{
          label: 'Number of attempts',
          data: data.pie_data,
          backgroundColor: pieChartColors, // <-- UPDATED COLORS
          borderColor: '#FFFFFF',
          borderWidth: 2,
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