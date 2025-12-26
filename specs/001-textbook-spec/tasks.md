# Tasks: Physical AI & Humanoid Robotics Docusaurus Book

**Input**: Design documents from `/specs/001-textbook-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `book/`, `docs/`, `static/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Task Board

### To Do

- [ ] T011 [P] [US1] Create Chapter 2 content: book/docs/module-1-ros/ros-nodes.md
- [ ] T012 [P] [US1] Create Chapter 3 content: book/docs/module-1-ros/ros-messages.md
- [ ] T013 [P] [US1] Create Chapter 4 content: book/docs/module-1-ros/ros-services.md
- [ ] T014 Create Chapter 5 content: book/docs/module-2-digital-twin/urdf-modeling.md
- [ ] T015 [P] [US2] Create Chapter 6 content: book/docs/module-2-digital-twin/gazebo-simulation.md
- [ ] T016 [P] [US2] Create Chapter 7 content: book/docs/module-2-digital-twin/unity-integration.md
- [ ] T017 [P] [US2] Create Chapter 8 content: book/docs/module-2-digital-twin/physics-simulation.md
- [ ] T018 Create Chapter 9 content: book/docs/module-3-isaac-ai/isaac-concepts.md
- [ ] T019 [P] [US3] Create Chapter 10 content: book/docs/module-3-isaac-ai/ai-robot-brain.md
- [ ] T020 [P] [US3] Create Chapter 11 content: book/docs/module-3-isaac-ai/perception-systems.md
- [ ] T021 [P] [US3] Create Chapter 12 content: book/docs/module-3-isaac-ai/deep-learning.md
- [ ] T022 Create Chapter 13 content: book/docs/module-4-vision-action/vision-language-models.md
- [ ] T023 [P] [US4] Create Chapter 14 content: book/docs/module-4-vision-action/action-planning.md
- [ ] T024 [P] [US4] Create Chapter 15 content: book/docs/module-4-vision-action/humanoid-capstone.md
- [ ] T025 [P] Create URDF robot model for Chapter 1: book/static/simulations/urdf/basic_robot.urdf
- [ ] T026 [P] Create SDF simulation environment for Chapter 2: book/static/simulations/sdf/simple_world.sdf
- [ ] T027 [P] Create Isaac USD assets for Chapter 9: book/static/simulations/isaac/basic_scene.usd
- [ ] T028 [P] Create Python code examples for ROS module: book/static/code-examples/python/ros_examples/
- [ ] T029 [P] Create C++ code examples for ROS module: book/static/code-examples/cpp/ros_examples/
- [ ] T030 [P] Create Python code examples for simulation module: book/static/code-examples/python/sim_examples/
- [ ] T032 [P] [US1] Create Urdu translation for Chapter 2: i18n/ur/docusaurus-plugin-content-docs/current/module-1-ros/ros-nodes.md
- [ ] T033 [P] [US1] Create Urdu translation for Chapter 3: i18n/ur/docusaurus-plugin-content-docs/current/module-1-ros/ros-messages.md
- [ ] T034 [P] [US2] Create Urdu translation for Chapter 5: i18n/ur/docusaurus-plugin-content-docs/current/module-2-digital-twin/urdf-modeling.md
- [ ] T035 [P] [US3] Create Urdu translation for Chapter 9: i18n/ur/docusaurus-plugin-content-docs/current/module-3-isaac-ai/isaac-concepts.md
- [ ] T036 [P] [US4] Create Urdu translation for Chapter 13: i18n/ur/docusaurus-plugin-content-docs/current/module-4-vision-action/vision-language-models.md
- [ ] T038 Create CI job to test simulation examples: .github/workflows/test-simulations.yml
- [ ] T039 Create CI job to validate URDF/SDF files: .github/workflows/validate-assets.yml

### In Progress

### Done

