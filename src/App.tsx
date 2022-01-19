import { useRef, Suspense } from 'react'
import './App.css'
import { Canvas, useLoader, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function Planet() {
  const planet = useRef<THREE.Group>(null!)
  const planetContainer = useRef<THREE.Group>(null!)
  const [map, topologyMap, roughnessMap] = useLoader(THREE.TextureLoader, [
    '/colour_1024x512.jpg', 
    '/topology_4096x2048.jpg',
    '/roughness_3600x1800.jpg'
  ])
  // const mouse = {
  //   x: 0,
  //   y: 0
  // }
  // addEventListener('mousemove', (event) => {
  //   mouse.x = (event.clientX / innerWidth) * 2 - 1
  //   mouse.y = -(event.clientY / innerHeight) * 2 + 1
  // })
  useFrame(() => {
    planet.current.rotation.y += 0.002
    // planetContainer.current.rotation.x = -mouse.y * 0.25
    // planetContainer.current.rotation.y = mouse.x * 0.25
  })
  return (
    <group ref={planet}>
      <mesh>
        <sphereGeometry args={[1, 32*4, 32*4]} />
        <meshStandardMaterial
          map={map}
          bumpMap={topologyMap}
          bumpScale={0.2}
          displacementMap={topologyMap}
          displacementScale={0.02}
          roughnessMap={roughnessMap}
          />
      </mesh>
    </group>
  )
}

function App() {
  return (
    <div className="App">
      <Canvas camera={{position: [0,0,3.333], fov: 45}}>
        <Suspense fallback={null}>
          <ambientLight args={["0x888"]} />
          <directionalLight args={["#fff", 5]} position={[1,1,1]} />
          <Planet />
        </Suspense>
      </Canvas>
    </div>
  )
}

export default App
