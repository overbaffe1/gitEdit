import * as T from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

// Local imports are self-contained GLBs. In particular an imported file cannot fetch
// external images/buffers or cause the browser to send the user's local file anywhere.
export async function glb(bytes) {
  const view = new DataView(bytes);
  if (bytes.byteLength < 20 || view.getUint32(0, false) !== 0x676c5446 || view.getUint32(4, true) !== 2)
    throw Error('Нужен один файл GLB 2.0.');
  const manager = new T.LoadingManager();
  manager.setURLModifier((url) => {
    if (/^(blob:|data:)/.test(url)) return url;
    throw Error('Упакуй текстуры и буферы внутрь GLB.');
  });
  const result = await new GLTFLoader(manager).parseAsync(bytes, '');
  return { object: result.scene, clips: result.animations };
}

export function stl(bytes) {
  if (bytes.byteLength < 15) throw Error('В файле нет поверхности.');
  const count = bytes.byteLength >= 84 ? new DataView(bytes).getUint32(80, true) : 0;
  if (
    84 + 50 * count !== bytes.byteLength &&
    !/^\s*solid\b/i.test(new TextDecoder().decode(bytes.slice(0, 160)))
  )
    throw Error('Не удалось прочитать STL.');
  const geometry = new STLLoader().parse(bytes);
  geometry.rotateX(-Math.PI / 2); // STL exhibit convention: Z up.
  geometry.computeVertexNormals();
  geometry.computeBoundingBox();
  const size = geometry.boundingBox.getSize(new T.Vector3()),
    min = geometry.boundingBox.min;
  const longest = Math.max(size.x, size.y, size.z),
    p = geometry.attributes.position,
    n = geometry.attributes.normal;
  if (!p.count || !Number.isFinite(longest) || longest <= 0) {
    geometry.dispose();
    throw Error('Пустая геометрия STL.');
  }
  // Box-project UVs per triangle, not per file. There is no UV channel in standard STL.
  const uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i) - min.x,
      y = p.getY(i) - min.y,
      z = p.getZ(i) - min.z;
    const nx = Math.abs(n.getX(i)),
      ny = Math.abs(n.getY(i)),
      nz = Math.abs(n.getZ(i));
    const [u, v] = ny >= nx && ny >= nz ? [x, z] : nx > nz ? [z, y] : [x, y];
    uv[2 * i] = u / longest;
    uv[2 * i + 1] = v / longest;
  }
  geometry.setAttribute('uv', new T.BufferAttribute(uv, 2));
  const material = new T.MeshStandardMaterial({
    color: geometry.hasColors ? 0xffffff : 0xcfa975,
    vertexColors: !!geometry.hasColors,
    roughness: 0.37,
    metalness: 0.34,
  });
  return { object: new T.Mesh(geometry, material), clips: [], paint: material };
}

function materials(object) {
  const set = new Set();
  object.traverse((o) => {
    if (o.material) for (const m of [].concat(o.material)) set.add(m);
  });
  return set;
}
export function release(object) {
  const textures = new Set();
  for (const m of materials(object)) {
    for (const v of Object.values(m)) if (v?.isTexture) textures.add(v);
    m.dispose();
  }
  for (const t of textures) {
    t.dispose();
    t.image?.close?.();
  }
  object.traverse((o) => {
    o.geometry?.dispose();
    o.skeleton?.dispose();
  });
}

