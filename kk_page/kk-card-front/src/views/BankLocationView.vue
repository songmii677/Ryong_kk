<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import bankData from '@/data/banklocation.json'

// 카카오 JavaScript 키
const MAP_KEY = import.meta.env.VITE_KAKAO_MAP_KEY

// 지도 DOM
const mapContainer = ref(null)

// 선택값
const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')

// 지도와 마커 상태
let map = null
let markers = []
let infowindow = null

// JSON 데이터
const sidoList = bankData.mapInfo
const bankList = bankData.bankInfo

// 선택한 시·도에 해당하는 시·군·구 목록
const sigunguList = computed(() => {
  const sido = bankData.mapInfo.find(
    (item) => item.name === selectedSido.value
  )

  return sido?.countries ?? []
})

// 시·도 변경 시 하위 선택값 초기화
function changeSido() {
  selectedSigungu.value = ''
  selectedBank.value = ''
}

// 시·군·구 변경 시 은행 선택값 초기화
function changeSigungu() {
  selectedBank.value = ''
}

// 카카오 지도 SDK 불러오기
function loadKakaoMapScript() {
  return new Promise((resolve, reject) => {
    if (!MAP_KEY) {
      reject(new Error('VITE_KAKAO_MAP_KEY가 설정되지 않았습니다.'))
      return
    }

    // 이미 카카오 SDK가 로드된 경우
    if (window.kakao?.maps) {
      window.kakao.maps.load(resolve)
      return
    }

    // SDK script가 이미 추가된 경우
    const existingScript = document.querySelector(
      'script[data-kakao-map-sdk="true"]'
    )

    if (existingScript) {
      existingScript.addEventListener('load', () => {
        window.kakao.maps.load(resolve)
      })

      existingScript.addEventListener('error', reject)
      return
    }

    const script = document.createElement('script')

    script.dataset.kakaoMapSdk = 'true'
    script.src =
      `https://dapi.kakao.com/v2/maps/sdk.js` +
      `?appkey=${MAP_KEY}` +
      `&autoload=false` +
      `&libraries=services`

    script.onload = () => {
      window.kakao.maps.load(resolve)
    }

    script.onerror = () => {
      reject(new Error('카카오 지도 SDK 로드에 실패했습니다.'))
    }

    document.head.appendChild(script)
  })
}

// 기본 지도 생성
function createMap() {
  const kakao = window.kakao

  const options = {
    // 강남역 좌표
    center: new kakao.maps.LatLng(37.49818, 127.027386),
    level: 4,
  }

  map = new kakao.maps.Map(mapContainer.value, options)
}

// 은행 검색
function searchBank() {
  if (
    !selectedSido.value ||
    !selectedSigungu.value ||
    !selectedBank.value
  ) {
    alert('광역시/도, 시/군/구, 은행을 모두 선택하세요.')
    return
  }

  if (!map || !window.kakao?.maps?.services) {
    alert('지도가 아직 준비되지 않았습니다.')
    return
  }

  removeMarkers()

  const keyword =
    `${selectedSido.value} ` +
    `${selectedSigungu.value} ` +
    `${selectedBank.value}`

  const places = new window.kakao.maps.services.Places()

  places.keywordSearch(keyword, placesSearchCallback)
}

// 장소 검색 완료 콜백
function placesSearchCallback(data, status) {
  const kakao = window.kakao

  if (status === kakao.maps.services.Status.OK) {
    const bounds = new kakao.maps.LatLngBounds()

    data.forEach((place) => {
      displayMarker(place)

      bounds.extend(
        new kakao.maps.LatLng(
          Number(place.y),
          Number(place.x)
        )
      )
    })

    map.setBounds(bounds)
    return
  }

  if (status === kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 없습니다.')
    return
  }

  alert('검색 중 오류가 발생했습니다.')
}

