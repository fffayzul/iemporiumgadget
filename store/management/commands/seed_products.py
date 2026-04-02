from django.core.management.base import BaseCommand
from store.models import Category, Brand, Product


PRODUCTS = [

    # ── PHONES ──────────────────────────────────────────────────────────────
    {
        'category': 'Phones', 'brand': 'Apple', 'condition': 'new',
        'name': 'iPhone 15 Pro Max 256GB',
        'price': 1_850_000, 'compare_at_price': 2_100_000,
        'stock': 8, 'is_featured': True,
        'description': (
            'The iPhone 15 Pro Max features Apple\'s most powerful A17 Pro chip, '
            'a titanium design, and a 48MP main camera system with 5x optical zoom. '
            'The 6.7-inch Super Retina XDR display with ProMotion delivers stunning visuals. '
            'USB-C with USB 3 speeds. Action Button for instant access to your favourite features.'
        ),
        'specifications': (
            'Display: 6.7-inch Super Retina XDR, 2796×1290, 120Hz ProMotion\n'
            'Chip: A17 Pro\n'
            'Storage: 256GB\n'
            'Main Camera: 48MP, ƒ/1.78 aperture\n'
            'Telephoto: 12MP, 5x optical zoom\n'
            'Battery: Up to 29 hours video playback\n'
            'OS: iOS 17\n'
            'Connectivity: 5G, Wi-Fi 6E, Bluetooth 5.3, USB-C'
        ),
    },
    {
        'category': 'Phones', 'brand': 'Apple', 'condition': 'new',
        'name': 'iPhone 15 128GB',
        'price': 1_150_000, 'compare_at_price': None,
        'stock': 15, 'is_featured': True,
        'description': (
            'The iPhone 15 brings Dynamic Island to the standard lineup, '
            'a 48MP main camera with 2x optical-quality zoom, USB-C charging, '
            'and the powerful A16 Bionic chip in a colour-infused matte back design.'
        ),
        'specifications': (
            'Display: 6.1-inch Super Retina XDR, 2556×1179, 60Hz\n'
            'Chip: A16 Bionic\n'
            'Storage: 128GB\n'
            'Main Camera: 48MP, ƒ/1.6 aperture\n'
            'Battery: Up to 20 hours video playback\n'
            'OS: iOS 17\n'
            'Connectivity: 5G, Wi-Fi 6, Bluetooth 5.3, USB-C'
        ),
    },
    {
        'category': 'Phones', 'brand': 'Samsung', 'condition': 'new',
        'name': 'Samsung Galaxy S24 Ultra 256GB',
        'price': 1_620_000, 'compare_at_price': 1_850_000,
        'stock': 6, 'is_featured': True,
        'description': (
            'The Galaxy S24 Ultra is Samsung\'s most powerful smartphone, '
            'featuring the built-in S Pen, a 200MP camera with 10x optical zoom, '
            'and Galaxy AI features for real-time translation, chat assist, and more. '
            'The 6.8-inch QHD+ Dynamic AMOLED 2X display runs at 120Hz.'
        ),
        'specifications': (
            'Display: 6.8-inch QHD+ AMOLED 2X, 120Hz\n'
            'Chip: Snapdragon 8 Gen 3\n'
            'RAM: 12GB\n'
            'Storage: 256GB\n'
            'Main Camera: 200MP, ƒ/1.7\n'
            'Telephoto: 50MP 5x optical zoom\n'
            'Battery: 5000mAh, 45W wired charging\n'
            'OS: Android 14 / One UI 6.1\n'
            'S Pen: Included'
        ),
    },
    {
        'category': 'Phones', 'brand': 'Samsung', 'condition': 'new',
        'name': 'Samsung Galaxy S24 128GB',
        'price': 950_000, 'compare_at_price': None,
        'stock': 20, 'is_featured': False,
        'description': (
            'Galaxy S24 brings Galaxy AI to the everyday flagship. '
            'Slim and lightweight with a 6.2-inch Dynamic AMOLED 2X display, '
            '50MP camera, Snapdragon 8 Gen 3, and seven years of OS updates guaranteed.'
        ),
        'specifications': (
            'Display: 6.2-inch FHD+ AMOLED 2X, 120Hz\n'
            'Chip: Snapdragon 8 Gen 3\n'
            'RAM: 8GB\n'
            'Storage: 128GB\n'
            'Main Camera: 50MP, ƒ/1.8\n'
            'Battery: 4000mAh, 25W wired charging\n'
            'OS: Android 14 / One UI 6.1'
        ),
    },
    {
        'category': 'Phones', 'brand': 'Tecno', 'condition': 'new',
        'name': 'Tecno Phantom X2 Pro 5G 256GB',
        'price': 420_000, 'compare_at_price': 480_000,
        'stock': 12, 'is_featured': False,
        'description': (
            'The Tecno Phantom X2 Pro is Nigeria\'s premium affordable flagship, '
            'featuring a retractable portrait lens, Dimensity 9000 processor, '
            'and a 6.8-inch curved AMOLED display at 120Hz. 5G ready.'
        ),
        'specifications': (
            'Display: 6.8-inch AMOLED, 2400×1080, 120Hz\n'
            'Chip: MediaTek Dimensity 9000\n'
            'RAM: 12GB\n'
            'Storage: 256GB\n'
            'Retractable Portrait Lens: 50MP\n'
            'Battery: 5160mAh, 45W fast charge\n'
            'OS: Android 13 / HiOS 12'
        ),
    },
    {
        'category': 'Phones', 'brand': 'Samsung', 'condition': 'used',
        'name': 'Samsung Galaxy S23 128GB (UK Used)',
        'price': 580_000, 'compare_at_price': None,
        'stock': 4, 'is_featured': False,
        'description': (
            'UK-used Samsung Galaxy S23 in excellent condition. '
            'Compact flagship with the Snapdragon 8 Gen 2, 50MP camera, '
            'and all-day battery. Comes with original charger.'
        ),
        'specifications': (
            'Display: 6.1-inch FHD+ AMOLED 2X, 120Hz\n'
            'Chip: Snapdragon 8 Gen 2\n'
            'RAM: 8GB\n'
            'Storage: 128GB\n'
            'Condition: UK Used — Grade A (minor signs of use)\n'
            'Includes: Charger, USB cable'
        ),
    },

    # ── LAPTOPS ─────────────────────────────────────────────────────────────
    {
        'category': 'Laptops', 'brand': 'Apple', 'condition': 'new',
        'name': 'MacBook Pro 14-inch M3 Pro 512GB',
        'price': 2_950_000, 'compare_at_price': None,
        'stock': 5, 'is_featured': True,
        'description': (
            'The MacBook Pro 14-inch with M3 Pro delivers exceptional performance '
            'for professionals. The stunning Liquid Retina XDR display, up to 22 hours '
            'battery life, and a powerful 12-core CPU make it perfect for video editing, '
            '3D design, and heavy development workloads.'
        ),
        'specifications': (
            'Chip: Apple M3 Pro, 12-core CPU, 18-core GPU\n'
            'RAM: 18GB Unified Memory\n'
            'Storage: 512GB SSD\n'
            'Display: 14.2-inch Liquid Retina XDR, 3024×1964, 120Hz ProMotion\n'
            'Battery: Up to 22 hours\n'
            'Ports: 3× Thunderbolt 4, HDMI, SD card, MagSafe 3\n'
            'OS: macOS Sonoma'
        ),
    },
    {
        'category': 'Laptops', 'brand': 'Apple', 'condition': 'new',
        'name': 'MacBook Air 15-inch M2 256GB',
        'price': 1_950_000, 'compare_at_price': 2_200_000,
        'stock': 7, 'is_featured': False,
        'description': (
            'The largest MacBook Air ever with a stunning 15.3-inch Liquid Retina display '
            'and the powerful M2 chip. Fanless, silent design with all-day battery and '
            'a MagSafe charging port. Perfect for students and creative professionals.'
        ),
        'specifications': (
            'Chip: Apple M2, 8-core CPU, 10-core GPU\n'
            'RAM: 8GB Unified Memory\n'
            'Storage: 256GB SSD\n'
            'Display: 15.3-inch Liquid Retina, 2880×1864, 60Hz\n'
            'Battery: Up to 18 hours\n'
            'Ports: 2× Thunderbolt / USB-4, MagSafe 3\n'
            'OS: macOS Sonoma'
        ),
    },
    {
        'category': 'Laptops', 'brand': 'Dell', 'condition': 'new',
        'name': 'Dell XPS 15 Core i7 512GB',
        'price': 2_100_000, 'compare_at_price': 2_400_000,
        'stock': 4, 'is_featured': True,
        'description': (
            'The Dell XPS 15 is a powerhouse Windows laptop with a gorgeous OLED touchscreen, '
            'Intel Core i7-13700H, NVIDIA GeForce RTX 4060, and 16GB DDR5 RAM. '
            'Ideal for content creators, developers, and power users who need Windows.'
        ),
        'specifications': (
            'CPU: Intel Core i7-13700H (14 cores)\n'
            'GPU: NVIDIA GeForce RTX 4060 8GB\n'
            'RAM: 16GB DDR5\n'
            'Storage: 512GB NVMe SSD\n'
            'Display: 15.6-inch OLED 3.5K Touchscreen, 60Hz\n'
            'Battery: 86Wh, up to 13 hours\n'
            'OS: Windows 11 Home'
        ),
    },
    {
        'category': 'Laptops', 'brand': 'HP', 'condition': 'new',
        'name': 'HP Pavilion 15 Core i5 512GB',
        'price': 890_000, 'compare_at_price': None,
        'stock': 10, 'is_featured': False,
        'description': (
            'The HP Pavilion 15 offers excellent value for students and office users. '
            'Intel Core i5-1335U, 8GB RAM, and a 512GB SSD deliver smooth everyday performance. '
            'The Full HD IPS display and backlit keyboard make it great for work and study.'
        ),
        'specifications': (
            'CPU: Intel Core i5-1335U (10 cores)\n'
            'GPU: Intel Iris Xe Graphics\n'
            'RAM: 8GB DDR4\n'
            'Storage: 512GB SSD\n'
            'Display: 15.6-inch FHD IPS, 1920×1080\n'
            'Battery: Up to 8 hours\n'
            'OS: Windows 11 Home'
        ),
    },
    {
        'category': 'Laptops', 'brand': 'Lenovo', 'condition': 'used',
        'name': 'Lenovo ThinkPad X1 Carbon Gen 11 (UK Used)',
        'price': 1_250_000, 'compare_at_price': None,
        'stock': 3, 'is_featured': False,
        'description': (
            'UK-used ThinkPad X1 Carbon Gen 11 — one of the best business laptops ever made. '
            'Ultra-lightweight at just 1.12kg, Intel Core i7-1365U, 16GB LPDDR5 RAM, '
            '512GB SSD, and a stunning 2.8K OLED display. Grade A condition.'
        ),
        'specifications': (
            'CPU: Intel Core i7-1365U (10 cores)\n'
            'RAM: 16GB LPDDR5\n'
            'Storage: 512GB SSD\n'
            'Display: 14-inch 2.8K OLED, 2880×1800, 90Hz\n'
            'Weight: 1.12kg\n'
            'Condition: UK Used — Grade A\n'
            'Battery: Up to 15 hours\n'
            'OS: Windows 11 Pro'
        ),
    },

    # ── DRONE CAMERAS ────────────────────────────────────────────────────────
    {
        'category': 'Drone Cameras', 'brand': 'DJI', 'condition': 'new',
        'name': 'DJI Mini 4 Pro Fly More Combo',
        'price': 890_000, 'compare_at_price': 980_000,
        'stock': 6, 'is_featured': True,
        'description': (
            'The DJI Mini 4 Pro weighs under 249g, requiring no registration in most regions. '
            'Shoot 4K/60fps HDR video with a 1/1.3-inch CMOS sensor, omnidirectional obstacle sensing, '
            'and up to 34 minutes flight time. The Fly More Combo includes 3 batteries and a charging hub.'
        ),
        'specifications': (
            'Weight: 249g\n'
            'Sensor: 1/1.3-inch CMOS, 48MP\n'
            'Video: 4K/60fps HDR, 4K/100fps\n'
            'Max Flight Time: 34 minutes\n'
            'Max Range: 20km (O4 transmission)\n'
            'Obstacle Sensing: Omnidirectional\n'
            'Includes: 3 batteries, charging hub, shoulder bag, RC-N2 controller'
        ),
    },
    {
        'category': 'Drone Cameras', 'brand': 'DJI', 'condition': 'new',
        'name': 'DJI Air 3 Fly More Combo',
        'price': 1_380_000, 'compare_at_price': None,
        'stock': 4, 'is_featured': False,
        'description': (
            'The DJI Air 3 features a dual main camera system — a wide-angle and a 3x medium telephoto, '
            'both with large 1/1.3-inch CMOS sensors. Shoot 4K/60fps HDR on both cameras, '
            'up to 46 minutes flight time, and obstacle sensing in all directions.'
        ),
        'specifications': (
            'Sensor: Dual 1/1.3-inch CMOS\n'
            'Wide Camera: 24mm, 12MP\n'
            'Telephoto: 70mm 3× zoom, 12MP\n'
            'Video: 4K/60fps HDR (both cameras)\n'
            'Max Flight Time: 46 minutes\n'
            'Max Range: 20km\n'
            'Includes: 3 batteries, charging hub, bag, RC-N2 controller'
        ),
    },
    {
        'category': 'Drone Cameras', 'brand': 'DJI', 'condition': 'new',
        'name': 'DJI Mavic 3 Classic',
        'price': 2_050_000, 'compare_at_price': None,
        'stock': 2, 'is_featured': False,
        'description': (
            'The DJI Mavic 3 Classic brings the iconic Hasselblad camera to a more accessible price. '
            'The 4/3 CMOS Hasselblad sensor captures stunning 5.1K video and 20MP photos. '
            'Up to 46 minutes of flight time and 15km transmission range.'
        ),
        'specifications': (
            'Sensor: 4/3-inch CMOS Hasselblad L-Format\n'
            'Photo: 20MP\n'
            'Video: 5.1K/50fps, 4K/120fps\n'
            'Max Flight Time: 46 minutes\n'
            'Max Range: 15km\n'
            'Obstacle Sensing: Omnidirectional APAS 5.0\n'
            'Includes: RC-N1 controller, 1 battery'
        ),
    },

    # ── CONTENT CREATION KITS ────────────────────────────────────────────────
    {
        'category': 'Content Creation Kits', 'brand': 'Rode', 'condition': 'new',
        'name': 'Rode Wireless ME Dual Creator Kit',
        'price': 320_000, 'compare_at_price': 360_000,
        'stock': 8, 'is_featured': True,
        'description': (
            'The ultimate wireless microphone solution for creators. '
            'Two clip-on transmitters and a receiver that connects directly to your phone or camera. '
            'Up to 200m range, onboard recording backup, and automatic level control. '
            'Perfect for interviews, vlogs, and social media content.'
        ),
        'specifications': (
            'Microphones: 2× compact clip-on transmitters\n'
            'Range: Up to 200m\n'
            'Battery: 7 hours per transmitter\n'
            'Connection: 3.5mm TRS / USB-C\n'
            'Onboard Recording: 24-bit internal backup\n'
            'Compatible: iPhone, Android, DSLR, mirrorless cameras'
        ),
    },
    {
        'category': 'Content Creation Kits', 'brand': 'Elgato', 'condition': 'new',
        'name': 'Elgato Ring Light Pro Studio Kit',
        'price': 195_000, 'compare_at_price': 220_000,
        'stock': 10, 'is_featured': False,
        'description': (
            'Professional studio lighting setup for streamers and content creators. '
            'The 18-inch key light ring provides soft, flattering illumination. '
            'Includes a backdrop stand, phone holder, and Bluetooth remote. '
            'App-controlled via Elgato Control Center.'
        ),
        'specifications': (
            'Ring Light Diameter: 18 inches (46cm)\n'
            'Brightness: Up to 2900 lumens\n'
            'Colour Temperature: 2900K–7000K adjustable\n'
            'Control: Bluetooth app + physical remote\n'
            'Includes: Ring light, tripod stand, phone holder, backdrop mount\n'
            'Power: USB-C adapter included'
        ),
    },
    {
        'category': 'Content Creation Kits', 'brand': 'GoPro', 'condition': 'new',
        'name': 'GoPro HERO12 Black Creator Edition',
        'price': 580_000, 'compare_at_price': 650_000,
        'stock': 5, 'is_featured': True,
        'description': (
            'Everything you need to shoot, stabilise, and live stream right out of the box. '
            'The Creator Edition includes the HERO12 Black, a Media Mod with cold shoe and 3.5mm mic, '
            'a Light Mod, and a Display Mod. Shoot 5.3K60 video with HyperSmooth 6.0 stabilisation.'
        ),
        'specifications': (
            'Video: 5.3K60, 4K120, 2.7K240\n'
            'Photo: 27MP\n'
            'Stabilisation: HyperSmooth 6.0\n'
            'Waterproof: 10m without housing\n'
            'Battery: Up to 70 minutes at 5.3K\n'
            'Includes: HERO12, Media Mod, Light Mod, Display Mod, Enduro battery'
        ),
    },
    {
        'category': 'Content Creation Kits', 'brand': 'Elgato', 'condition': 'new',
        'name': 'Elgato Facecam Pro 4K Webcam Kit',
        'price': 210_000, 'compare_at_price': None,
        'stock': 7, 'is_featured': False,
        'description': (
            'The Elgato Facecam Pro shoots native 4K60 with a Sony STARVIS sensor — '
            'no compression, full RAW data stream via USB-C. Comes with a desk mount and '
            'full manual control over aperture, shutter speed, and ISO. '
            'Perfect for streamers, podcasters, and video call professionals.'
        ),
        'specifications': (
            'Resolution: 4K30 / 1080p60 uncompressed\n'
            'Sensor: 1/1.8-inch Sony STARVIS\n'
            'Field of View: 90° (adjustable 65°–90°)\n'
            'Connection: USB-C 3.0\n'
            'Includes: Desk mount, USB-C cable\n'
            'Software: Elgato Camera Hub (Windows/Mac)'
        ),
    },

    # ── ACCESSORIES ─────────────────────────────────────────────────────────
    {
        'category': 'Accessories', 'brand': 'Apple', 'condition': 'new',
        'name': 'Apple AirPods Pro 2nd Generation',
        'price': 310_000, 'compare_at_price': 350_000,
        'stock': 18, 'is_featured': True,
        'description': (
            'AirPods Pro (2nd gen) feature Apple\'s H2 chip, up to 2× more Active Noise '
            'Cancellation than the previous generation, Adaptive Audio that dynamically blends '
            'ANC and Transparency mode, and up to 30 hours total listening time with the case. '
            'MagSafe charging case with USB-C.'
        ),
        'specifications': (
            'Chip: Apple H2\n'
            'ANC: Active Noise Cancellation (2nd gen)\n'
            'Transparency Mode: Adaptive Audio\n'
            'Battery: 6 hours per charge, 30 hours with case\n'
            'Case: MagSafe + USB-C charging\n'
            'Connectivity: Bluetooth 5.3\n'
            'Water Resistance: IPX4 (earbuds + case)'
        ),
    },
    {
        'category': 'Accessories', 'brand': 'Samsung', 'condition': 'new',
        'name': 'Samsung Galaxy Buds2 Pro',
        'price': 165_000, 'compare_at_price': 190_000,
        'stock': 14, 'is_featured': False,
        'description': (
            'Galaxy Buds2 Pro offer exceptional 360 Audio with head tracking, '
            'intelligent ANC that reduces noise by up to 98%, and a compact ergonomic design. '
            '24-bit Hi-Fi audio for studio-quality sound in your ears. '
            'Compatible with all Android devices, not just Samsung.'
        ),
        'specifications': (
            'Audio: 24-bit Hi-Fi, 360 Audio with head tracking\n'
            'ANC: Up to 98% noise reduction\n'
            'Battery: 5 hours per charge, 18 hours with case\n'
            'Connectivity: Bluetooth 5.3\n'
            'Water Resistance: IPX7 (earbuds), IPX2 (case)\n'
            'Voice Detect: Auto switch on speech\n'
            'Case: Wireless charging'
        ),
    },
    {
        'category': 'Accessories', 'brand': 'Anker', 'condition': 'new',
        'name': 'Anker 737 Power Bank 24000mAh',
        'price': 68_000, 'compare_at_price': None,
        'stock': 30, 'is_featured': False,
        'description': (
            'The Anker 737 is a high-capacity 24000mAh power bank that can charge a MacBook, '
            'phone, and earbuds simultaneously. 140W total output with a smart LED display '
            'showing remaining charge percentage and input/output wattage in real time.'
        ),
        'specifications': (
            'Capacity: 24000mAh / 86.4Wh\n'
            'Output: 1× USB-C (140W), 1× USB-C (20W), 1× USB-A (12W)\n'
            'Total Output: 140W\n'
            'Recharge Time: 1.5 hours (via 140W charger)\n'
            'Display: Smart LED wattage + percentage screen\n'
            'Weight: 642g'
        ),
    },
    {
        'category': 'Accessories', 'brand': 'Logitech', 'condition': 'new',
        'name': 'Logitech MX Master 3S Wireless Mouse',
        'price': 72_000, 'compare_at_price': 85_000,
        'stock': 20, 'is_featured': False,
        'description': (
            'The MX Master 3S is the most advanced mouse Logitech makes. '
            '8K DPI performance, MagSpeed electromagnetic scroll wheel (1 second = 1000 lines), '
            'ultra-quiet clicks, and Logi Bolt wireless technology. Works with Mac and Windows.'
        ),
        'specifications': (
            'DPI: 200–8000 DPI (adjustable)\n'
            'Scroll Wheel: MagSpeed electromagnetic\n'
            'Battery: Rechargeable, up to 70 days\n'
            'Connectivity: Logi Bolt USB + Bluetooth\n'
            'Multi-Device: Up to 3 devices\n'
            'Compatible: Windows, macOS, Linux, ChromeOS'
        ),
    },
    {
        'category': 'Accessories', 'brand': 'Anker', 'condition': 'new',
        'name': 'Anker USB-C Hub 7-in-1',
        'price': 28_000, 'compare_at_price': None,
        'stock': 25, 'is_featured': False,
        'description': (
            'Expand your laptop\'s connectivity with this slim 7-in-1 USB-C hub. '
            '100W Power Delivery passthrough keeps your laptop charged while you use '
            '4K HDMI, USB-A 3.0, SD card, and microSD card slots simultaneously.'
        ),
        'specifications': (
            'Ports: 1× HDMI (4K@30Hz), 2× USB-A 3.0, 1× USB-C 3.0, 1× USB-C PD (100W), 1× SD, 1× microSD\n'
            'Power Delivery: 100W passthrough\n'
            'Compatibility: MacBook, iPad Pro, Windows laptops\n'
            'Dimensions: 110 × 33 × 13mm\n'
            'Cable: Built-in USB-C cable (22cm)'
        ),
    },

    # ── GAMING CONSOLE KITS ──────────────────────────────────────────────────
    {
        'category': 'Gaming Console Kits', 'brand': 'Sony', 'condition': 'new',
        'name': 'PlayStation 5 Disc Edition Bundle (2 Controllers + 2 Games)',
        'price': 750_000, 'compare_at_price': 850_000,
        'stock': 5, 'is_featured': True,
        'description': (
            'The ultimate PS5 starter bundle. Includes the PS5 Disc Edition console, '
            '2 DualSense wireless controllers, and 2 top-tier games (Spider-Man 2 + FIFA 24). '
            'Experience 4K gaming, ray tracing, haptic feedback, and adaptive triggers. '
            'Load games in seconds with the ultra-high-speed SSD.'
        ),
        'specifications': (
            'CPU: AMD Zen 2, 8 cores @ 3.5GHz\n'
            'GPU: AMD RDNA 2, 10.28 TFLOPS, 4K @ up to 120fps\n'
            'RAM: 16GB GDDR6\n'
            'Storage: 825GB Custom SSD (~5.5GB/s)\n'
            'Optical Drive: Yes (Blu-ray / DVD)\n'
            'Connectivity: Wi-Fi 6, Bluetooth 5.1, HDMI 2.1\n'
            'Includes: Console, 2× DualSense controller, Spider-Man 2, FIFA 24, cables'
        ),
    },
    {
        'category': 'Gaming Console Kits', 'brand': 'Sony', 'condition': 'new',
        'name': 'PlayStation 5 Digital Edition Slim',
        'price': 590_000, 'compare_at_price': None,
        'stock': 7, 'is_featured': False,
        'description': (
            'The new PS5 Slim Digital Edition is 30% smaller and lighter than the original PS5. '
            'All the same raw power — 4K gaming, ray tracing, haptic feedback — '
            'in a more compact, sleek design. No disc drive, play games downloaded from PS Store.'
        ),
        'specifications': (
            'CPU: AMD Zen 2, 8 cores @ 3.5GHz\n'
            'GPU: AMD RDNA 2, 10.28 TFLOPS\n'
            'RAM: 16GB GDDR6\n'
            'Storage: 1TB Custom SSD\n'
            'Optical Drive: No (Digital Edition)\n'
            'Connectivity: Wi-Fi 6, Bluetooth 5.1, HDMI 2.1\n'
            'Size: 30% smaller than original PS5'
        ),
    },
    {
        'category': 'Gaming Console Kits', 'brand': 'Microsoft', 'condition': 'new',
        'name': 'Xbox Series X Bundle (2 Controllers + 3 Month Game Pass)',
        'price': 720_000, 'compare_at_price': 800_000,
        'stock': 4, 'is_featured': True,
        'description': (
            'The most powerful Xbox ever. The Series X delivers true 4K gaming at 60fps, '
            'with select titles running at 4K/120fps. Includes an extra Xbox controller '
            'and 3 months of Xbox Game Pass Ultimate — access 100+ games instantly.'
        ),
        'specifications': (
            'CPU: AMD Zen 2, 8 cores @ 3.8GHz\n'
            'GPU: AMD RDNA 2, 12 TFLOPS\n'
            'RAM: 16GB GDDR6\n'
            'Storage: 1TB Custom NVMe SSD\n'
            'Optical Drive: Yes (4K Blu-ray)\n'
            'Connectivity: Wi-Fi 5, Bluetooth, HDMI 2.1\n'
            'Includes: Console, 2× controllers, 3-month Game Pass Ultimate code'
        ),
    },
    {
        'category': 'Gaming Console Kits', 'brand': 'Nintendo', 'condition': 'new',
        'name': 'Nintendo Switch OLED White Set',
        'price': 370_000, 'compare_at_price': 420_000,
        'stock': 8, 'is_featured': False,
        'description': (
            'The Nintendo Switch OLED features a vibrant 7-inch OLED screen, '
            'a wide adjustable stand for tabletop play, and a wired LAN port for stable online gaming. '
            'Play at home on your TV or take it anywhere — the Switch does it all.'
        ),
        'specifications': (
            'Display: 7-inch OLED, 1280×720\n'
            'TV Output: Up to 1080p\n'
            'Battery: 4.5–9 hours depending on game\n'
            'Storage: 64GB internal (expandable via microSD)\n'
            'Controllers: 2× Joy-Con (left + right)\n'
            'Connectivity: Wi-Fi, Bluetooth 4.1, USB-C, LAN (via dock)\n'
            'Includes: Console, dock with LAN port, 2× Joy-Con, Joy-Con grip, HDMI cable, AC adapter'
        ),
    },
    {
        'category': 'Gaming Console Kits', 'brand': 'Sony', 'condition': 'used',
        'name': 'PlayStation 4 Pro 1TB (UK Used)',
        'price': 210_000, 'compare_at_price': None,
        'stock': 3, 'is_featured': False,
        'description': (
            'UK-used PS4 Pro in very good condition. Play thousands of PS4 titles '
            'with enhanced 4K and HDR visuals. Comes with 1 DualShock 4 controller '
            'and all necessary cables. Great entry-level gaming at a fraction of PS5 price.'
        ),
        'specifications': (
            'CPU: AMD Jaguar, 8 cores @ 2.1GHz\n'
            'GPU: 4.2 TFLOPS\n'
            'RAM: 8GB GDDR5\n'
            'Storage: 1TB HDD\n'
            'Condition: UK Used — Grade A/B\n'
            'Includes: Console, 1× DualShock 4, HDMI cable, power cable'
        ),
    },
]

