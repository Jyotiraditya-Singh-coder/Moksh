'use client';

import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import * as THREE from 'three';
import { useLanguage } from '@/app/contexts/LanguageContext';

/* ═══════════════════════════════════════════════════════════
   PUBLIC API
   ═══════════════════════════════════════════════════════════ */




export interface BookSceneHandle {
  setProgress: (p: number) => void;
}



/* ═══════════════════════════════════════════════════════════
   BOOK DIMENSIONS
   ═══════════════════════════════════════════════════════════ */
const BOOK_W      = 2.4;    // cover width
const BOOK_H      = 3.2;    // cover height
const COVER_T     = 0.07;   // cover thickness
const PAGE_W      = 2.2;    // page width (slightly smaller than cover)
const PAGE_H      = 3.0;    // page height
const PAGE_SEGS   = 40;     // segments across width for smooth bending
const SPINE_W     = 0.10;   // spine width
const STACK_T     = 0.22;   // total page-stack thickness
const NUM_PAGES   = 4;      // interactive pages

/* ═══════════════════════════════════════════════════════════
   ANIMATION CONSTANTS
   ═══════════════════════════════════════════════════════════ */
const SMOOTH_FACTOR   = 0.10;     // exponential lerp — snappy but stable
const INTRO_END       = 0.10;     // 0–10% = cinematic zoom
const COVER_RANGE: [number, number] = [0.10, 0.15];
export const PAGE_RANGES: [number, number][] = [[0.15, 0.30], [0.31, 0.46], [0.47, 0.62], [0.63, 0.80]];
const BACK_COVER_RANGE: [number, number] = [0.83, 0.94];

/* Maximum bend angle at the tip of the page during mid-flip (radians) */
const BEND_AMOUNT = 0.55;

/* ═══════════════════════════════════════════════════════════
   MATH HELPERS
   ═══════════════════════════════════════════════════════════ */
function clamp(v: number, lo: number, hi: number) {
  return Math.max(lo, Math.min(hi, v));
}