// 마커 표시
function displayMarker(place) {
  const kakao = window.kakao

  const marker = new kakao.maps.Marker({
    map,
    position: new kakao.maps.LatLng(
      Number(place.y),
      Number(place.x)
    ),
  })

  markers.push(marker)

  kakao.maps.event.addListener(marker, 'click', () => {
    const address =
      place.road_address_name ||
      place.address_name ||
      '주소 정보 없음'

    const content = `
      <div style="
        width: 220px;
        padding: 12px 14px;
        box-sizing: border-box;
        white-space: normal;
        word-break: keep-all;
        overflow-wrap: anywhere;
        font-size: 13px;
        line-height: 1.5;
      ">
        <strong style="
          display: block;
          margin-bottom: 5px;
          color: #222;
          font-size: 14px;
          line-height: 1.4;
          white-space: normal;
          word-break: keep-all;
          overflow-wrap: anywhere;
        ">
          ${place.place_name}
        </strong>

        <span style="
          display: block;
          color: #666;
          white-space: normal;
          word-break: keep-all;
          overflow-wrap: anywhere;
        ">
          ${place.road_address_name || place.address_name || '주소 정보 없음'}
        </span>
      </div>
    `

    if (infowindow) {
      infowindow.close()
    }

    infowindow = new kakao.maps.InfoWindow({
      content,
    })

    infowindow.open(map, marker)
  })
}

// 기존 마커 제거
function removeMarkers() {
  markers.forEach((marker) => {
    marker.setMap(null)
  })

  markers = []

  if (infowindow) {
    infowindow.close()
    infowindow = null
  }
}

// 페이지가 화면에 나타날 때 지도 생성
onMounted(async () => {
  try {
    await loadKakaoMapScript()
    createMap()
  } catch (error) {
    console.error('카카오 지도 초기화 실패:', error)
    alert('지도를 불러오지 못했습니다.')
  }
})

// 페이지에서 나갈 때 마커 정리
onBeforeUnmount(() => {
  removeMarkers()
  map = null
})
</script>

<template>
  <main class="bank-page">
    <header class="page-header">
      <p class="page-badge">BANK LOCATION</p>
      <h1>가까운 은행 찾기</h1>
      <p class="page-description">
        지역과 은행을 선택해 가까운 지점을 확인해보세요.
      </p>
    </header>

    <section class="bank-layout">
      <aside class="search-panel">
        <div class="panel-header">
          <h2>은행 찾기</h2>
          <p>검색 조건을 선택해주세요.</p>
        </div>

        <div class="search-form">
          <div class="form-group">
            <label for="sido">광역시 / 도</label>

            <select
              id="sido"
              v-model="selectedSido"
              @change="changeSido"
            >
              <option value="">
                광역시 / 도를 선택하세요
              </option>

              <option
                v-for="item in sidoList"
                :key="item.name"
                :value="item.name"
              >
                {{ item.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="sigungu">시 / 군 / 구</label>

            <select
              id="sigungu"
              v-model="selectedSigungu"
              :disabled="!selectedSido"
              @change="changeSigungu"
            >
              <option value="">
                시 / 군 / 구를 선택하세요
              </option>

              <option
                v-for="sigungu in sigunguList"
                :key="sigungu"
                :value="sigungu"
              >
                {{ sigungu }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="bank">은행</label>

            <select
              id="bank"
              v-model="selectedBank"
              :disabled="!selectedSigungu"
            >
              <option value="">
                은행을 선택하세요
              </option>

              <option
                v-for="bank in bankList"
                :key="bank"
                :value="bank"
              >
                {{ bank }}
              </option>
            </select>
          </div>

          <button
            type="button"
            class="search-button"
            @click="searchBank"
          >
            은행 찾기
          </button>
        </div>

        <div class="search-guide">
          <span class="guide-icon">i</span>

          <p>
            지도 위 마커를 클릭하면 은행명과 주소를 확인할 수 있어요.
          </p>
        </div>
      </aside>

      <div class="map-card">
        <div
          ref="mapContainer"
          class="map"
        ></div>
      </div>
    </section>
  </main>
</template>
