---
name: definitions-manager
description: Manage, test, and validate API definitions (schemas, parsers, resources, upstream). Use this skill to add/edit/delete definition files, test parsers, visualize schemas, or analyze if code matches the definition contract. Uses tlc-spec-driven when code changes are needed.
---

# Definitions Manager Skill

This skill helps you manage the custom YAML endpoint specifications, JSON schemas, Python parser scripts, and upstream service definitions in `it-mdb-api/definitions`.

## Rules & Normalizations

1. **Source of Truth**: The `definitions/` directory contains contracts. Follow `definitions/README.md` for schemas and structures.
2. **Directory Structure**:
   - `definitions/schemas/`: JSON schemas for validating output.
   - `definitions/parsers/`: Python scripts that map upstream responses to our schemas.
   - `definitions/upstream/`: External API service configurations.
   - `definitions/resources/<version>/`: YAML definitions of our API endpoints.
3. **Parser Contract**:
   - Must expose `def parse(input_data: dict) -> dict:`.
   - Must support CLI execution: `python3 definitions/parsers/[name].py <input_json_file>` (outputs JSON).
4. **Validation**: When creating or editing resources, ensure referenced parsers, schemas, and upstream models exist and paths are correct.

## Actions

### 1. Manage Definitions (Add, Edit, Delete)
- Use standard file modification tools (`write`, `edit`, `bash` for `rm`) to update files in `definitions/`.
- Always respect the structural contracts defined in `definitions/README.md`.
- Keep YAML and JSON strictly formatted.

### 2. Test Parsers
- To test a parser, create a temporary JSON input file with upstream sample data.
- Run its CLI script: `python3 definitions/parsers/<parser_name>.py <input_json_file>`.
- Verify the output matches the expected JSON schema.

### 3. Visualize Schemas
- Read and format JSON schemas using `read` or `bash` (e.g., `cat definitions/schemas/<schema>.json | jq`).
- Explain the schema components to the user when visualizing.

### 4. Analyze Code against Definitions
- If asked to verify compliance, examine the codebase (e.g., API routes, upstream clients, parser execution logic).
- Compare the code implementation with the contracts in `definitions/`.
- **When out of sync**: DO NOT fix the code directly. Instead, invoke the `tlc-spec-driven` skill.
  - Plan and create a specification describing what changes are required to bring the code back in line with the definitions.
  - Follow the `tlc-spec-driven` workflow (`Specify → Design → Tasks → Execute → Validate`).

## Usage
When dealing with definitions, ensure strict adherence to `definitions/README.md`. You have full autonomy to inspect files in `definitions/` and write/delete them as requested by the user, while ensuring contracts remain valid.
