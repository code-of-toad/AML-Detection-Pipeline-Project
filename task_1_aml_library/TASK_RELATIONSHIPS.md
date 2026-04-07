# Task Relationships: AML Library Foundation for Detection and Explainability

## Overview

This document summarizes the relationship between **Task 1 (AML Knowledge Library)** and the subsequent tasks: **Task 2 (Detection Model)** and **Task 3 (Explainability)**. 

**Important Note on Library Independence**: The AML Knowledge Library is a **standalone, independent component** that can be used on its own for AML investigation, research, and reference purposes. This document describes how the library can **facilitate** Tasks 2 and 3, but the library itself does not depend on those tasks and maintains complete independence. The library is designed to be self-contained, reproducible, and usable independently of any downstream applications.

---

## The Three Tasks

### Task 1: Building AML Knowledge Library ✅ (Current Status)
**Objective**: Build a comprehensive AML Knowledge Library containing ML/TF red flags, indicators, and intelligence, especially those related to Organized Crime Groups (OCGs).

**Status**: Complete - This directory contains the full knowledge library with 147+ red flags from 8 authoritative sources.

**Independence**: This library is a **standalone component** that:
- Can be used independently for AML investigation and research
- Does not require or depend on Tasks 2 or 3
- Is complete, self-contained, and reproducible on its own
- Is designed to facilitate (but not depend on) downstream tasks

### Task 2: Building Money Laundering Bad Actors Detection Model
**Objective**: Use AI and machine learning to identify customers for intensive investigation by extracting insights from provided data.

**Key Requirements**:
- Ensure flagged customers are relevant to AML risk identified in the AML Knowledge Library
- Detect suspicious actors by identifying behavioral patterns within their context
- Generalize to emerging or unlabeled patterns
- Address challenges such as label scarcity and data imbalance

### Task 3: Explaining Model Results in the Context of Red Flags and Indicators
**Objective**: Automate clear, non-technical explanations of AML risks in model outputs, showing why a customer was flagged or not, and how the decision was reached.

**Key Requirements**:
- Help understand why borderline cases are flagged/not flagged
- Use non-technical language for users without ML/AI knowledge
- Explore and evaluate different explainable ML techniques and interpretation methods

---

## Relationship: Task 1 → Task 2 (Detection Model)

### How the AML Library Enables the Detection Model

#### 1. **Feature Engineering Foundation**
The AML Library provides the critical link between AML knowledge and data features:

- **Red Flag to Feature Mapping**: The `Red_Flag_to_Feature_Mapping.md` document maps each red flag to:
  - **Data Signals**: What patterns in the data indicate this red flag
  - **Engineered Features**: Specific features to create for model detection
  - **Feature Categories**: How features group together

- **Example**: 
  - **Red Flag**: "Structured Cash Deposits" (from Bulk Cash Smuggling)
  - **Data Signal**: Multiple cash deposits $9K-$10K in quick succession
  - **Features**: `structured_cash_deposits_count`, `just_below_threshold_cash_deposits`, `rapid_cash_deposit_sequence`

#### 2. **Risk Pattern Understanding**
The library helps model developers understand:
- **What to look for**: Each red flag document explains the context and methodology
- **High-risk combinations**: Documents identify which red flags often appear together
- **Pattern recognition**: Understanding of behavioral patterns that indicate money laundering

#### 3. **Model Validation and Relevance**
**Critical Requirement**: "Ensure flagged customers are relevant to AML risk identified in the AML Knowledge Library"

- The library provides the **ground truth** for what constitutes AML risk
- Model outputs must align with red flags documented in the library
- Risk scores should reflect the severity and type of red flags present
- The `00_COMPREHENSIVE_RED_FLAGS_MASTER.md` serves as a validation checklist

#### 4. **Feature Engineering Priority**
The library guides feature engineering priorities:
- **High Priority**: Wire transfers, geographic risk, flow-through velocity (critical red flags)
- **Medium Priority**: Time-based patterns, channel-specific features
- **Lower Priority**: Supporting indicators like round numbers

#### 5. **Addressing Data Challenges**
The library helps address label scarcity and data imbalance:
- **Unlabeled pattern detection**: Red flags help identify suspicious patterns even without labels
- **Context-aware features**: Understanding red flag context helps create features that generalize
- **Risk-based sampling**: Library knowledge can guide sampling strategies for imbalanced data

---

## Relationship: Task 1 → Task 3 (Explainability)

### How the AML Library Enables Model Explainability

#### 1. **Non-Technical Explanation Framework**
The library provides the language and context for explaining model decisions:

- **Red Flag Descriptions**: Each red flag includes clear, non-technical descriptions of what it means
- **Context and Methodology**: Documents explain why certain patterns are suspicious
- **Source Authority**: Explanations can reference authoritative sources (FINTRAC, FinCEN)

#### 2. **Mapping Model Features to Red Flags**
For explainability, the library enables:
- **Feature → Red Flag Mapping**: When a model flags a customer, identify which red flags are present
- **Risk Score Interpretation**: Explain risk scores in terms of red flag severity and combinations
- **Decision Rationale**: Use red flag descriptions to explain why a customer was flagged