function easeIO(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function snapshotPositions(geo: THREE.BufferGeometry): Float32Array {
  const arr = geo.getAttribute('position').array;
  return new Float32Array(arr);
}

/* ═══════════════════════════════════════════════════════════
   CANVAS TEXTURE FACTORY
   ═══════════════════════════════════════════════════════════ */
function tex(w: number, h: number, fn: (ctx: CanvasRenderingContext2D) => void) {
  const cv = document.createElement('canvas');
  cv.width = w; cv.height = h;
  fn(cv.getContext('2d')!);
  const t = new THREE.CanvasTexture(cv);
  t.needsUpdate = true;
  return t;
}

function updateTexture(t: THREE.CanvasTexture, fn: (c: CanvasRenderingContext2D) => void) {
  const cv = t.image;
  const c = cv.getContext('2d');
  if (c) fn(c);
  t.needsUpdate = true;
}

/* ─── COVER TEXTURES ─── */
function coverFrontTex(t: any) {
  return tex(1024, 1400, (c) => drawCoverFront(c, t));
}

function drawCoverFront(c: CanvasRenderingContext2D, t: any) {
  const g = c.createLinearGradient(0, 0, 0, 1400);
  g.addColorStop(0, '#1e120b');
  g.addColorStop(1, '#0d0805');
  c.fillStyle = g;
  c.fillRect(0, 0, 1024, 1400);
  
  // leather grain noise
  for (let i = 0; i < 5000; i++) {
    c.fillStyle = `rgba(${90 + Math.random() * 50},${50 + Math.random() * 40},${15 + Math.random() * 25},0.04)`;
    c.fillRect(Math.random() * 1024, Math.random() * 1400, 3, 3);
  }
  
  // gold border
  c.strokeStyle = '#c4a35a';
  c.lineWidth = 6;
  c.strokeRect(45, 45, 934, 1310);
  c.lineWidth = 2;
  c.strokeRect(65, 65, 894, 1270);
  
  // title
  c.fillStyle = '#c4a35a';
  c.textAlign = 'center';
  c.font = 'bold 78px Georgia,serif';
  c.fillText('EduNex AI', 512, 580);
  
  c.font = '30px Georgia,serif';
  c.fillText(t('bookCoverSub'), 512, 650);
  
  c.beginPath(); c.moveTo(320, 690); c.lineTo(704, 690); c.stroke();
  c.font = '38px serif';
  c.fillText('\u2726', 512, 740);
}

function coverBackTex() {
  return tex(1024, 1400, (c) => {
    const g = c.createLinearGradient(0, 0, 0, 1400);
    g.addColorStop(0, '#1e120b'); g.addColorStop(1, '#0d0805');
    c.fillStyle = g;
    c.fillRect(0, 0, 1024, 1400);
    for (let i = 0; i < 3000; i++) {
      c.fillStyle = `rgba(${90 + Math.random() * 50},${50 + Math.random() * 40},${15 + Math.random() * 25},0.03)`;
      c.fillRect(Math.random() * 1024, Math.random() * 1400, 3, 3);
    }
    c.strokeStyle = '#c4a35a'; c.lineWidth = 4;
    c.strokeRect(50, 50, 924, 1300);
  });
}

function pageBackTex() {
  return tex(1024, 1400, (c) => {
    c.fillStyle = '#f0ebe3';
    c.fillRect(0, 0, 1024, 1400);
    for (let i = 0; i < 4000; i++) {
      const v = 220 + Math.random() * 20;
      c.fillStyle = `rgba(${v},${v - 8},${v - 16},0.06)`;
      c.fillRect(Math.random() * 1024, Math.random() * 1400, 2, 2);
    }
  });
}

/* ─── DYNAMIC PAGE CONTENT ─── */
function getPageContent(idx: number, t: any) {
  if (idx === 0) {
    return {
      title: '🧠\n' + t('feat1Title'),
      draw: (c: any) => drawFeatureDesc(c, t('feat1Desc'))
    };
  }
  if (idx === 1) {
    return {
      title: '⚠️\n' + t('feat2Title'),
      draw: (c: any) => drawFeatureDesc(c, t('feat2Desc'))
    };
  }
  if (idx === 2) {
    return {
      title: '🎯\n' + t('feat3Title'),
      draw: (c: any) => drawFeatureDesc(c, t('feat3Desc'))
    };
  }
  if (idx === 3) {
    return {
      title: '🗣️\n' + t('feat4Title'),
      draw: (c: any) => drawFeatureDesc(c, t('feat4Desc'))
    };
  }
  return { title: '', draw: drawEmpty };
}

function drawPageContent(c: CanvasRenderingContext2D, idx: number, t: any) {
  c.fillStyle = '#f5f0e8';
  c.fillRect(0, 0, 1024, 1400);
  
  // paper grain
  for (let i = 0; i < 6000; i++) {
    const v = 225 + Math.random() * 25;
    c.fillStyle = `rgba(${v},${v - 8},${v - 18},0.07)`;
    c.fillRect(Math.random() * 1024, Math.random() * 1400, 2, 2);
  }
  
  c.fillStyle = '#c4a35a';
  c.fillRect(90, 90, 844, 3);
  
  const content = getPageContent(idx, t);
  
  c.fillStyle = '#1a0f0a';
  c.textAlign = 'center';
  c.font = 'bold 65px Georgia,serif';
  content.title.split('\n').forEach((l: string, li: number) => c.fillText(l, 512, 250 + li * 85));
  
  c.save(); 
  c.translate(512, 640);
  content.draw(c, t);
  c.restore();
  
  c.fillStyle = '#c4a35a'; 
  c.fillRect(90, 1240, 844, 3);
  
  c.fillStyle = '#999'; 
  c.font = '24px Georgia,serif';
  c.fillText(`${idx + 1}`, 512, 1300);
}

/* ─── ILLUSTRATION DRAWERS ─── */
function drawEmpty(c: CanvasRenderingContext2D, t: any) {
  c.fillStyle = 'rgba(196,163,90,0.1)';
  c.font = 'italic 30px Georgia';
  c.fillText(t('bookPathInstruct'), 0, 0);
}

function drawPathSelect(c: CanvasRenderingContext2D) {
  // Placeholder outlines where HTML buttons will sit
  c.strokeStyle = 'rgba(196,163,90,0.3)';
  c.lineWidth = 2;
  c.setLineDash([10, 10]);
  c.strokeRect(-180, -80, 360, 100);
  c.strokeRect(-180, 40, 360, 100);
  c.setLineDash([]);
}

function drawBrain(c: CanvasRenderingContext2D) {
  c.strokeStyle = '#c4a35a'; c.lineWidth = 3;
  c.beginPath();
  c.arc(0, -30, 80, Math.PI * 0.8, Math.PI * 0.2, true);
  c.lineTo(30, 60); c.lineTo(-30, 60); c.closePath(); c.stroke();
  c.beginPath(); c.moveTo(-18, 60); c.lineTo(-18, 82); c.lineTo(18, 82); c.lineTo(18, 60); c.stroke();
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    c.beginPath(); c.moveTo(Math.cos(a) * 98, Math.sin(a) * 98 - 30);
    c.lineTo(Math.cos(a) * 118, Math.sin(a) * 118 - 30); c.stroke();
  }
  c.fillStyle = '#c4a35a'; c.font = 'bold 34px Georgia'; c.fillText('AI', 0, -18);
}

