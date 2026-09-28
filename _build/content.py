"""
All of the site's words live here. Edit this file, then run:

    python _build/build.py

to regenerate index.html, resume.html, 404.html and projects/*.html.

Text fields may contain simple inline HTML (<strong>, <em>, <a>).
"""

SITE = {
    "name": "James Kurtis",
    "first": "James",
    "last": "Kurtis",
    "title": "Mechanical Engineering @ Cornell",
    "url": "https://jjk349.github.io/",
    "description": (
        "James Kurtis is a Mechanical Engineering student at Cornell University and "
        "Cooling Sub-team Lead for Cornell Racing FSAE, designing cooling, battery, and "
        "high-voltage systems for an electric race car."
    ),
    "lede": (
        "Cooling Sub-team Lead at Cornell Racing FSAE. I design, build, and test the "
        "systems that keep an electric race car cool, light, and safe."
    ),
    "location": "Ithaca, NY",
    "availability": "Available May&ndash;Aug 2027",
    "email": "jjk349@cornell.edu",
    "linkedin": "https://www.linkedin.com/in/James-Kurtis",
    "resume_pdf": "assets/resume/James-Kurtis-Resume.pdf",
    "photo": "assets/img/profile.jpg",
    "class_year": "28",
}

# The status bar across the top of the hero "dash".
DASH_BAR = [
    ("Car", "Cornell Racing FSAE"),
    ("Driver", "J. Kurtis"),
    ("Role", "Cooling Sub-team Lead"),
]

# Readouts along the bottom of the hero "dash".
#   type "gauge":   arc gauge; "fill" is how much of the arc is lit (0-1)
#   type "digital": big number readout
#   type "status":  status light + text
GAUGES = [
    {
        "type": "gauge",
        "label": "Battery container mass",
        "value": "&minus;1.0",
        "unit": "kg vs. previous design",
        "fill": 0.90,
        "note": "90% of previous mass",
    },
    {"type": "digital", "label": "Sub-team", "value": "5", "unit": "person cooling team, lead"},
    {"type": "digital", "label": "Projects", "value": "auto", "unit": "on this site"},  # "auto" = count
    {"type": "status", "label": "Status", "value": "Available", "unit": "May&ndash;Aug 2027"},
]

ABOUT = [
    "I&rsquo;m a Mechanical Engineering student at Cornell University, minoring in Business "
    "for Engineers. On Cornell Racing FSAE I lead the cooling sub-team, and my work on the "
    "team spans the car&rsquo;s cooling system, its high-voltage accumulator, and battery "
    "cell testing.",
    "Working hands-on where mechanical and electrical engineering meet has given me a "
    "particular interest in electric vehicles, and in the thermal and battery systems "
    "that make them work.",
]

INTERESTS = [
    "Formula One", "Electric Vehicles", "Mixed Martial Arts", "Karting",
    "Scuba Diving (PADI Advanced Open Water)", "Guitar",
]

# ---------------------------------------------------------------------------
# Projects
#
# status: "full"  -> gets a card that links to projects/<slug>.html
#         "stub"  -> card only, marked "In the garage / write-up coming soon".
#                    To publish it, switch to "full" and fill in the fields
#                    used by the full projects (lede, specs, sections, tools).
#
# art:     name of an SVG in _build/art/ used as the card + page illustration.
# gallery: optional list of photos for the project page, e.g.
#          {"src": "assets/img/projects/tbc-1.jpg", "alt": "...", "caption": "..."}
#          Put the image files in assets/img/projects/.
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "id": "fsae",
        "name": "Cornell FSAE Racing",
        "kicker": "Category 01",
        "intro": (
            "Cornell Racing designs, builds, and races an electric Formula SAE car. "
            "These are the systems I&rsquo;ve worked on across cooling, the high-voltage "
            "battery, and vehicle testing."
        ),
    },
    {
        "id": "other",
        "name": "Other Projects",
        "kicker": "Category 02",
        "intro": "Engineering work outside the race team.",
    },
]

