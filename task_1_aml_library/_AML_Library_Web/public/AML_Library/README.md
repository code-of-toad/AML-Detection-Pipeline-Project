# AML Knowledge Library

## Overview

This library is a **standalone, comprehensive knowledge base** containing Money Laundering (ML) and Terrorist Financing (TF) red flags, indicators, and intelligence, with a special focus on **Organized Crime Groups (OCGs)**. 

**This library is an independent component** that can be used on its own for AML investigation, research, and reference purposes. It is also designed to facilitate downstream tasks such as detection model development and explainability, but it does not depend on those tasks and maintains its own complete value proposition.

## Purpose

This library serves as a **centralized, authoritative reference** for AML intelligence and can be used independently for:

### Standalone Use Cases
- **AML Investigation**: Quick reference for identifying suspicious patterns during investigations
- **Risk Assessment**: Understanding and evaluating AML risk indicators
- **Training and Education**: Learning about ML/TF typologies and red flags
- **Research and Analysis**: Source-backed intelligence for AML research
- **Compliance and Due Diligence**: Reference for compliance professionals

### Facilitation Use Cases (Optional)
The library is also designed to facilitate:
- **Model Development**: Support feature engineering and risk pattern understanding for detection models
- **Model Explainability**: Provide context and non-technical descriptions for explaining model decisions

**Note**: While the library facilitates these use cases, it remains a complete, independent knowledge base that does not require or depend on any downstream applications.

## Library Structure

```
AML_Library/
├── README.md (this file)
├── 00_COMPREHENSIVE_RED_FLAGS_MASTER.md ⭐ START HERE for quick reference
├── 01_Professional_Money_Laundering_Trade_MSB.md
├── 02_Bulk_Cash_Smuggling_Mexico_TCOs.md
├── 03_Oil_Smuggling_Mexico_Cartels.md
├── 04_Chinese_ML_Networks_Mexico_TCOs.md
├── 05_Synthetic_Opioids_Proceeds.md
├── 06_Underground_Banking_Schemes.md
├── 07_Human_Trafficking_Proceeds.md
├── 08_General_ML_TF_Indicators.md
├── Red_Flag_to_Feature_Mapping.md
└── SOURCES.md
```

### Quick Start

**For a comprehensive view of all red flags in one place**: See `00_COMPREHENSIVE_RED_FLAGS_MASTER.md`
- All 147+ red flags organized in tables
- Quick reference format
- Data signals and feature mappings included
- Easy navigation by category

**For detailed context and methodology**: See individual documents (01-08)
- In-depth explanations
- Risk assessment guidance
- High-risk combination indicators
- Full source citations

## Source Traceability

**CRITICAL**: Every red flag and indicator in this library includes:
- Source document (with URL)
- Publication date
- Document reference number (if applicable)
- Page/section reference (where applicable)

All sources are documented in `SOURCES.md` and cited inline throughout the library.

## Design Decisions and Methodology

### Design Philosophy
- **Standalone Independence**: The library is designed as a complete, self-contained knowledge base
- **Source Traceability**: Every red flag is traceable to authoritative sources (FINTRAC, FinCEN)
- **Clarity and Usability**: Emphasis on clear, non-technical descriptions accessible to all users
- **Structured Organization**: Consistent structure across all documents for easy navigation

### Methodology
1. **Source Selection**: Red flags extracted from 8 authoritative AML/ATF documents
2. **Categorization**: Organized by typology (Trade-based ML, Bulk Cash Smuggling, etc.)
3. **Standardization**: Consistent format across all red flags (Indicator, Data Signal, Feature Mapping, Source)
4. **Validation**: All red flags verified against source documents with full citations

### Dependencies and Assumptions
- **No External Dependencies**: The library is self-contained and does not require any external systems or data
- **Source Assumptions**: All red flags assume authoritative sources (FINTRAC, FinCEN) are current and valid
- **Format Assumptions**: Documents assume markdown format for maximum accessibility and portability

## How to Use This Library

### For Standalone Investigation Use
1. **Quick Reference**: See `00_COMPREHENSIVE_RED_FLAGS_MASTER.md` for all red flags in one place
2. **Detailed Analysis**: Review individual documents (01-08) for in-depth context on specific typologies
3. **Source Verification**: Check `SOURCES.md` for complete source information and traceability
4. **Pattern Identification**: Use red flag descriptions to identify suspicious patterns in transaction data

### For Model Development (Optional Facilitation)
1. **Feature Engineering**: See `Red_Flag_to_Feature_Mapping.md` to understand which features detect which red flags
2. **Risk Pattern Understanding**: Reference specific red flag documents to understand behavioral patterns
3. **Model Validation**: Use red flags as validation criteria to ensure flagged customers align with AML risks

### For Model Explainability (Optional Facilitation)
1. **Explanation Generation**: Use red flag descriptions to explain why customers were flagged
2. **Non-Technical Language**: Leverage clear, source-backed descriptions for user-friendly explanations
3. **Context Provision**: Reference detailed documents (01-08) for comprehensive context on red flags

## Library Independence

This library is designed as a **standalone, independent component**:

- ✅ **Self-Contained**: Complete knowledge base with all necessary information
- ✅ **No Dependencies**: Does not require any external systems, models, or data
- ✅ **Reproducible**: Can be generated from source documents independently
- ✅ **Portable**: Markdown format ensures maximum accessibility
- ✅ **Complete**: All red flags, sources, and mappings included

While the library can facilitate downstream tasks (detection models, explainability), it maintains complete independence and can be used, understood, and validated on its own.

## Data Sources

All red flags in this library are sourced from authoritative AML/ATF documents:
- FINTRAC (Financial Transactions and Reports Analysis Centre of Canada) Operational Alerts
- FinCEN (Financial Crimes Enforcement Network) Alerts and Advisories

Complete source information is available in `SOURCES.md`, and all red flags include inline source references for full traceability.

---

**Last Updated**: 2025-01-23  
**Status**: Complete and Standalone  
**Version**: 1.0