function drawChart(c: CanvasRenderingContext2D) {
  const bars = [55, 80, 40, 92, 65, 88, 48];
  const bw = 28, gap = 10, sx = -(bars.length * (bw + gap)) / 2;
  c.fillStyle = 'rgba(196,163,90,0.25)'; c.strokeStyle = '#c4a35a'; c.lineWidth = 2;
  bars.forEach((v, i) => { const x = sx + i * (bw + gap), h = v * 1.4; c.fillRect(x, 80 - h, bw, h); c.strokeRect(x, 80 - h, bw, h); });
  c.beginPath(); c.moveTo(sx - 8, 80); c.lineTo(sx + bars.length * (bw + gap), 80); c.stroke();
  c.strokeStyle = '#ff6b6b'; c.lineWidth = 3; c.beginPath();
  bars.forEach((v, i) => { const x = sx + i * (bw + gap) + bw / 2, y = 80 - v * 1.4; i === 0 ? c.moveTo(x, y) : c.lineTo(x, y); });
  c.stroke();
}

function drawRadarWithLabels(c: CanvasRenderingContext2D, t: any) {
  const n = 6, r = 95; c.strokeStyle = '#c4a35a'; c.lineWidth = 1.5;
  for (let ring = 1; ring <= 3; ring++) {
    const rr = (ring / 3) * r; c.beginPath();
    for (let i = 0; i <= n; i++) { const a = (i / n) * Math.PI * 2 - Math.PI / 2; i === 0 ? c.moveTo(Math.cos(a) * rr, Math.sin(a) * rr) : c.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); }
    c.closePath(); c.stroke();
  }
  for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2 - Math.PI / 2; c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.cos(a) * r, Math.sin(a) * r); c.stroke(); }
  const d = [0.8, 0.55, 0.9, 0.5, 0.72, 0.85]; c.fillStyle = 'rgba(196,163,90,0.25)'; c.strokeStyle = '#c4a35a'; c.lineWidth = 2.5; c.beginPath();
  d.forEach((v, i) => { const a = (i / n) * Math.PI * 2 - Math.PI / 2; i === 0 ? c.moveTo(Math.cos(a) * r * v, Math.sin(a) * r * v) : c.lineTo(Math.cos(a) * r * v, Math.sin(a) * r * v); });
  c.closePath(); c.fill(); c.stroke();
  const lbl = [t('bookMath'), t('bookScience'), t('bookEnglish'), t('bookHistory'), t('bookArt'), t('bookCode')]; 
  c.fillStyle = '#1a0f0a'; c.font = '17px Georgia'; c.textAlign = 'center';
  lbl.forEach((l, i) => { const a = (i / n) * Math.PI * 2 - Math.PI / 2; c.fillText(l, Math.cos(a) * (r + 24), Math.sin(a) * (r + 24) + 6); });
}

function drawGlobe(c: CanvasRenderingContext2D) {
  // Clear the boxes since we now use an HTML dropdown
}

function drawFeatureDesc(c: CanvasRenderingContext2D, desc: string) {
  c.fillStyle = '#3b2818';
  c.font = '45px Georgia,serif';
  c.textAlign = 'center';
  
  // Basic text wrapping
  const words = desc.split(' ');
  let line = '';
  let y = -20;
  
  for (let n = 0; n < words.length; n++) {
    const testLine = line + words[n] + ' ';
    const metrics = c.measureText(testLine);
    const testWidth = metrics.width;
    if (testWidth > 800 && n > 0) {
      c.fillText(line, 0, y);
      line = words[n] + ' ';
      y += 65;
    } else {
      line = testLine;
    }
  }
  c.fillText(line, 0, y);
}

/* ═══════════════════════════════════════════════════════════
   CURVED-PAGE VERTEX DEFORMER
   ═══════════════════════════════════════════════════════════ */