PROJECTS = [
    {
        "slug": "cooling-system-architecture",
        "category": "fsae",
        "status": "full",
        "title": "Cooling System Architecture",
        "tags": ["Thermal", "Systems", "Leadership"],
        "art": "cooling",
        "readout": "5-person sub-team",
        "summary": (
            "Leading the design of the car&rsquo;s full liquid cooling loop, sized with a "
            "MATLAB flow model and checked against sensor data from the previous car."
        ),
        "lede": (
            "As cooling sub-team lead, I&rsquo;m responsible for the architecture of the "
            "liquid cooling loop on Cornell Racing&rsquo;s electric race car, and for making "
            "sure every part of it earns its weight."
        ),
        "specs": [
            ("Role", "Cooling Sub-team Lead"),
            ("Team", "5-person sub-team"),
            ("Tools", "MATLAB, flow &amp; temperature sensors"),
            ("Status", "Ongoing"),
        ],
        "stats": [
            ("5", "engineers on the sub-team"),
            ("MATLAB", "loop model for flow rate &amp; pressure drop"),
            ("T + Q", "temperature &amp; flow sensors on the previous car"),
        ],
        "sections": [
            {
                "title": "The problem",
                "body": [
                    "An electric powertrain still turns a real share of its energy into heat, "
                    "and that heat has to leave the car through coolant, pumps, hoses, and "
                    "radiators, all of which add mass. Oversize the system and the car is "
                    "heavy. Undersize it and components overheat before the end of an "
                    "endurance run. The goal is a loop that is just big enough.",
                ],
            },
            {
                "title": "What I did",
                "list": [
                    "Lead a five-person sub-team: I run weekly design meetings, delegate work, "
                    "and coordinate integration with the other sub-teams to build out the "
                    "full-car cooling infrastructure.",
                    "Built a MATLAB model of the car&rsquo;s liquid cooling loop that predicts "
                    "the flow rate each component needs and the pressure drop across it.",
                    "Use the model to give part designers optimized design targets, with the "
                    "aim of minimizing total system mass.",
                    "Fitted the previous car&rsquo;s cooling system with temperature and "
                    "flow-rate sensors to validate the team&rsquo;s design method against "
                    "endurance performance data.",
                ],
            },
            {
                "title": "Why it matters",
                "body": [
                    "Pairing a predictive model with measured data from the last car means "
                    "design targets are grounded in how the system actually behaved on track, "
                    "not only in how it was expected to behave.",
                ],
            },
        ],
        "tools": [
            "MATLAB", "Fluid Dynamics", "Heat Transfer", "Data Acquisition",
            "Systems Integration", "Team Leadership",
        ],
        "gallery": [],
    },
    {
        "slug": "tractive-battery-container",
        "category": "fsae",
        "status": "full",
        "title": "Tractive Battery Container",
        "tags": ["Structures", "Composites", "Manufacturing"],
        "art": "battery",
        "readout": "&minus;1.0 kg &nbsp;/&nbsp; &minus;10%",
        "summary": (
            "Redesigned and manufactured the container that holds the car&rsquo;s "
            "high-voltage battery, cutting 1&nbsp;kg (10%) from the previous design."
        ),
        "lede": (
            "The tractive battery container holds the car&rsquo;s high-voltage cells. I "
            "redesigned and manufactured it, taking 1&nbsp;kg, or 10%, out of the previous "
            "design."
        ),
        "specs": [
            ("Role", "Design &amp; manufacturing"),
            ("CAD", "Autodesk Inventor"),
            ("Material", "Composites"),
            ("Result", "&minus;1.0&nbsp;kg (&minus;10%)"),
        ],
        "stats": [
            ("&minus;1.0 kg", "lighter than the previous container"),
            ("&minus;10%", "of the previous design&rsquo;s mass"),
            ("GD&amp;T", "drawings for the battery mounting hardware"),
        ],
        "sections": [
            {
                "title": "The problem",
                "body": [
                    "The container is one of the most heavily regulated parts on an FSAE car. "
                    "It has to hold and protect the battery, meet the competition&rsquo;s "
                    "structural and safety rules, and mount solidly to the chassis. Every one "
                    "of those requirements pulls toward more material.",
                ],
            },
            {
                "title": "What I did",
                "list": [
                    "Redesigned the container through iterative modeling in Autodesk "
                    "Inventor, saving 1&nbsp;kg: 10% of the previous design&rsquo;s mass.",
                    "Pioneered the use of composite materials for the container on the team.",
                    "Created GD&amp;T-compliant engineering drawings for the battery "
                    "mounting hardware.",
                    "Machined clevises, bushings, and other aluminum mounting parts on a mill "
                    "and lathe.",
                    "Manufactured the redesigned container for the car.",
                ],
            },
        ],
        "tools": [
            "Autodesk Inventor", "Composites", "GD&amp;T", "Mill", "Lathe", "FSAE Rules",
        ],
        "gallery": [],
    },
    {
        "slug": "cg-height-test",
        "category": "fsae",
        "status": "stub",
        "title": "Center of Gravity Height Test",
        "tags": ["Vehicle Dynamics", "Testing"],
        "art": "cg",
        "summary": "Finding how high the car&rsquo;s center of gravity sits.",
    },
    {
        "slug": "low-voltage-box",
        "category": "fsae",
        "status": "full",
        "title": "Low Voltage Box",
        "tags": ["Packaging", "Prototyping"],
        "art": "lvbox",
        "readout": "CAD &rarr; print &rarr; car",
        "summary": (
            "Designed the ARG25 low-voltage enclosure in CAD and proved out its fit with "
            "3D-printed prototypes before building it for the car."
        ),
        "lede": (
            "The ARG25 low-voltage box houses the electronics that control and monitor the "
            "car&rsquo;s high-voltage system. I designed the enclosure and took it from CAD "
            "to the car."
        ),
        "specs": [
            ("Car", "ARG25"),
            ("Role", "Enclosure design"),
            ("Tools", "CAD, 3D printing"),
            ("Result", "Integrated on the car"),
        ],
        "stats": [],
        "sections": [
            {
                "title": "The problem",
                "body": [
                    "The box has to package a defined set of low-voltage electrical components "
                    "into the space available on the car.",
                ],
            },
            {
                "title": "What I did",
                "list": [
                    "Designed the enclosure in CAD around the required electrical components.",
                    "3D-printed prototypes to check fit and packaging before committing to "
                    "final parts.",
                    "Manufactured the final components and integrated them onto the car.",
                ],
            },
        ],
        "tools": ["CAD", "3D Printing", "Rapid Prototyping", "Packaging"],
        "gallery": [],
    },
    {
        "slug": "fireproof-composite-testing",
        "category": "fsae",
        "status": "stub",
        "title": "Fireproof Composite Testing",
        "tags": ["Materials", "Testing"],
        "art": "composite",
        "summary": "Evaluating the fire resistance of composite materials.",
    },
    {
        "slug": "dcir-cell-testing",
        "category": "fsae",
        "status": "full",
        "title": "DCIR Cell Testing",
        "tags": ["Batteries", "Testing"],
        "art": "dcir",
        "readout": "R = &Delta;V / &Delta;I",
        "summary": (
            "Measured the internal resistance of lithium-polymer pouch cells to quantify "
            "their heat generation and validate the pack, cooling, and BMS design."
        ),
        "lede": (
            "How much heat a battery cell makes depends on its internal resistance. I "
            "measured it on lithium-polymer pouch cells to validate the battery pack "
            "architecture, cooling, and BMS configuration."
        ),
        "specs": [
            ("Cells", "Lithium-polymer pouch"),
            ("Measured", "DC internal resistance"),
            ("Output", "Heat generation"),
            ("Informs", "Pack, cooling &amp; BMS"),
        ],
        "stats": [
            ("R = &Delta;V/&Delta;I", "internal resistance from a current step"),
            ("Q&#775; = I&sup2;R", "heat generated under load"),
        ],
        "sections": [
            {
                "title": "The idea",
                "body": [
                    "DCIR, or direct-current internal resistance, is found by stepping the "
                    "current through a cell and recording how far its voltage drops. The ratio "
                    "of the two is the cell&rsquo;s resistance, and the heat it produces under "
                    "load scales with I&sup2;R. That makes it the link between the "
                    "battery&rsquo;s electrical design and the cooling system that has to carry "
                    "the heat away.",
                ],
            },
            {
                "title": "What I did",
                "list": [
                    "Performed internal resistance testing on lithium-polymer pouch cells.",
                    "Used the results to quantify how much heat the cells generate.",
                    "Applied those numbers to validate the battery pack architecture, cooling, "
                    "and BMS configuration.",
                ],
            },
        ],
        "tools": ["Battery Testing", "Electrical Measurement", "Heat Generation", "BMS"],
        "gallery": [],
    },
    {
        "slug": "bike-frame-design",
        "category": "other",
        "status": "stub",
        "title": "Bike Frame Design",
        "tags": ["Design", "Structures"],
        "art": "bike",
        "summary": "Frame geometry and structural design for a bicycle.",
    },
]

