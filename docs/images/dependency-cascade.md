# Visual Dependency Cascade

## The User Experience: Error Chain
```mermaid
graph TD
    A[User: python ihm_validator.py] --> B{Import Check}
    B -->|Missing| C[Error: No module 'pdfkit']
    C --> D[User: pip install pdfkit]
    D --> E{Import Check}
    E -->|Missing| F[Error: No module 'bokeh']
    F --> G[User: pip install bokeh]
    G --> H{Import Check}
    H -->|Missing| I[Error: No module 'mendeleev']
    I --> J[User: pip install mendeleev]
    J --> K{Import Check}
    K -->|Version Conflict| L[Error: Bokeh API incompatible]
    L --> M[User: pip install bokeh==2.4.3]
    M --> N{Import Check}
    N -->|Version Conflict| O[Error: numpy.bool8 not found]
    O --> P[User gives up 😞]
    
    style C fill:#ff6b6b
    style F fill:#ff6b6b
    style I fill:#ff6b6b
    style L fill:#ff9f1c
    style O fill:#ff9f1c
    style P fill:#cc0000
```

## Discovered Dependency Tree
```mermaid
graph LR
    A[ihm_validator.py] --> B[pdfkit]
    A --> C[jinja2]
    A --> D[report.py]
    D --> E[mmcif_io]
    D --> F[excludedvolume]
    D --> G[get_plots]
    D --> H[sas]
    E --> I[utility ✓]
    E --> J[ihm]
    F --> K[mendeleev]
    G --> L[bokeh v2.4.3]
    H --> M[scipy]
    H --> N[numpy <2.4]
    G --> O[matplotlib]
    G --> P[plotly]
    
    style I fill:#51cf66
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    style J fill:#ff6b6b
    style K fill:#ff6b6b
    style L fill:#ff9f1c
    style M fill:#ff6b6b
    style N fill:#ff9f1c
    style O fill:#ff6b6b
    style P fill:#ff6b6b
```

**Legend:**
- 🔴 Red = Not documented (discovered through errors)
- 🟠 Orange = Version-critical (breaks with wrong version)
- 🟢 Green = Found in codebase
