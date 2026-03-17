<template>
  <div class="relative w-full rounded-xl overflow-hidden shadow-inner border border-gray-200">
    <div id="map" class="h-[300px] w-full z-0 bg-gray-100"></div>
    <div v-if="!mapLoaded" class="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-80 z-10 backdrop-blur-sm">
      <div class="text-center">
        <div class="text-4xl mb-2 animate-bounce">🗺️</div>
        <p class="font-bold text-gray-500 uppercase tracking-widest text-sm">Loading Map...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, ref, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default Leaflet marker icons with Vite
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
})

const props = defineProps({
  markers: {
    type: Array,
    default: () => []
  }
})

let map = null
let markerLayerGroup = null
const mapLoaded = ref(false)

const initMap = () => {
  if (map) return

  // Default to a central point if no markers
  let center = [11.0168, 76.9558]
  if (props.markers && props.markers.length > 0) {
    center = [props.markers[0].lat, props.markers[0].lon]
  }

  map = L.map('map', {
    zoomControl: false // Custom controls look better
  }).setView(center, 12)

  L.control.zoom({ position: 'bottomright' }).addTo(map)

  // A more modern, cleaner map tile style
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map)

  markerLayerGroup = L.layerGroup().addTo(map)
  mapLoaded.value = true

  updateMarkers()
}

const updateMarkers = () => {
  if (!map || !markerLayerGroup) return

  markerLayerGroup.clearLayers()

  if (!props.markers || props.markers.length === 0) return

  const bounds = L.latLngBounds()

  props.markers.forEach(m => {
    const latlng = [m.lat, m.lon]
    bounds.extend(latlng)

    // Create custom HTML marker for emotional design
    const customIcon = L.divIcon({
      className: 'custom-map-marker',
      html: `
        <div class="relative group cursor-pointer">
          <div class="absolute -inset-2 bg-green-500 rounded-full opacity-20 animate-ping"></div>
          <div class="relative w-8 h-8 bg-green-500 rounded-full border-2 border-white shadow-lg flex items-center justify-center text-white font-bold text-xs transform group-hover:scale-110 group-hover:bg-green-400 transition-all duration-200">
            ${Math.round(m.score * 100)}%
          </div>
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    })

    const popupContent = `
      <div class="font-sans">
        <h4 class="font-extrabold text-gray-800 m-0">${m.employer_name || m.name}</h4>
        <p class="text-xs font-bold text-gray-500 mt-1 uppercase">Match: <span class="text-green-600">${Math.round(m.score * 100)}%</span></p>
      </div>
    `

    L.marker(latlng, { icon: customIcon })
      .bindPopup(popupContent, {
        className: 'custom-popup rounded-xl border-none shadow-xl',
        closeButton: false
      })
      .addTo(markerLayerGroup)
  })

  if (props.markers.length > 0) {
    // Add some padding to bounds so markers aren't on the edge
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 })
  }
}

onMounted(() => {
  // Wait a tick for DOM to be ready
  nextTick(() => {
    initMap()
  })
})

watch(() => props.markers, () => {
  updateMarkers()
}, { deep: true })
</script>

<style>
/* Global styles for Leaflet custom popup */
.custom-popup .leaflet-popup-content-wrapper {
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  border: 2px solid #e5e5e5;
  padding: 4px;
}
.custom-popup .leaflet-popup-tip {
  background: white;
  border-right: 2px solid #e5e5e5;
  border-bottom: 2px solid #e5e5e5;
  box-shadow: none;
}
</style>