# ---------------------------------------------------------------------------
# Experience, shown as a race "timing tower". Most relevant first.
# ---------------------------------------------------------------------------

EXPERIENCE = [
    {
        "org": "Cornell Racing FSAE",
        "role": "Cooling Sub-team Lead",
        "dates": "Oct 2024 &ndash; Present",
        "place": "Ithaca, NY",
        "points": [
            "Lead a 5-person cooling sub-team, hosting weekly design meetings, delegating "
            "tasks, and coordinating integration with other sub-teams to develop full-car "
            "cooling infrastructure.",
            "Built a MATLAB model of the liquid cooling loop to predict required flow rates and "
            "component pressure drops, giving part designers mass-optimized design targets.",
            "Fitted the previous cooling system with temperature and flow-rate sensors to "
            "validate the team&rsquo;s design method against endurance data.",
            "Redesigned and manufactured the tractive battery container, saving 1&nbsp;kg "
            "(10%) through iterative modeling in Autodesk Inventor.",
            "Created GD&amp;T-compliant drawings for battery mounting hardware and machined "
            "clevises, bushings, and aluminum parts on a mill and lathe.",
            "Performed internal resistance testing on lithium-polymer pouch cells to quantify "
            "heat generation, validating pack architecture, cooling, and BMS configuration.",
        ],
    },
    {
        "org": "Ametek Hughes-Treitler",
        "role": "Materials Management Intern",
        "dates": "Jun &ndash; Aug 2026",
        "place": "Garden City, NY",
        "points": [
            "Manufactured Inconel foil (laser cutting, stamping, cleaning) and assembled "
            "stacked-foil cores for 5 iterations of experimental micro-foil heat exchangers "
            "for performance and pressure testing.",
            "Reverse-engineered performance specifications (flow rate, pressure drop, heat "
            "rejection) from 20+ competitor direct-to-chip GPU cold plates, informing cold "
            "plate redesigns and next-gen targets.",
            "Built 6 Power BI and Excel tools consolidating sales, demand, and inventory data, "
            "aligning planning, purchasing, and manufacturing while saving planners about 3 "
            "hours per week.",
        ],
    },
    {
        "org": "Aesthetic Wrks",
        "role": "Car Detailing Apprentice",
        "dates": "Jun &ndash; Aug 2025",
        "place": "Hempstead, NY",
        "points": [
            "Shadowed technicians during automotive maintenance including oil changes, spark "
            "plug replacement, and basic diagnostics.",
            "Installed vinyl wraps and paint protection film and performed minor bodywork on "
            "high-performance and luxury vehicles.",
        ],
    },
]

