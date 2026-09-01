'use client';

import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import { useQuery } from '@tanstack/react-query';
import 'leaflet/dist/leaflet.css';
import { apiGet } from '@/lib/api';
import { PaginatedResponse, Complaint, Vehicle } from '@/types';
import styles from './LiveMap.module.css';

// Fix Leaflet's default icon path issues in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom Premium Markers (Neomorphic/Glass style logic via DivIcon)
const createPremiumIcon = (color: string, label: string) => {
  return L.divIcon({
    className: 'custom-leaflet-icon',
    html: `
      <div style="
        background: var(--bg-elevated);
        border: 2px solid ${color};
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 10px ${color}80, var(--neo-shadow);
        color: var(--text-primary);
        font-weight: bold;
        font-size: 14px;
      ">
        ${label}
      </div>
      <div style="
        width: 2px;
        height: 12px;
        background: ${color};
        margin: 0 auto;
      "></div>
    `,
    iconSize: [36, 48],
    iconAnchor: [18, 48],
    popupAnchor: [0, -48],
  });
};

const ICONS = {
  complaint: createPremiumIcon('#ff7b7b', '!'),
  vehicle: createPremiumIcon('#E6FF2B', '🚚'),
  worker: createPremiumIcon('#50b4dc', '👷'),
  bin: createPremiumIcon('#6ddc6d', '🗑️'),
};

const CHENNAI_CENTER: [number, number] = [13.0827, 80.2707]; // Placeholder Center

export default function LiveMap() {
  // Poll complaints every 15s
  const { data: complaintsData } = useQuery<PaginatedResponse<Complaint>>({
    queryKey: ['gis', 'complaints'],
    queryFn: () => apiGet('/complaints?per_page=100'),
    refetchInterval: 15000,
  });

  // Poll vehicles every 10s
  const { data: vehiclesData } = useQuery<PaginatedResponse<Vehicle>>({
    queryKey: ['gis', 'vehicles'],
    queryFn: () => apiGet('/vehicles'),
    refetchInterval: 10000,
  });

  return (
    <div className={styles.mapContainer}>
      <MapContainer
        center={CHENNAI_CENTER}
        zoom={12}
        className={styles.map}
        zoomControl={false}
      >
        {/* CartoDB Dark Matter Tile Layer for Premium SaaS aesthetic */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />

        {/* Geo-Fencing Mock for Ward Boundary */}
        <Circle
          center={CHENNAI_CENTER}
          radius={5000}
          pathOptions={{ color: 'var(--accent)', fillColor: 'var(--accent)', fillOpacity: 0.05, weight: 1, dashArray: '4 4' }}
        >
          <Popup className="premium-popup">
            <strong>Ward 123 Boundary</strong>
            <br />
            Active Geo-Fence
          </Popup>
        </Circle>

        {/* Render Complaints */}
        {complaintsData?.data.map((c) => (
          (c.latitude && c.longitude) ? (
            <Marker key={`comp-${c.id}`} position={[c.latitude, c.longitude]} icon={ICONS.complaint}>
              <Popup className="premium-popup">
                <strong>{c.reference_number}</strong><br/>
                {c.category.replace('_', ' ')}<br/>
                <span style={{ color: '#ff7b7b' }}>{c.status}</span>
              </Popup>
            </Marker>
          ) : null
        ))}

        {/* Render Vehicles */}
        {vehiclesData?.data.map((v) => (
          (v.current_lat && v.current_lng) ? (
            <Marker key={`veh-${v.id}`} position={[v.current_lat, v.current_lng]} icon={ICONS.vehicle}>
              <Popup className="premium-popup">
                <strong>{v.registration_number}</strong><br/>
                Type: {v.vehicle_type}<br/>
                <span style={{ color: '#E6FF2B' }}>{v.status}</span>
              </Popup>
            </Marker>
          ) : null
        ))}

        {/* Workers and Bins would map similarly here based on backend APIs */}
      </MapContainer>
    </div>
  );
}