BRANDS = ['Apple', 'Samsung', 'Tecno', 'Dell', 'HP', 'Lenovo', 'DJI', 'Rode', 'Elgato', 'GoPro', 'Anker', 'Logitech', 'Sony', 'Microsoft', 'Nintendo']


class Command(BaseCommand):
    help = 'Seed demo inventory for iEmporium Gadgets'

    def handle(self, *args, **options):
        self.stdout.write('Creating brands...')
        brand_map = {}
        for name in BRANDS:
            b, _ = Brand.objects.get_or_create(name=name)
            brand_map[name] = b

        self.stdout.write('Creating categories...')
        cat_map = {}
        for cat_name in ['Phones', 'Laptops', 'Drone Cameras', 'Content Creation Kits', 'Accessories', 'Gaming Console Kits']:
            c, _ = Category.objects.get_or_create(name=cat_name)
            cat_map[cat_name] = c

        self.stdout.write('Creating products...')
        created = 0
        for p in PRODUCTS:
            _, made = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': cat_map[p['category']],
                    'brand': brand_map.get(p['brand']),
                    'condition': p['condition'],
                    'price': p['price'],
                    'compare_at_price': p.get('compare_at_price'),
                    'stock': p['stock'],
                    'low_stock_threshold': 3,
                    'is_featured': p.get('is_featured', False),
                    'is_active': True,
                    'description': p['description'],
                    'specifications': p['specifications'],
                },
            )
            if made:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created} products across {len(cat_map)} categories and {len(brand_map)} brands.'
        ))
        self.stdout.write(self.style.WARNING(
            '\nNote: No images have been added — upload product photos via /admin/store/product/'
        ))
