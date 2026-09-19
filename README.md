# CodeShift

**AI-Assisted Code Migration & Static Analysis**

CodeShift is a developer tool for analyzing JavaScript source code, inferring types using AST-based static analysis, and automatically migrating JavaScript code to TypeScript.

## What CodeShift Does

CodeShift currently provides a JavaScript → TypeScript migration pipeline:

```text
JavaScript Source
       ↓
AST Parsing
       ↓
Static Analysis
       ↓
Type Inference
       ↓
Migration Suggestions
       ↓
TypeScript Transformation
       ↓
Syntax Validation
       ↓
Semantic Validation
       ↓
TypeScript Output


Features
JavaScript AST parsing using Tree-sitter
Function and parameter analysis
Expression-level type inference
Confidence-aware type suggestions
JavaScript → TypeScript transformation
Source-range based code edits
TypeScript syntax validation
TypeScript compiler-based semantic validation
Migration warnings for uncertain inferences
Automated test suite
Example
JavaScript
function addTen(a) {
    return a + 10;
}
CodeShift Analysis
Function: addTen
Parameters: a
Return expression: a + 10
Operation: +
Inferred return type: number
Confidence: high

Migration Suggestions:
  a → number
  return → number
Generated TypeScript
function addTen(a: number): number {
    return a + 10;
}



Architecture
                 ┌──────────────────┐
                 │ JavaScript Source │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Tree-sitter AST  │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Static Analyzer  │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Type Inference   │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ TS Transformer   │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │   Validator      │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ TypeScript Code  │
                 └──────────────────┘



Project Structure


codeshift/
├── examples/
├── src/
│   └── codeshift/
│       ├── analyzer/
│       │   ├── javascript.py
│       │   ├── expression.py
│       │   └── type_inference.py
│       ├── parser/
│       │   └── javascript.py
│       ├── transformer/
│       │   ├── typescript.py
│       │   └── edits.py
│       ├── validator/
│       │   └── typescript.py
│       ├── walker/
│       │   └── ast.py
│       └── cli.py
├── tests/
├── pyproject.toml
├── architecture.md
└── README.md




Installation

Clone the repository and create a virtual environment:

python -m venv .venv

Activate the environment.

Windows
.venv\Scripts\Activate.ps1

Install the project:

pip install -e .

Install development dependencies:

pip install pytest
Usage

Analyze a JavaScript file:

codeshift analyze test.js

Generate a TypeScript file:

codeshift analyze test.js --output test.ts
Testing

Run the complete test suite:

pytest

Current test suite covers:

JavaScript parsing
Function analysis
Literal type inference
Binary expression inference
Parameter type inference
JavaScript → TypeScript transformation
Confidence warnings
TypeScript syntax validation
TypeScript semantic validation
Design Principles

CodeShift follows a static-analysis-first approach.

Instead of relying entirely on an AI model to rewrite source code, CodeShift first extracts structural and type information from the source program using AST-based analysis.

AI-assisted transformation can be added as a later layer where deterministic analysis is insufficient.

Current Scope

The current implementation focuses on JavaScript function analysis and JavaScript → TypeScript migration.

The migration engine is designed to be extended with additional:

JavaScript syntax patterns
Type inference rules
Migration transformations
Validation rules
AI-assisted transformations
Research Direction

Potential research directions include:

AI-assisted code migration
Static analysis
Program transformation
Large-scale code modernization
Developer tools
Automated type inference
Hybrid static-analysis and LLM systems