        // --- PAGE TRANSITIONS ---
        document.addEventListener('DOMContentLoaded', () => {
            const transitionOverlay = document.getElementById('page-transition');
            setTimeout(() => {
                transitionOverlay.classList.add('fade-out');
            }, 100);
        });

        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            // Intercept internal links ending in .html
            if (link && link.href && link.getAttribute('href').endsWith('.html')) {
                e.preventDefault();
                const targetUrl = link.getAttribute('href');
                const transitionOverlay = document.getElementById('page-transition');
                transitionOverlay.classList.remove('fade-out'); // Fade in
                
                setTimeout(() => {
                    window.location.href = targetUrl;
                }, 500); // Wait for transition before navigating
            }
        });

        // --- GLOBAL AVATAR SYNC ---
        function generateInitialsAvatarUrl(firstName, lastName) {
            const fullName = `${(firstName || '').trim()} ${(lastName || '').trim()}`.trim();
            if(!fullName) return `https://ui-avatars.com/api/?name=System+User&background=a200ff&color=fff&bold=true`;
            return `https://ui-avatars.com/api/?name=${encodeURIComponent(fullName)}&background=a200ff&color=fff&bold=true`;
        }

        function loadGlobalAvatar() {
            const avatarImg = document.getElementById('top-nav-avatar');
            const dropdownName = document.getElementById('dropdown-user-name');
            if (!avatarImg) return;

            const savedAvatar = localStorage.getItem('userAvatar');
            const firstName = localStorage.getItem('firstName');
            const lastName = localStorage.getItem('lastName');

            if (savedAvatar) {
                avatarImg.src = savedAvatar;
            } else if (firstName || lastName) {
                avatarImg.src = generateInitialsAvatarUrl(firstName, lastName);
            }

            if (dropdownName) {
                dropdownName.textContent = `${(firstName || '').trim()} ${(lastName || '').trim()}`.trim() || 'User';
            }
        }
        loadGlobalAvatar();

        // --- PROFILE DROPDOWN LOGIC ---
        const profileTrigger = document.getElementById('user-profile-trigger');
        const profileDropdown = document.getElementById('profile-dropdown');

        if (profileTrigger && profileDropdown) {
            profileTrigger.addEventListener('click', (e) => {
                e.stopPropagation();
                profileDropdown.classList.toggle('show');
            });

            document.addEventListener('click', (e) => {
                if (!profileTrigger.contains(e.target)) {
                    profileDropdown.classList.remove('show');
                }
            });
        }

        // --- DATA ---
        // This would come from a backend in a real application
        const knowledgeData = {
            nodes: [
                { id: 'ai_challenges', name: 'AI Daily Learning Challenges', mastery: 'unexplored', url: 'AIDailyChallenges.html', desc: 'Participate in dynamic AI-generated daily challenges to hone your skills.' },
                { id: 'dropout_risk', name: 'Dropout Risk Prediction', mastery: 'weak', url: 'DropoutRisk.html', desc: 'Identify factors affecting your engagement and get intelligent support interventions.' },
                { id: 'skill_gap', name: 'Skill Gap Analyzer', mastery: 'strong', url: 'SkillGap.html', desc: 'Analyze and bridge gaps in your learning path to achieve mastery.' },
                { id: 'voice_tutor', name: 'Multilingual Voice Tutor', mastery: 'unexplored', url: 'VoiceTutor.html', desc: 'Interact with your AI tutor via voice across multiple languages.' },
                { id: 'brain_map', name: 'Brain Map (Active)', mastery: 'strong', isRoot: true, url: 'Dashboard.html', desc: 'Central hub for monitoring your cognitive progression.' },
                { id: 'tasks', name: 'Tasks', mastery: 'weak', url: 'CompletedTasks.html', desc: 'Manage your active projects, daily goals, and completed assignments.' },
                { id: 'analytics', name: 'Analytics', mastery: 'unexplored', url: '#', desc: 'Deep dive into your performance metrics and learning trends.' },
                { id: 'settings', name: 'Settings', mastery: 'strong', url: '#', desc: 'Configure your Cognitive OS preferences and account details.' },
            ],
            links: [
                { source: 'brain_map', target: 'ai_challenges' },
                { source: 'brain_map', target: 'dropout_risk' },
                { source: 'brain_map', target: 'skill_gap' },
                { source: 'brain_map', target: 'voice_tutor' },
                { source: 'brain_map', target: 'tasks' },
                { source: 'brain_map', target: 'analytics' },
                { source: 'brain_map', target: 'settings' }
            ]
        };

        // --- CONFIGURATION ---
        const COLORS = {
            strong: new THREE.Color('#4caf50'),
            weak: new THREE.Color('#f44336'),
            unexplored: new THREE.Color('#9e9e9e'),
            line: new THREE.Color('#ffffff')
        };
        const SIZES = {
            strong: 0.3,
            weak: 0.2,
            unexplored: 0.15,
            root: 0.4
        };

        // --- UI ELEMENTS ---
        const detailPanel = document.getElementById('detail-panel');
        const detailTitle = document.getElementById('detail-title');
        const detailStatus = document.getElementById('detail-status');
        const detailContent = document.getElementById('detail-content');
        const closePanelBtn = document.getElementById('close-panel-btn');
        const tooltip = document.getElementById('tooltip');
        const aiPrompt = document.getElementById('ai-prompt');

        // --- 3D SCENE SETUP ---
        let scene, camera, renderer, controls;
        let nodes = {}, lines = {};
        let INTERSECTED, brainGroup;
        let nodeLabels = {};
        let particlesMesh;
        const particleData = [];
        let focusPulses = [];
        let activeExplosions = [];
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const clock = new THREE.Clock();

        // Zoom and animation state
        let isDetailView = false;
        let isZooming = false;
        const targetCameraPos = new THREE.Vector3();
        const targetControlsPos = new THREE.Vector3();
        let brainRotationY = 0;
        let brainBobTime = 0;

        // --- UI LOGIC ---
        const hamburgerBtn = document.getElementById('hamburger-btn');
        const mainSidebar = document.getElementById('main-sidebar');
        const sidebarOverlay = document.getElementById('sidebar-overlay');

        function toggleSidebar() {
            mainSidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('open');
        }
        hamburgerBtn.addEventListener('click', toggleSidebar);
        sidebarOverlay.addEventListener('click', toggleSidebar);

        // Generate Mock Calendar Heatmap
        let currentDisplayDate = new Date();
        const activityDataCache = {}; // Cache to store generated daily activity levels

        function renderCalendar(dateToDisplay) {
            const calendarGrid = document.getElementById('calendar-grid');
            calendarGrid.innerHTML = ''; // Clear previous days

            const today = new Date();
            const year = dateToDisplay.getFullYear();
            const month = dateToDisplay.getMonth();

            // Update title
            const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            document.getElementById('calendar-month-year').textContent = `${monthNames[month]} ${year}`;
            
            // Calculate the first day of the month
            const firstDay = new Date(year, month, 1);
            const startWeekday = firstDay.getDay(); // 0 (Sun) to 6 (Sat)
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            
            for (let i = 0; i < startWeekday; i++) {
                const emptyDay = document.createElement('div');
                emptyDay.className = 'cal-day';
                emptyDay.style.visibility = 'hidden'; // Keeps grid sizing
                calendarGrid.appendChild(emptyDay);
            }

            for (let i = 1; i <= daysInMonth; i++) {
                const targetDate = new Date(year, month, i);
                const day = document.createElement('div');
                day.className = 'cal-day';
                
                // Only assign mock activity to today or past days
                if (targetDate <= today) {
                    const dateKey = `${year}-${month}-${i}`; // Create a unique key for the day
                    let lvl = activityDataCache[dateKey];
                    
                    // Generate and cache if it doesn't exist yet
                    if (lvl === undefined) {
                        lvl = Math.floor(Math.random() * 5); // Random activity level 0-4
                        activityDataCache[dateKey] = lvl;
                    }

                    if (lvl > 0) day.classList.add(`lvl-${lvl}`);
                    const dateString = targetDate.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                    day.title = `${dateString}: ${lvl * 3} topics reviewed`;
                } else {
                    day.title = targetDate.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                }
                
                // Highlight today with a glowing border
                if (targetDate.toDateString() === today.toDateString()) {
                    day.style.border = '2px solid var(--primary-glow)';
                }

                day.textContent = i; // Show the day number inside the box
                calendarGrid.appendChild(day);
            }
        }

        // Initialize calendar
        renderCalendar(currentDisplayDate);

        // Calendar Navigation
        document.getElementById('prev-month').addEventListener('click', () => {
            currentDisplayDate.setMonth(currentDisplayDate.getMonth() - 1);
            renderCalendar(currentDisplayDate);
        });
        document.getElementById('next-month').addEventListener('click', () => {
            currentDisplayDate.setMonth(currentDisplayDate.getMonth() + 1);
            renderCalendar(currentDisplayDate);
        });

        // Search filtering
        document.getElementById('node-search').addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            
            // Filter sidebar list
            const listItems = document.querySelectorAll('#knowledge-list li');
            listItems.forEach(li => {
                const text = li.querySelector('span').textContent.toLowerCase();
                li.style.display = text.includes(term) ? 'flex' : 'none';
            });
        });

        // --- 3D SYSTEM ---
        const dailyFocusNodeId = 'brain_map';

        function init() {
            // Scene
            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0a0a1a, 0.1);

            // Camera
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 14; // Pull back slightly to fit the brain

            // Renderer
            const container = document.getElementById('three-canvas-container');
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
            container.appendChild(renderer.domElement);

            // Controls
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.minDistance = 3;
            controls.maxDistance = 20;

            // Lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
            scene.add(ambientLight);
            const pointLight = new THREE.PointLight(0xa200ff, 1, 100);
            pointLight.position.set(5, 5, 5);
            scene.add(pointLight);
            const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.5);
            scene.add(hemiLight);

            // Cinematic Rim Light to highlight the brain folds
            const rimLight = new THREE.SpotLight(0x00d4ff, 2);
            rimLight.position.set(0, 10, -10);
            rimLight.angle = Math.PI / 4;
            rimLight.penumbra = 0.5;
            scene.add(rimLight);

            // Group to hold the entire brain so it can rotate together
            brainGroup = new THREE.Group();
            scene.add(brainGroup);

            // Create Brain Shell
            createBrainShell();

            // Create Flowing Particles
            createParticles();

            // Create Graph
            createGraph();

            // Create Focus Beams
            createFocusBeams();

            // Event Listeners
            window.addEventListener('resize', onWindowResize);
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('click', onClick);
            closePanelBtn.addEventListener('click', hideDetailPanel);
            
            // Set AI prompt
            const focusNode = knowledgeData.nodes.find(n => n.id === dailyFocusNodeId);
            aiPrompt.innerHTML = `⚡ Today's neuron to strengthen: <strong>${focusNode.name}</strong>`;

            // Populate the Sidebar
            const listContainer = document.getElementById('knowledge-list');
            knowledgeData.nodes.forEach(nodeData => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>${nodeData.name}</span>
                    <span class="dot-indicator" style="background-color: ${COLORS[nodeData.mastery].getStyle()}"></span>
                `;
                li.addEventListener('click', () => {
                    if (isDetailView) hideDetailPanel();
                    setTimeout(() => {
                        INTERSECTED = nodes[nodeData.id];
                        onClick(); // Trigger the 3D click effect and zoom
                    }, isDetailView ? 300 : 0);
                });
                listContainer.appendChild(li);
            });
        }

        // Helper function to mathematically deform a sphere into a brain shape
        function deformToBrain(vec) {
            // Base proportions
            vec.z *= 1.25;
            
            // Sagittal Fissure (deep split down the middle)
            if (vec.y > -1.0) {
                const fissure = Math.exp(-(vec.x * vec.x) / 0.8); 
                vec.y -= fissure * 1.5; 
                vec.x += (vec.x > 0 ? 1 : (vec.x < 0 ? -1 : 0)) * fissure * 0.4;
            }
            
            // Temporal lobes (bulging lower sides)
            const temporalBulge = Math.exp(-((vec.y + 0.5)*(vec.y + 0.5) + (vec.z)*(vec.z)) / 3.0);
            vec.x += (vec.x > 0 ? 1 : -1) * temporalBulge * 0.5;

            // Flatten bottom
            if (vec.y < 0) vec.y *= 0.7;
            
            // Widen back (occipital lobe)
            if (vec.z < 0) vec.x *= 1.1;
            
            // Taper front (frontal lobe)
            if (vec.z > 0) vec.x *= 0.9;

            // Realistic organic brain folds (gyri and sulci) using pseudo-fractal noise
            const f1 = 2.5, f2 = 5.1, f3 = 8.3;
            let noise = Math.sin(vec.x * f1 + vec.z) * Math.cos(vec.y * f1 + vec.x) * Math.sin(vec.z * f1 + vec.y);
            noise += 0.5 * Math.sin(vec.x * f2 - vec.y) * Math.cos(vec.y * f2 + vec.z);
            noise += 0.25 * Math.sin(vec.x * f3) * Math.cos(vec.z * f3);

            // Subtracting the absolute value of the noise creates sharp, deep grooves (sulci) 
            // and smoothly rounded ridges (gyri) exactly like real biological tissue.
            const foldDepth = 0.12;
            const folds = 1 - Math.abs(noise) * foldDepth;
            vec.multiplyScalar(folds);
        }

        function createBrainShell() {
            const geometry = new THREE.SphereGeometry(6, 200, 200); // Ultra-high resolution for micro-folds
            const pos = geometry.attributes.position;
            const vec = new THREE.Vector3();
            
            for(let i = 0; i < pos.count; i++) {
                vec.fromBufferAttribute(pos, i);
                deformToBrain(vec);
                pos.setXYZ(i, vec.x, vec.y, vec.z);
            }
            geometry.computeVertexNormals();

            // Realistic Frosted Glass / Fleshy Volume
            const volumeMat = new THREE.MeshPhysicalMaterial({
                color: 0xd8b4fe, // Softer pinkish-purple base
                emissive: 0x220044,
                emissiveIntensity: 0.5,
                transparent: true,
                opacity: 0.85, // More opaque to catch highlights
                depthWrite: false,
                roughness: 0.2,
                metalness: 0.2,
                transmission: 0.9, // Glass refraction
                ior: 1.45, // Index of refraction closer to biological tissue
                thickness: 2.0,
                clearcoat: 1.0, // Wet/glossy look
                clearcoatRoughness: 0.1,
                wireframe: false
            });
            
            const brainVolume = new THREE.Mesh(geometry, volumeMat);
            brainGroup.add(brainVolume);
        }

        function createParticles() {
            const particlesCount = 800;
            const positions = new Float32Array(particlesCount * 3);
            const geometry = new THREE.BufferGeometry();

            for (let i = 0; i < particlesCount; i++) {
                const theta = Math.random() * Math.PI * 2;
                const phi = Math.acos((Math.random() * 2) - 1);
                const speed = 0.002 + Math.random() * 0.005; // Flow speed
                particleData.push({ theta, phi, speed });
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            const material = new THREE.PointsMaterial({
                color: 0xe0e6ff, // Light glowing particles
                size: 0.06,
                transparent: true,
                opacity: 0.6,
                blending: THREE.AdditiveBlending
            });

            particlesMesh = new THREE.Points(geometry, material);
            brainGroup.add(particlesMesh);
        }

        function createGraph() {
            const nodeMaterial = (color) => new THREE.MeshPhysicalMaterial({
                color: color,
                roughness: 0.15,
                metalness: 0.8,
                emissive: color,
                emissiveIntensity: 0.5,
                clearcoat: 1.0,
                clearcoatRoughness: 0.2
            });

            // Create Nodes (Neurons)
            knowledgeData.nodes.forEach((nodeData, i) => {
                const size = nodeData.isRoot ? SIZES.root : SIZES[nodeData.mastery] || 0.2;
                const geometry = new THREE.SphereGeometry(size, 32, 32);
                const material = nodeMaterial(COLORS[nodeData.mastery]);
                const sphere = new THREE.Mesh(geometry, material);

                if (nodeData.isRoot) {
                    sphere.position.set(0, 0, 0); // Root is dead center
                } else {
                    // Spread nodes inside the brain volume using a randomized spherical distribution
                    const radius = 2 + Math.random() * 3.5; 
                    const phi = Math.acos(-1 + (2 * i) / knowledgeData.nodes.length);
                    const theta = Math.sqrt(knowledgeData.nodes.length * Math.PI) * phi;
                    sphere.position.setFromSphericalCoords(radius, phi, theta);
                    deformToBrain(sphere.position); // Fit them into the brain lobes
                }
                
                sphere.userData = nodeData;
                brainGroup.add(sphere);
                nodes[nodeData.id] = sphere;

                // Create floating HTML label
                const label = document.createElement('div');
                label.className = 'node-label';
                label.textContent = nodeData.name;
                document.body.appendChild(label);
                nodeLabels[nodeData.id] = label;
            });

            // Create Links (Connections)
            knowledgeData.links.forEach(linkData => {
                const sourceNode = nodes[linkData.source];
                const targetNode = nodes[linkData.target];
                if (!sourceNode || !targetNode) return;

                const material = new THREE.LineDashedMaterial({
                    color: COLORS.line,
                    transparent: true,
                    opacity: 0.4,
                    dashSize: 0.2,
                    gapSize: 0.2
                });
                const geometry = new THREE.BufferGeometry().setFromPoints([sourceNode.position, targetNode.position]);
                const line = new THREE.Line(geometry, material);
                line.computeLineDistances();
                brainGroup.add(line);
                lines[`${linkData.source}-${linkData.target}`] = line;
            });
        }

        function createFocusBeams() {
            const focusNode = nodes[dailyFocusNodeId];
            if (!focusNode) return;

            // Find all connected links to the focus node
            knowledgeData.links.forEach(link => {
                if (link.source === dailyFocusNodeId || link.target === dailyFocusNodeId) {
                    const targetNodeId = link.source === dailyFocusNodeId ? link.target : link.source;
                    const targetNode = nodes[targetNodeId];

                    if (targetNode) {
                        // Create a bright glowing pulse
                        const geometry = new THREE.SphereGeometry(0.1, 16, 16);
                        const material = new THREE.MeshBasicMaterial({
                            color: 0xffffff,
                            transparent: true,
                            opacity: 0.9,
                            blending: THREE.AdditiveBlending // Makes it look intensely bright
                        });
                        const pulseMesh = new THREE.Mesh(geometry, material);
                        brainGroup.add(pulseMesh);

                        focusPulses.push({
                            mesh: pulseMesh,
                            startPos: focusNode.position,
                            endPos: targetNode.position,
                            progress: Math.random(), // Stagger the start times
                            speed: 0.005 + Math.random() * 0.015 // Randomize speeds slightly
                        });
                    }
                }
            });
        }

        function explodeNode(nodeMesh) {
            const particleCount = 60;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const velocities = [];

            // Get the current world position of the node
            const nodeWorldPos = new THREE.Vector3();
            nodeMesh.getWorldPosition(nodeWorldPos);

            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] = nodeWorldPos.x;
                positions[i * 3 + 1] = nodeWorldPos.y;
                positions[i * 3 + 2] = nodeWorldPos.z;

                // Generate a random outward trajectory
                const velocity = new THREE.Vector3(
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2
                ).normalize().multiplyScalar(0.05 + Math.random() * 0.1);
                velocities.push(velocity);
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

            const material = new THREE.PointsMaterial({
                color: nodeMesh.material.color, // Inherit node color
                size: 0.15,
                transparent: true,
                opacity: 1,
                blending: THREE.AdditiveBlending // Glow effect
            });

            const particleMesh = new THREE.Points(geometry, material);
            scene.add(particleMesh);

            activeExplosions.push({
                mesh: particleMesh,
                velocities: velocities,
                life: 1.0 // Life tracker to handle fading out
            });
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function onMouseMove(event) {
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

            tooltip.style.left = event.clientX + 15 + 'px';
            tooltip.style.top = event.clientY + 'px';
        }

        function onClick() {
            if (INTERSECTED && !isDetailView) {
                showDetailPanel(INTERSECTED.userData);
                isDetailView = true;
                isZooming = true;
                controls.enabled = false; // Disable orbit controls during transition

                // Get absolute world position of the clicked node
                const nodeWorldPos = new THREE.Vector3();
                INTERSECTED.getWorldPosition(nodeWorldPos);

                // Trigger the explosion effect
                explodeNode(INTERSECTED);

                targetControlsPos.copy(nodeWorldPos);
                
                // Calculate new camera position (pushing out from center)
                const direction = nodeWorldPos.clone().normalize();
                if (direction.lengthSq() === 0) direction.set(0, 0, 1);
                targetCameraPos.copy(nodeWorldPos).add(direction.multiplyScalar(4));
            }
        }

        function showDetailPanel(nodeData) {
            detailTitle.textContent = nodeData.name;
            detailStatus.textContent = nodeData.mastery;
            detailStatus.style.backgroundColor = COLORS[nodeData.mastery].getStyle();
            detailStatus.style.color = nodeData.mastery === 'unexplored' ? 'black' : 'white';
            
            detailContent.innerHTML = `
                <p style="margin-top: 15px; font-size: 1.1em; color: #ddd;">${nodeData.desc}</p>
                <div style="margin-top: 30px; text-align: center;">
                    <a href="${nodeData.url}" class="nav-action-btn">Launch ${nodeData.name.replace(' (Active)', '')}</a>
                </div>
            `;

            detailPanel.classList.add('visible');
        }

        function hideDetailPanel() {
            detailPanel.classList.remove('visible');
            isDetailView = false;
            isZooming = true;
            controls.enabled = false;

            targetControlsPos.set(0, 0, 0);
            
            // Zoom back out to distance 14 while keeping current viewing angle
            const direction = camera.position.clone().normalize();
            if (direction.lengthSq() === 0) direction.set(0, 0, 1);
            targetCameraPos.copy(direction.multiplyScalar(14));
        }

        function animate() {
            requestAnimationFrame(animate);
            const elapsedTime = clock.getElapsedTime();

            // Raycasting for hover/interaction
            raycaster.setFromCamera(mouse, camera);
            const intersects = isDetailView ? [] : raycaster.intersectObjects(Object.values(nodes));

            if (intersects.length > 0) {
                if (INTERSECTED != intersects[0].object) {
                    if (INTERSECTED) INTERSECTED.material.emissiveIntensity = 0.2;
                    INTERSECTED = intersects[0].object;
                    INTERSECTED.material.emissiveIntensity = 0.6;
                    tooltip.style.display = 'block';
                    tooltip.textContent = INTERSECTED.userData.name;
                }
                document.body.style.cursor = 'pointer';
            } else {
                if (INTERSECTED) INTERSECTED.material.emissiveIntensity = 0.2;
                INTERSECTED = null;
                tooltip.style.display = 'none';
                document.body.style.cursor = 'default';
            }

            // Handle search bar highlight effects for nodes
            const searchTerm = document.getElementById('node-search').value.toLowerCase();
            if (searchTerm !== "") {
                Object.values(nodes).forEach(node => {
                    if (node.userData.name.toLowerCase().includes(searchTerm)) {
                        node.material.emissiveIntensity = 0.8;
                        node.scale.set(1.5, 1.5, 1.5);
                    } else {
                        node.material.emissiveIntensity = 0.1; // dim others
                        node.scale.set(1, 1, 1);
                    }
                });
            } else if (!INTERSECTED && !isDetailView) {
                // Reset when search is cleared
                Object.values(nodes).forEach(node => {
                    if (node.id !== dailyFocusNodeId) {
                        node.material.emissiveIntensity = 0.5;
                        node.scale.set(1, 1, 1);
                    }
                });
            }

            // Animate daily focus node
            const focusNodeMesh = nodes[dailyFocusNodeId];
            if (focusNodeMesh) {
                const pulse = 1 + 0.2 * Math.sin(elapsedTime * 5);
                focusNodeMesh.scale.set(pulse, pulse, pulse);
                focusNodeMesh.material.emissiveIntensity = 0.5 + 0.5 * Math.sin(elapsedTime * 5);
            }

            // Handle brain rotation & bobbing (pauses when detail panel is open)
            if (!isDetailView) {
                brainRotationY += 0.002;
                brainBobTime += 0.016;
            }
            brainGroup.rotation.y = brainRotationY;
            brainGroup.position.y = Math.sin(brainBobTime * 1.5) * 0.2;

            // Handle camera zoom transitions
            if (isZooming) {
                camera.position.lerp(targetCameraPos, 0.08);
                controls.target.lerp(targetControlsPos, 0.08);
                if (camera.position.distanceTo(targetCameraPos) < 0.1 && controls.target.distanceTo(targetControlsPos) < 0.1) {
                    isZooming = false;
                    controls.enabled = true; // Re-enable user interaction
                }
            }

            // Update 2D HTML labels for nodes
            Object.keys(nodes).forEach(id => {
                const node = nodes[id];
                const label = nodeLabels[id];
                
                if (label) {
                    const vector = new THREE.Vector3();
                    node.getWorldPosition(vector);
                    vector.project(camera);
                    
                    if (vector.z < 1 && vector.x > -1 && vector.x < 1 && vector.y > -1 && vector.y < 1) {
                        const x = (vector.x * 0.5 + 0.5) * window.innerWidth;
                        const y = -(vector.y * 0.5 - 0.5) * window.innerHeight;
                        label.style.left = `${x}px`;
                        label.style.top = `${y - 20}px`;
                        label.style.display = 'block';
                        
                        // Fade out labels if detail view is open and it's not the focused node
                        label.style.opacity = (isDetailView && INTERSECTED !== node) ? 0 : 0.9;
                    } else {
                        label.style.display = 'none';
                    }
                }
            });

            // Animate particles flowing along the brain shell
            if (particlesMesh) {
                const positions = particlesMesh.geometry.attributes.position.array;
                const vec = new THREE.Vector3();
                for (let i = 0; i < particleData.length; i++) {
                    const data = particleData[i];
                    data.theta += data.speed; // Flow continuously around the shell
                    
                    // Float slightly above the brain shell (radius 6.15 vs shell radius 6.0)
                    vec.setFromSphericalCoords(6.15, data.phi, data.theta);
                    deformToBrain(vec);

                    positions[i * 3] = vec.x;
                    positions[i * 3 + 1] = vec.y;
                    positions[i * 3 + 2] = vec.z;
                }
                particlesMesh.geometry.attributes.position.needsUpdate = true;
            }

            // Animate focus beams (bright pulses of light)
            focusPulses.forEach(pulse => {
                pulse.progress += pulse.speed;
                if (pulse.progress > 1) pulse.progress = 0; // Reset when it reaches the target
                
                pulse.mesh.position.lerpVectors(pulse.startPos, pulse.endPos, pulse.progress);
                
                // Scale the beam so it smoothly fades in at the start and out at the end
                const pulseIntensity = Math.sin(pulse.progress * Math.PI);
                pulse.mesh.scale.setScalar(pulseIntensity);
            });

            // Animate explosions
            for (let i = activeExplosions.length - 1; i >= 0; i--) {
                const explosion = activeExplosions[i];
                const positions = explosion.mesh.geometry.attributes.position.array;
                
                for (let j = 0; j < explosion.velocities.length; j++) {
                    positions[j * 3] += explosion.velocities[j].x;
                    positions[j * 3 + 1] += explosion.velocities[j].y;
                    positions[j * 3 + 2] += explosion.velocities[j].z;
                }
                
                explosion.mesh.geometry.attributes.position.needsUpdate = true;
                explosion.life -= 0.02; // Fade out gradually
                explosion.mesh.material.opacity = explosion.life;
                
                // Clean up when the explosion has faded
                if (explosion.life <= 0) {
                    scene.remove(explosion.mesh);
                    explosion.mesh.geometry.dispose();
                    explosion.mesh.material.dispose();
                    activeExplosions.splice(i, 1);
                }
            }

            // Animate data flowing through connections
            Object.values(lines).forEach(line => {
                line.material.dashOffset -= 0.02; // Creates the flow effect
            });

            controls.update();
            renderer.render(scene, camera);
        }

        init();
        animate();