#### 3. **Borderline Case Explanation**
**Critical Requirement**: "Help understand why borderline cases are flagged/not flagged"

- **Red Flag Thresholds**: Library documents provide context on what makes a pattern suspicious
- **Risk Assessment Guidance**: Documents include guidance on risk levels and combinations
- **Edge Case Context**: Understanding red flag context helps explain why similar cases might differ

#### 4. **User-Friendly Explanations**
The library structure supports different explanation needs:
- **Quick Reference**: `00_COMPREHENSIVE_RED_FLAGS_MASTER.md` for quick lookups
- **Detailed Context**: Individual documents (01-08) for in-depth explanations
- **Feature Mapping**: `Red_Flag_to_Feature_Mapping.md` to connect technical features to red flags

#### 5. **Source-Backed Explanations**
Every explanation can be traced to authoritative sources:
- **Source Traceability**: Each red flag includes source document, date, and reference number
- **Credibility**: Explanations reference official FINTRAC and FinCEN documents
- **Verification**: Users can verify explanations by checking source documents

---

## Integration Workflow

### For Task 2 (Detection Model Development)

1. **Feature Engineering Phase**:
   - Review `Red_Flag_to_Feature_Mapping.md` for feature suggestions
   - Check `00_COMPREHENSIVE_RED_FLAGS_MASTER.md` for all relevant red flags
   - Reference individual documents (01-08) for detailed context

2. **Model Training Phase**:
   - Engineer features based on red flag data signals
   - Use red flag combinations to create composite features
   - Validate that features align with library red flags

3. **Model Validation Phase**:
   - Ensure flagged customers match red flags in the library
   - Verify risk scores reflect red flag severity
   - Check that model detects patterns documented in the library

### For Task 3 (Explainability Development)

1. **Explanation Generation Phase**:
   - Map model feature importance to red flags using `Red_Flag_to_Feature_Mapping.md`
   - Identify which red flags are present in flagged customers
   - Reference red flag descriptions for explanation text

2. **Explanation Validation Phase**:
   - Verify explanations reference correct red flags
   - Ensure explanations are non-technical and clear
   - Check that borderline cases are explained using red flag context

3. **User Presentation Phase**:
   - Use red flag descriptions as explanation templates
   - Reference source documents for credibility
   - Provide links to detailed red flag documents for interested users

---

## Key Documents for Each Task

### Task 2 (Detection Model) - Primary Documents:
- **`Red_Flag_to_Feature_Mapping.md`**: Core document for feature engineering
- **`00_COMPREHENSIVE_RED_FLAGS_MASTER.md`**: Quick reference for all red flags and their feature mappings
- **Individual documents (01-08)**: Detailed context for understanding risk patterns

### Task 3 (Explainability) - Primary Documents:
- **`00_COMPREHENSIVE_RED_FLAGS_MASTER.md`**: Quick reference for red flag descriptions
- **`Red_Flag_to_Feature_Mapping.md`**: Connect model features to red flags
- **Individual documents (01-08)**: Detailed context for explaining decisions
- **`SOURCES.md`**: Source information for authoritative explanations

---

## Critical Success Factors

### For Task 2:
1. ✅ **Feature Alignment**: Features must detect red flags documented in the library
2. ✅ **Risk Relevance**: Flagged customers must align with AML risks in the library
3. ✅ **Pattern Generalization**: Model should detect patterns similar to library red flags

### For Task 3:
1. ✅ **Red Flag Mapping**: Every explanation must map to specific red flags
2. ✅ **Non-Technical Language**: Use red flag descriptions (not technical feature names)
3. ✅ **Source Authority**: Reference authoritative sources for credibility
4. ✅ **Borderline Clarity**: Explain why similar cases differ using red flag context

---

## Summary

The AML Knowledge Library (Task 1) is a **standalone, independent knowledge base** that:

### Standalone Value
- **Complete and Self-Contained**: Can be used independently for AML investigation, research, and reference
- **No Dependencies**: Does not require Tasks 2 or 3 to be complete or useful
- **Reproducible**: Can be generated and validated independently from source documents
- **Authoritative**: Source-backed intelligence that stands on its own merit

### Facilitation of Downstream Tasks
While the library is independent, it is **designed to facilitate** Tasks 2 and 3:

1. **Facilitates Task 2** by:
   - Providing feature engineering guidance through red flag to feature mappings
   - Defining what constitutes AML risk for model validation
   - Offering context for understanding suspicious patterns

2. **Facilitates Task 3** by:
   - Providing non-technical language for explanations
   - Mapping model features to understandable red flags
   - Offering source-backed authority for explanations

**Key Point**: The library's design allows it to facilitate Tasks 2 and 3 effectively, but it maintains complete independence and can be used, understood, and validated without any reference to those downstream tasks.

---

**Last Updated**: 2025-01-23  
**Status**: Complete  
**Version**: 1.0
