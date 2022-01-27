import { useRef, Suspense } from 'react'
import { Canvas, useLoader, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function Planet() {
  const planet = useRef<THREE.Group>(null!)
  const planetContainer = useRef<THREE.Group>(null!)
  const [map, topologyMap, roughnessMap] = useLoader(THREE.TextureLoader, [
    '/colour_1024x512.jpg', 
    '/topology_1024x512.jpg',
    '/roughness_3600x1800.jpg',
  ])
  useFrame(() => {
    planet.current.rotation.y += 0.002
  })
  return (
    <group ref={planet}>
      <mesh>
        <sphereGeometry args={[10, 32*4, 32*4]} />
        <meshStandardMaterial
          map={map}
          bumpMap={topologyMap}
          bumpScale={3}
          displacementMap={topologyMap}
          displacementScale={0.2}
          roughnessMap={roughnessMap}
          // emissive={new THREE.Color("white")}
          // emissiveMap={emissiveMap}
          // emissiveIntensity={1}
          />
      </mesh>
    </group>
  )
}

function Globe() {
  return (
    <Canvas camera={{position: [0,0,27], fov: 45}}>
    <Suspense fallback={null}>
        <ambientLight args={["0x888"]} />
        <directionalLight args={["#fff", 5]} position={[1,1,1]} />
        <Planet />
    </Suspense>
    </Canvas>
  )
}

export default Globe