function dais() {
  const g = new T.Group();
  const velvet = new T.MeshStandardMaterial({ color: 0x172820, roughness: 0.63 });
  const brass = new T.MeshStandardMaterial({ color: 0xaf9168, roughness: 0.35, metalness: 0.73 });
  function disk(r, h, y, m) {
    const o = new T.Mesh(new T.CylinderGeometry(r, r, h, 96), m);
    o.position.y = y;
    g.add(o);
  }
  disk(1.47, 0.075, -0.04, velvet);
  disk(1.473, 0.012, -0.047, brass);
  const lines = [];
  for (let i = 0; i < 120; i++) {
    const a = (i * Math.PI) / 60,
      r = i % 10 === 0 ? 1.32 : i % 5 === 0 ? 1.36 : 1.4;
    lines.push(r * Math.cos(a), 0.002, r * Math.sin(a), 1.435 * Math.cos(a), 0.002, 1.435 * Math.sin(a));
  }
  const ruler = new T.BufferGeometry();
  ruler.setAttribute('position', new T.Float32BufferAttribute(lines, 3));
  g.add(new T.LineSegments(ruler, new T.LineBasicMaterial({ color: 0xb99f76 })));
  for (const r of [1.25, 1.444]) {
    const pts = Array.from(
      { length: 128 },
      (_, i) => new T.Vector3(r * Math.cos((i * Math.PI) / 64), 0.003, r * Math.sin((i * Math.PI) / 64))
    );
    g.add(
      new T.LineLoop(new T.BufferGeometry().setFromPoints(pts), new T.LineBasicMaterial({ color: 0x70816d }))
    );
  }
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const ctx = c.getContext('2d'),
    s = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
  s.addColorStop(0, 'rgba(0,0,0,.6)');
  s.addColorStop(0.45, 'rgba(0,0,0,.31)');
  s.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = s;
  ctx.fillRect(0, 0, 128, 128);
  const shadow = new T.Mesh(
    new T.PlaneGeometry(2.18, 2.18),
    new T.MeshBasicMaterial({ map: new T.CanvasTexture(c), transparent: true, depthWrite: false })
  );
  shadow.rotation.x = -Math.PI / 2;
  shadow.position.y = 0.008;
  g.add(shadow);
  return g;
}

