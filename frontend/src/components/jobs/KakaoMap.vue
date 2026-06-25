<template>
  <div class="kakao-map-wrapper">
    <h3>근무 위치</h3>
    <p class="map-address">{{ address }}</p>
    <div ref="mapContainer" class="map-container"></div>
    <p v-if="geocodeFailed" class="map-fallback">주소를 지도에서 찾을 수 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  address: String
})

const mapContainer = ref(null)
const geocodeFailed = ref(false)

const loadKakaoScript = () => {
  return new Promise((resolve, reject) => {
    // services까지 완전히 로드된 경우
    if (window.kakao?.maps?.services) {
      resolve()
      return
    }
    // kakao.maps는 있지만 services 초기화 전 (autoload=false 이후 load 호출 필요)
    if (window.kakao?.maps) {
      window.kakao.maps.load(resolve)
      return
    }
    // 스크립트 태그가 이미 DOM에 있지만 아직 로드 중인 경우
    const existing = document.getElementById('kakao-map-script')
    if (existing) {
      existing.addEventListener('load', () => window.kakao.maps.load(resolve))
      existing.addEventListener('error', reject)
      return
    }
    const key = import.meta.env.VITE_KAKAO_API_KEY
    if (!key) {
      console.error('[KakaoMap] VITE_KAKAO_API_KEY가 없습니다. .env 파일을 확인하고 dev 서버를 재시작하세요.')
      reject(new Error('API key missing'))
      return
    }
    const script = document.createElement('script')
    script.id = 'kakao-map-script'
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&libraries=services&autoload=false`
    script.onload = () => window.kakao.maps.load(resolve)
    script.onerror = () => {
      console.error('[KakaoMap] Kakao Maps SDK 로드 실패. API 키 또는 카카오 개발자 콘솔 도메인 등록을 확인하세요.')
      reject(new Error('Script load failed'))
    }
    document.head.appendChild(script)
  })
}

const initMap = async () => {
  if (!props.address || !mapContainer.value) return
  geocodeFailed.value = false

  try {
    await loadKakaoScript()
  } catch (e) {
    console.error('[KakaoMap] 스크립트 로드 오류:', e.message)
    geocodeFailed.value = true
    return
  }

  const geocoder = new window.kakao.maps.services.Geocoder()
  console.log('[KakaoMap] geocoding 주소:', props.address)

  geocoder.addressSearch(props.address, (result, status) => {
    console.log('[KakaoMap] geocoding 결과:', status, result)
    if (status === window.kakao.maps.services.Status.OK) {
      const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x)
      const map = new window.kakao.maps.Map(mapContainer.value, {
        center: coords,
        level: 4
      })
      new window.kakao.maps.Marker({ map, position: coords })
    } else {
      console.warn('[KakaoMap] 주소를 찾지 못했습니다. status:', status, '/ 주소:', props.address)
      geocodeFailed.value = true
    }
  })
}

onMounted(initMap)
watch(() => props.address, initMap)
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.kakao-map-wrapper {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;

  h3 {
    font-size: 14px;
    font-weight: 600;
    color: $primary;
    padding-bottom: 10px;
    border-bottom: 1px solid #f0f0f0;
  }

  .map-address {
    font-size: 13px;
    color: #555;
  }

  .map-container {
    width: 100%;
    height: 300px;
    border-radius: 8px;
    overflow: hidden;
  }

  .map-fallback {
    font-size: 13px;
    color: #aaa;
    text-align: center;
  }
}
</style>