- [x] T001 Create Docusaurus project structure in book/ directory
- [x] T002 [P] Set up package.json with Docusaurus dependencies
- [x] T003 Configure docusaurus.config.js with 4 modules navigation
- [x] T004 Create sidebars.js with module and chapter structure
- [x] T005 [P] Set up GitHub Actions workflow for deployment to GitHub Pages
- [x] T006 Create module 1 root page: book/docs/module-1-ros/index.md
- [x] T007 [P] Create module 2 root page: book/docs/module-2-digital-twin/index.md
- [x] T008 [P] Create module 3 root page: book/docs/module-3-isaac-ai/index.md
- [x] T009 [P] Create module 4 root page: book/docs/module-4-vision-action/index.md
- [x] T010 Create Chapter 1 content: book/docs/module-1-ros/introduction-to-physical-ai.md
- [x] T023 [P] [US4] Create Chapter 15 content: book/docs/module-4-vision-action/humanoid-capstone.md
- [x] T031 [P] Configure multilingual support for English and Urdu in docusaurus.config.js
- [x] T032 [P] [US1] Create Urdu translation for Chapter 1: i18n/ur/docusaurus-plugin-content-docs/current/module-1-ros/introduction-to-physical-ai.md
- [x] T037 Create CI job to build Docusaurus site: .github/workflows/build.yml

---

## Task Details

### Setup Phase
- **Owner**: DevOps
- **Branch naming**: `setup-project`
- **Required files**: package.json, docusaurus.config.js, sidebars.js
- **CI job**: build-docs
- **Implementation**:
  ```bash
  npx create-docusaurus@latest book classic
  cd book && npm install
  ```

### Module 1: ROS 2 Nervous System (US1 - Student Learning)
- **Owner**: Author
- **Branch naming**: `feature/module-1-ros`
- **Required files**: book/docs/module-1-ros/*
- **CI job**: build-module-1
- **Implementation**:
  ```bash
  # Create ROS module content
  mkdir -p book/docs/module-1-ros
  # Add chapter content with learning objectives and examples
  ```

### Module 2: Digital Twin (US2 - Instructor Teaching)
- **Owner**: Author
- **Branch naming**: `feature/module-2-digital-twin`
- **Required files**: book/docs/module-2-digital-twin/*, book/static/simulations/*
- **CI job**: build-module-2
- **Implementation**:
  ```bash
  # Create simulation module content and assets
  mkdir -p book/docs/module-2-digital-twin book/static/simulations
  # Add URDF/SDF files and simulation examples
  ```

### Module 3: NVIDIA Isaac AI-Robot Brain (US3 - Developer Implementation)
- **Owner**: Author
- **Branch naming**: `feature/module-3-isaac-ai`
- **Required files**: book/docs/module-3-isaac-ai/*, book/static/code-examples/*
- **CI job**: build-module-3
- **Implementation**:
  ```bash
  # Create AI module content and code examples
  mkdir -p book/docs/module-3-isaac-ai book/static/code-examples
  # Add Isaac Sim examples and AI code implementations
  ```

### Module 4: Vision-Language-Action & Humanoid Capstone (US4 - Lab Technician Setup)
- **Owner**: Author
- **Branch naming**: `feature/module-4-vision-action`
- **Required files**: book/docs/module-4-vision-action/*, book/static/simulations/*
- **CI job**: build-module-4
- **Implementation**:
  ```bash
  # Create capstone module content and integration examples
  mkdir -p book/docs/module-4-vision-action
  # Add comprehensive project integrating all concepts
  ```

### Multilingual Support Phase
- **Owner**: Translator
- **Branch naming**: `feature/multilingual`
- **Required files**: i18n/ur/*, docusaurus.config.js
- **CI job**: build-multilingual
- **Implementation**:
  ```bash
  # Generate translation files
  cd book && npm run write-translations -- --locale ur
  # Add Urdu translations for all content
  ```

### Deployment Phase
- **Owner**: DevOps
- **Branch naming**: `deploy-gh-pages`
- **Required files**: .github/workflows/deploy.yml
- **CI job**: deploy-gh-pages
- **Implementation**:
  ```bash
  # Configure GitHub Pages deployment
  # Build and deploy site on merge to main
  ```