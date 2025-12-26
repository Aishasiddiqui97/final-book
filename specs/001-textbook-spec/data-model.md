# Data Model: Physical AI & Humanoid Robotics Docusaurus Book

## Entities

### Module
- **Fields**:
  - id: string (unique identifier, e.g., "module-1-ros")
  - title: string (e.g., "ROS 2 Nervous System")
  - description: string (brief overview of the module)
  - order: integer (sequence in which modules appear)
  - learningObjectives: array of strings (specific learning outcomes)
  - prerequisites: array of strings (required knowledge/skills)
  - duration: integer (estimated hours to complete)

### Chapter
- **Fields**:
  - id: string (unique identifier, e.g., "module-1-chapter-1")
  - moduleId: string (foreign key to Module)
  - title: string (chapter title)
  - summary: string (one-line summary)
  - content: string (main content in markdown format)
  - order: integer (sequence within module)
  - learningObjectives: array of strings (specific learning outcomes)
  - prerequisites: array of strings (required knowledge/skills)
  - duration: integer (estimated hours to complete)
  - codeExamples: array of strings (file paths to code examples)
  - simulationAssets: array of strings (file paths to simulation files)

### CodeExample
- **Fields**:
  - id: string (unique identifier)
  - title: string (descriptive title)
  - description: string (what the example demonstrates)
  - language: string (e.g., "python", "cpp", "bash")
  - code: string (the actual code content)
  - associatedChapterId: string (foreign key to Chapter)
  - difficulty: string (e.g., "beginner", "intermediate", "advanced")
  - tags: array of strings (relevant topics/tags)

### SimulationAsset
- **Fields**:
  - id: string (unique identifier)
  - title: string (descriptive title)
  - description: string (what the asset represents)
  - type: string (e.g., "urdf", "sdf", "usd", "world")
  - filePath: string (path to the asset file)
  - associatedChapterId: string (foreign key to Chapter)
  - tags: array of strings (relevant topics/tags)
  - complexity: string (e.g., "simple", "intermediate", "complex")

### Assessment
- **Fields**:
  - id: string (unique identifier)
  - title: string (descriptive title)
  - description: string (what the assessment tests)
  - type: string (e.g., "quiz", "lab", "project", "exam")
  - associatedChapterId: string (foreign key to Chapter)
  - questions: array of objects (for quizzes)
  - requirements: string (for projects/labs)
  - difficulty: string (e.g., "beginner", "intermediate", "advanced")
  - estimatedTime: integer (minutes to complete)

### User
- **Fields**:
  - id: string (unique identifier)
  - role: string (e.g., "student", "instructor", "developer")
  - languagePreference: string (e.g., "en", "ur")
  - progress: object (tracking completion status)

## Relationships

- Module (1) → (many) Chapter: A module contains multiple chapters
- Chapter (1) → (many) CodeExample: A chapter may have multiple code examples
- Chapter (1) → (many) SimulationAsset: A chapter may have multiple simulation assets
- Chapter (1) → (many) Assessment: A chapter may have multiple assessments
- User (many) → (many) Chapter: Users can access multiple chapters and track progress

## Validation Rules

- Module.id must be unique
- Chapter.id must be unique
- Chapter.moduleId must reference an existing Module
- CodeExample.associatedChapterId must reference an existing Chapter
- SimulationAsset.associatedChapterId must reference an existing Chapter
- Assessment.associatedChapterId must reference an existing Chapter
- Module.order must be unique within the course
- Chapter.order must be unique within a module
- LanguagePreference must be one of the supported languages (en, ur)

## State Transitions

### Chapter Progress States
- `not_started` → `in_progress` → `completed`
- User can move between states based on their progress

### Content States
- `draft` → `review` → `published` → `deprecated`
- Content follows editorial workflow through these states