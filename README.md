# Fabric Data Platform Reference

A practical reference architecture for building a modern data platform on Microsoft Fabric.

## What you'll find here
- Lakehouse zones (Bronze / Silver / Gold)
- Governance & security foundations
- Naming conventions & folder structure
- Deployment notes and operational considerations

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Microsoft Fabric Platform                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Bronze     │───▶│    Silver    │───▶│     Gold     │      │
│  │  (Raw Data)  │    │  (Cleansed)  │    │  (Curated)   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                    │              │
│         └────────────────────┴────────────────────┘              │
│                              │                                    │
│                    ┌─────────▼──────────┐                        │
│                    │  Governance Layer  │                        │
│                    │  - Security        │                        │
│                    │  - Lineage         │                        │
│                    │  - Quality         │                        │
│                    └────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

## How to use
- Read `/docs/architecture.md` for detailed architecture overview
- Check `/examples` for sample pipelines and patterns
- Review lakehouse zones in `/lakehouse` directory

## Repository Structure

```
fabric-data-platform-reference/
├── docs/                    # Documentation
│   ├── architecture.md      # Architecture overview
│   ├── lakehouse-zones.md   # Bronze/Silver/Gold details
│   ├── governance-security.md
│   ├── naming-conventions.md
│   └── deployment.md
├── examples/                # Sample implementations
│   ├── pipelines/          # Data pipeline examples
│   └── notebooks/          # Notebook examples
└── lakehouse/              # Lakehouse structure
    ├── bronze/             # Raw data layer
    ├── silver/             # Cleansed data layer
    └── gold/               # Curated data layer
```

## Quick Start

1. Review the [Architecture Documentation](/docs/architecture.md)
2. Understand the [Lakehouse Zones](/docs/lakehouse-zones.md)
3. Follow [Naming Conventions](/docs/naming-conventions.md)
4. Explore [Examples](/examples)

## Contributing

This is a reference architecture. Adapt it to your specific needs and organizational requirements.

## License

See LICENSE file for details.