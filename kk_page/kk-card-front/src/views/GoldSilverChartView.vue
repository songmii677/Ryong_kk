<template>
  <div class="container mt-4">
    <h2>현물 상품 비교</h2>

    <div class="card p-4 mt-3">
      <h5>금/은 가격 변동</h5>

      <div class="d-flex gap-2 mt-3">
        <button
          class="btn"
          :class="asset === 'gold' ? 'btn-warning' : 'btn-outline-warning'"
          @click="changeAsset('gold')"
        >
          금
        </button>

        <button
          class="btn"
          :class="asset === 'silver' ? 'btn-secondary' : 'btn-outline-secondary'"
          @click="changeAsset('silver')"
        >
          은
        </button>
      </div>

      <div class="date-row">

        <div class="date-group">
          <div class="field">
            <label>시작일</label>
            <input type="date" v-model="startDate" />
          </div>

          <div class="field">
            <label>종료일</label>
            <input type="date" v-model="endDate" />
          </div>
        </div>

        <button class="search-btn" @click="fetchPrices">
          조회
        </button>

      </div>

      <p v-if="errorMessage" class="text-danger mt-3">
        {{ errorMessage }}
      </p>

      <p v-if="infoMessage" class="text-muted mt-3">
        {{ infoMessage }}
      </p>

      <div class="mt-4">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, nextTick } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
)

const asset = ref('gold')
const startDate = ref('')
const endDate = ref('')
const errorMessage = ref('')
const infoMessage = ref('')

const chartCanvas = ref(null)
let chartInstance = null

const changeAsset = selectedAsset => {
  asset.value = selectedAsset
  fetchPrices()
}

const fetchPrices = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/prices/', {
      params: {
        asset: asset.value,
        start: startDate.value,
        end: endDate.value
      }
    })

    console.log(response.data)

    drawChart(response.data.labels, response.data.prices)

  } catch (error) {
    console.log(error)
    errorMessage.value = '데이터를 불러오지 못했습니다.'
  }
}

const drawChart = async (labels, prices) => {
  await nextTick()

  if (chartInstance) {
    chartInstance.destroy()
  }

  const labelName = asset.value === 'gold' ? 'Gold Price' : 'Silver Price'
  const lineColor = asset.value === 'gold' ? '#f1c40f' : '#95a5a6'

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: labelName,
          data: prices,
          borderColor: lineColor,
          backgroundColor: lineColor,
          tension: 0.2,
          pointRadius: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true
        },
        title: {
          display: true,
          text: asset.value === 'gold' ? '금 가격 변동 그래프' : '은 가격 변동 그래프'
        }
      },
      scales: {
        x: {
          ticks: {
            maxTicksLimit: 10
          }
        },
        y: {
          beginAtZero: false
        }
      }
    }
  })
}

onMounted(() => {
  fetchPrices()
})
</script>