function deformPageVertices(
  posAttr: THREE.BufferAttribute,
  basePositions: Float32Array,
  flipT: number,
) {
  const count = posAttr.count;
  const eased = easeIO(flipT);
  const flipAngle = eased * Math.PI;
  const bendStrength = Math.sin(eased * Math.PI) * BEND_AMOUNT;

  for (let i = 0; i < count; i++) {
    const ox = basePositions[i * 3];      
    const oy = basePositions[i * 3 + 1];  
    const nx = clamp(ox / PAGE_W, 0, 1);
    const localBend = bendStrength * nx * nx;
    const theta = flipAngle + localBend;

    const newX = Math.cos(theta) * ox;
    const newZ = Math.sin(theta) * ox;

    posAttr.setXYZ(i, newX, oy, newZ);
  }

  posAttr.needsUpdate = true;
}

/* ═══════════════════════════════════════════════════════════
   SCENE STATE
   ═══════════════════════════════════════════════════════════ */
interface PageData {
  pivot: THREE.Group;
  frontGeo: THREE.BufferGeometry;
  backGeo: THREE.BufferGeometry;
  frontBase: Float32Array;
  backBase: Float32Array;
  frontTex: THREE.CanvasTexture;
}

interface SceneState {
  renderer: THREE.WebGLRenderer;
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  coverPivot: THREE.Group;
  backCoverPivot: THREE.Group;
  pages: PageData[];
  bookGroup: THREE.Group;
  stackBlock: THREE.Mesh;
  coverTex: THREE.CanvasTexture;
  progress: number;
  smoothProgress: number;
  raf: number;
}

/* ═══════════════════════════════════════════════════════════
   COMPONENT
   ═══════════════════════════════════════════════════════════ */