LEADERSHIP = [
    {
        "org": "Varsity Wrestling, Xavier High School",
        "role": "Team Captain",
        "dates": "Nov 2022 &ndash; Feb 2024",
        "points": [
            "Elected by teammates to lead and instruct a 60-person team.",
            "Qualified for the CHSAA State Championship.",
        ],
    },
    {
        "org": "Valor Mixed Martial Arts",
        "role": "First Degree Black Belt",
        "dates": "2012 &ndash; Present",
        "points": [
            "Earned a 1st degree black belt in Kaju Bujutsu Kwai over 13 years of training.",
            "Mentored junior students and served on the leadership team.",
        ],
    },
]

EDUCATION = {
    "school": "Cornell University",
    "college": "College of Engineering",
    "degree": "B.S. Mechanical Engineering",
    "minor": "Business Minor for Engineers",
    "gpa": "3.68",
    "grad": "Expected May 2028",
    "courses": [
        "Differential Equations", "Statics &amp; Mechanics of Solids", "Dynamics",
        "Thermodynamics", "Intro to Mechanical Design", "Engineering Simulations &amp; Design",
        "Physics I&ndash;III", "System Dynamics", "Fluid Dynamics", "Mechanics of Materials",
    ],
}

SKILLS = [
    ("CAD / Simulation", ["ANSYS", "Autodesk Inventor", "Fusion 360", "Rhino 7"]),
    ("Manufacturing", [
        "Mill", "Lathe", "Laser Welding (Lightweld 2000XR)", "3D Printing", "Soldering",
        "GD&amp;T Drawings",
    ]),
    ("Programming &amp; Tools", [
        "Python", "MATLAB", "Excel", "Power BI", "Power Automate",
    ]),
]