export class Theatre {
  constructor(mount, transport) {
    this.transport = transport;
    this.renderer = new T.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'low-power' });
    const r = this.renderer;
    r.setPixelRatio(Math.min(2, devicePixelRatio));
    r.setClearColor(0, 0);
    r.toneMapping = T.ACESFilmicToneMapping;
    r.toneMappingExposure = 1.08;
    const canvas = r.domElement;
    canvas.tabIndex = 0;
    canvas.setAttribute('aria-label', '3D-модель: стрелки вращают, плюс и минус меняют масштаб');
    mount.append(canvas);
    this.scene = new T.Scene();
    this.camera = new T.PerspectiveCamera(33, 1, 0.03, 100);
    const pm = new T.PMREMGenerator(r),
      env = new RoomEnvironment();
    this.scene.environment = pm.fromScene(env, 0, 0.1, 60, { size: 64 }).texture;
    this.scene.environmentIntensity = 0.65;
    env.dispose();
    pm.dispose();
    this.scene.add(new T.HemisphereLight(0xfbf4dc, 0x53655c, 1.02));
    for (const [x, y, z, c, power] of [
      [2, 4, 3, 0xffedcd, 1.65],
      [-3, 2, -3, 0xacffdb, 1.7],
      [0, 1, -3, 0xffb667, 1.15],
    ]) {
      const l = new T.DirectionalLight(c, power);
      l.position.set(x, y, z);
      this.scene.add(l);
    }
    this.dais = dais();
    this.scene.add(this.dais);
    this.controls = new OrbitControls(this.camera, canvas);
    this.controls.enablePan = false;
    this.controls.minDistance = 2;
    this.controls.maxDistance = 12;
    this.controls.maxPolarAngle = Math.PI * 0.89;
    this.controls.addEventListener('change', () => this.request());
    canvas.addEventListener('keydown', (e) => this.key(e));
    this.time = 0;
    this.duration = 8;
    this.playing = false;
    this.last = 0;
    this.frame = 0;
    new ResizeObserver(() => {
      const { width: w, height: h } = mount.getBoundingClientRect();
      if (w && h) {
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        r.setSize(w, h, false);
        this.request();
      }
    }).observe(mount);
    document.addEventListener('visibilitychange', () => {
      this.last = 0;
      if (document.hidden) {
        cancelAnimationFrame(this.frame);
        this.frame = 0;
      } else this.request();
    });
    this.home();
  }
  home() {
    this.camera.position
      .set(2.4, 1.35, 4.75)
      .multiplyScalar((this.model?.capsule ? 1.31 : 1) * (this.camera.aspect < 1.08 ? 1.12 : 1));
    this.controls.target.set(0, -0.1, 0);
    this.controls.update();
    this.request();
  }
  key(e) {
    const delta = new T.Spherical().setFromVector3(this.camera.position.clone().sub(this.controls.target));
    switch (e.key) {
      case 'ArrowLeft':
        delta.theta -= 0.12;
        break;
      case 'ArrowRight':
        delta.theta += 0.12;
        break;
      case 'ArrowUp':
        delta.phi -= 0.1;
        break;
      case 'ArrowDown':
        delta.phi += 0.1;
        break;
      case '+':
      case '=':
        delta.radius *= 0.87;
        break;
      case '-':
        delta.radius *= 1.15;
        break;
      default:
        return;
    }
    e.preventDefault();
    delta.phi = T.MathUtils.clamp(delta.phi, 0.02, this.controls.maxPolarAngle);
    delta.radius = T.MathUtils.clamp(delta.radius, 2, 12);
    this.camera.position.setFromSpherical(delta).add(this.controls.target);
    this.controls.update();
  }
  mount(model) {
    const obj = model.object,
      box = new T.Box3().setFromObject(obj, true),
      size = box.getSize(new T.Vector3()),
      side = Math.max(...size.toArray());
    if (!Number.isFinite(side) || side < 1e-10) throw Error('В модели нет видимых граней.');
    if (this.turn) {
      this.mixer?.stopAllAction();
      this.mixer?.uncacheRoot(this.model.object);
      this.scene.remove(this.turn);
      release(this.model.object);
    }
    this.model = model;
    this.turn = new T.Group();
    const pivot = new T.Group();
    pivot.position.copy(box.getCenter(new T.Vector3())).multiplyScalar(-1);
    pivot.add(obj);
    this.turn.add(pivot);
    this.turn.scale.setScalar(2.04 / side);
    this.scene.add(this.turn);
    this.dais.position.y = (-size.y / side) * 1.02 - (model.capsule ? 0.5 : 0.14);
    this.mixer = new T.AnimationMixer(obj);
    this.action = null;
    this.home();
  }
  clip(index) {
    this.mixer.stopAllAction();
    this.turn.rotation.y = 0;
    const clip = this.model.clips[index];
    this.action = clip ? this.mixer.clipAction(clip).reset().play() : null;
    this.duration = clip?.duration || 8;
    this.seek(0);
  }
  wire(on) {
    for (const m of materials(this.model.object)) m.wireframe = on;
    this.request();
  }
  seek(t) {
    this.time = T.MathUtils.clamp(t, 0, this.duration);
    this.pose();
    this.request();
  }
  pose() {
    if (!this.turn) return;
    if (this.action) this.mixer.setTime(Math.min(this.time, this.duration - 1e-6));
    else this.turn.rotation.y = (this.time / this.duration) * Math.PI * 2;
    this.transport(this.time, this.duration);
  }
  play(on) {
    this.playing = on;
    this.last = 0;
    this.request();
  }
  request() {
    if (!this.frame && !document.hidden)
      this.frame = requestAnimationFrame((t) => {
        this.frame = 0;
        if (this.playing) {
          if (this.last) this.time = (this.time + Math.min(0.25, (t - this.last) / 1000)) % this.duration;
          this.last = t;
          this.pose();
        }
        this.renderer.render(this.scene, this.camera);
        if (this.playing) this.request();
      });
  }
}