const BookScene = forwardRef<BookSceneHandle>((_, ref) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const state = useRef<SceneState | null>(null);
  const { lang, t } = useLanguage();

  useImperativeHandle(ref, () => ({
    setProgress(p: number) {
      if (state.current) state.current.progress = clamp(p, 0, 1);
    }
  }));

  // Re-draw textures whenever language changes
  useEffect(() => {
    if (!state.current) return;
    const s = state.current;
    
    // Front Cover
    updateTexture(s.coverTex, c => drawCoverFront(c, t));
    
    // Pages
    s.pages.forEach((pg, i) => {
      updateTexture(pg.frontTex, c => drawPageContent(c, i, t));
    });
  }, [lang, t]);

  useEffect(() => {
    const el = mountRef.current;
    if (!el) return;

    const w = el.clientWidth;
    const h = el.clientHeight;

    /* ── Scene ── */
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a0a0f, 0.035);

    /* ── Camera ── */
    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    camera.position.set(0, 0.6, 8);

    /* ── Renderer ── */
    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
      });
    } catch {
      el.innerHTML = '<div style="color:#c4a35a;padding:2rem;">WebGL unsupported</div>';
      return;
    }
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    el.appendChild(renderer.domElement);

    /* ── Lighting ── */
    scene.add(new THREE.AmbientLight(0x404050, 0.5));
    const keyLight = new THREE.DirectionalLight(0xfff5e6, 2.0);
    keyLight.position.set(3, 7, 5);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(2048, 2048);
    keyLight.shadow.bias = -0.001;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0x6688cc, 0.35);
    fillLight.position.set(-4, 3, 2);
    scene.add(fillLight);

    const rimLight = new THREE.PointLight(0x8866ff, 0.4, 20);
    rimLight.position.set(0, 3, -6);
    scene.add(rimLight);

    /* ── Book Structure ── */
    const bookGroup = new THREE.Group();

    // Back Cover
    const backCoverPivot = new THREE.Group();
    backCoverPivot.position.set(0, 0, 0);

    const backCover = new THREE.Mesh(
      new THREE.BoxGeometry(BOOK_W, BOOK_H, COVER_T),
      new THREE.MeshStandardMaterial({
        map: coverBackTex(),
        roughness: 0.7,
        metalness: 0.08,
      }),
    );
    backCover.position.set(BOOK_W / 2, 0, -(STACK_T / 2) - COVER_T / 2);
    backCover.castShadow = true;
    backCover.receiveShadow = true;
    backCoverPivot.add(backCover);
    bookGroup.add(backCoverPivot);

    // Spine
    const spine = new THREE.Mesh(
      new THREE.BoxGeometry(SPINE_W, BOOK_H, STACK_T + COVER_T * 2),
      new THREE.MeshStandardMaterial({ color: 0x1a0f0a, roughness: 0.85 }),
    );
    spine.position.set(-SPINE_W / 2, 0, 0);
    spine.castShadow = true;
    bookGroup.add(spine);

    // Stack Block
    const stackBlock = new THREE.Mesh(
      new THREE.BoxGeometry(PAGE_W * 0.98, PAGE_H * 0.98, STACK_T * 0.7),
      new THREE.MeshStandardMaterial({ color: 0xf0ebe3, roughness: 0.95 }),
    );
    stackBlock.position.set(PAGE_W / 2, 0, -0.06);
    stackBlock.castShadow = true;
    stackBlock.receiveShadow = true;
    bookGroup.add(stackBlock);

    /* ── Pages ── */
    const pages: PageData[] = [];
    const sharedBackTex = pageBackTex();

    for (let i = 0; i < NUM_PAGES; i++) {
      const pivot = new THREE.Group();
      const initialZ = 0.09 + (NUM_PAGES - 1 - i) * 0.02;
      pivot.position.set(0, 0, initialZ);

      const frontGeo = new THREE.PlaneGeometry(PAGE_W, PAGE_H, PAGE_SEGS, 1);
      frontGeo.translate(PAGE_W / 2, 0, 0);
      
      const frontTex = tex(1024, 1400, (c) => drawPageContent(c, i, t));
      const frontMesh = new THREE.Mesh(
        frontGeo,
        new THREE.MeshStandardMaterial({
          map: frontTex,
          side: THREE.FrontSide,
          roughness: 0.92,
        }),
      );
      frontMesh.castShadow = true;
      frontMesh.receiveShadow = true;
      frontMesh.position.z = 0.001;

      const backGeo = new THREE.PlaneGeometry(PAGE_W, PAGE_H, PAGE_SEGS, 1);
      backGeo.translate(PAGE_W / 2, 0, 0);
      const backMesh = new THREE.Mesh(
        backGeo,
        new THREE.MeshStandardMaterial({
          map: sharedBackTex,
          side: THREE.BackSide,
          roughness: 0.92,
        }),
      );
      backMesh.castShadow = true;
      backMesh.position.z = -0.001;

      pivot.add(frontMesh, backMesh);
      bookGroup.add(pivot);

      pages.push({
        pivot, frontGeo, backGeo,
        frontBase: snapshotPositions(frontGeo),
        backBase: snapshotPositions(backGeo),
        frontTex,
      });
    }

    /* ── Front Cover ── */
    const coverPivot = new THREE.Group();
    const coverZ = (STACK_T / 2) + COVER_T / 2;
    coverPivot.position.set(0, 0, 0);

    const cTex = coverFrontTex(t);
    const frontCover = new THREE.Mesh(
      new THREE.BoxGeometry(BOOK_W, BOOK_H, COVER_T),
      new THREE.MeshStandardMaterial({
        map: cTex,
        roughness: 0.65,
        metalness: 0.1,
      }),
    );
    frontCover.position.set(BOOK_W / 2, 0, coverZ);
    frontCover.castShadow = true;
    frontCover.receiveShadow = true;
    coverPivot.add(frontCover);
    bookGroup.add(coverPivot);

    /* ── Initial orientation ── */
    bookGroup.rotation.set(-0.12, 0.18, 0);
    scene.add(bookGroup);

    /* ── Ground ── */
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(10, 10),
      new THREE.ShadowMaterial({ opacity: 0.25 }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -BOOK_H / 2 - 0.35;
    ground.receiveShadow = true;
    scene.add(ground);

    /* ── Init State ── */
    state.current = {
      renderer, scene, camera, coverPivot, backCoverPivot, pages, bookGroup, stackBlock,
      coverTex: cTex,
      progress: 0, smoothProgress: 0, raf: 0,
    };

    /* ── Animation Loop ── */
    function tick() {
      state.current!.raf = requestAnimationFrame(tick);
      const s = state.current!;

      s.smoothProgress += (s.progress - s.smoothProgress) * SMOOTH_FACTOR;
      s.smoothProgress = clamp(s.smoothProgress, 0, 1);
      if (Math.abs(s.progress - s.smoothProgress) < 0.0001) {
        s.smoothProgress = s.progress;
      }

      const p = s.smoothProgress;
      const t = performance.now() * 0.001;

      const introT = easeIO(clamp(p / INTRO_END, 0, 1));
      const introScale = 1 + introT * 0.2;
      const introCamZ  = 8 - introT * 3.0;

      const coverT = clamp((p - COVER_RANGE[0]) / (COVER_RANGE[1] - COVER_RANGE[0]), 0, 1);
      s.coverPivot.rotation.y = -easeIO(coverT) * Math.PI;

      const backCoverT = clamp((p - BACK_COVER_RANGE[0]) / (BACK_COVER_RANGE[1] - BACK_COVER_RANGE[0]), 0, 1);
      const backCoverAngle = -easeIO(backCoverT) * Math.PI;
      s.backCoverPivot.rotation.y = backCoverAngle;
      
      const blockT = clamp((p - 0.20) / (0.75 - 0.20), 0, 1);
      s.stackBlock.scale.z = 1 - blockT * 0.98;
      // Hide the stack block once all turning pages are flipped
      s.stackBlock.visible = p <= 0.75;
      
      s.pages.forEach((pg, i) => {
        const frontAttr = pg.frontGeo.getAttribute('position') as THREE.BufferAttribute;
        const backAttr  = pg.backGeo.getAttribute('position') as THREE.BufferAttribute;

        if (i < PAGE_RANGES.length) {
          const [st, en] = PAGE_RANGES[i];
          const rawT = clamp((p - st) / (en - st), 0, 1);

          deformPageVertices(frontAttr, pg.frontBase, rawT);
          deformPageVertices(backAttr,  pg.backBase,  rawT);

          pg.frontGeo.computeVertexNormals();
          pg.backGeo.computeVertexNormals();

          const eased = easeIO(rawT);
          pg.pivot.position.y = Math.sin(eased * Math.PI) * 0.15;

          const unflippedZ = 0.09 + (NUM_PAGES - 1 - i) * 0.02;
          const flippedZ = -0.08 + i * 0.02;
          pg.pivot.position.z = unflippedZ + (flippedZ - unflippedZ) * eased;
          pg.pivot.rotation.y = 0;
          pg.pivot.renderOrder = eased > 0.5 ? i : NUM_PAGES - i;
        } else {
          // The very last page does not physically bend its paper.
          // It stays flat against the back cover and swings shut as a solid piece.
          deformPageVertices(frontAttr, pg.frontBase, 0);
          deformPageVertices(backAttr,  pg.backBase,  0);
          
          pg.pivot.position.y = 0;
          pg.pivot.position.z = 0.09 + (NUM_PAGES - 1 - i) * 0.02;
          pg.pivot.rotation.y = backCoverAngle;
          pg.pivot.renderOrder = NUM_PAGES - i;
        }
      });

      let targetZ = p <= INTRO_END ? introCamZ : 
                    p < 0.94 ? 5.0 - (p - INTRO_END) * 0.4 : 
                    4.7 + (p - 0.94) * 20;

      camera.position.z += (clamp(targetZ, 4.5, 10) - camera.position.z) * 0.08;
      camera.position.y += (0.5 - camera.position.y) * 0.06;

      const scaleTarget = p <= INTRO_END ? introScale : 1.2;
      const currentScale = s.bookGroup.scale.x;
      s.bookGroup.scale.setScalar(currentScale + (clamp(scaleTarget, 1, 1.25) - currentScale) * 0.08);

      s.bookGroup.rotation.y = 0.18 + Math.sin(t * 0.4) * 0.01;
      s.bookGroup.rotation.x = -0.12 + Math.sin(t * 0.3) * 0.005;

      const fade = p > 0.96 ? 1 - clamp((p - 0.96) / 0.04, 0, 1) : 1;
      renderer.domElement.style.opacity = String(fade);

      camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    }
    tick();

    let resizeId = 0;
    const onResize = () => {
      cancelAnimationFrame(resizeId);
      resizeId = requestAnimationFrame(() => {
        const nw = el.clientWidth, nh = el.clientHeight;
        camera.aspect = nw / nh;
        camera.updateProjectionMatrix();
        renderer.setSize(nw, nh);
      });
    };
    window.addEventListener('resize', onResize);

    

    

    return () => {
      
      
      window.removeEventListener('resize', onResize);
      if (state.current) cancelAnimationFrame(state.current.raf);
      cancelAnimationFrame(resizeId);
      renderer.dispose();
      if (el.contains(renderer.domElement)) el.removeChild(renderer.domElement);
    };
  }, [t]);

  return <div ref={mountRef} className="book-canvas" />;
});

BookScene.displayName = 'BookScene';
export default BookScene;
