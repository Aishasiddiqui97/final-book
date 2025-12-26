<!--
SYNC IMPACT REPORT:
Version change: 1.0.1 → 1.0.2
List of modified principles:
- Added "RAG Chatbot Principles" section
Added sections: RAG Chatbot Principles
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics: Spec-Driven Guide Constitution

## Core Principles

### Educational Mission-First
Every chapter and exercise serves the educational mission of teaching Physical AI & Humanoid Robotics concepts to undergrad/early grad CS & robotics engineers; Content must be pedagogically sound, progressively structured, and aligned with learning objectives; Clear learning outcomes required for each module.

### Spec-Driven Learning
Every concept and implementation follows spec-driven methodology; Specifications must be written and validated before implementation; Each chapter includes clear requirements, testable outcomes, and verification steps; Red-Green-Refactor learning cycle applied to both code and understanding.

### Reproducible Experiments
All experiments must include exact environment, datasets, and Docker/firmware builds; Every practical exercise must be reproducible across different hardware setups; Detailed setup instructions, version specifications, and configuration files required; Laboratory exercises must include verification steps and expected outcomes.

### Accessible Content
Content must be written in clear English with Urdu summaries for broader accessibility; All examples and explanations must be approachable for target audience; Multiple learning modalities supported (text, visual, hands-on); Barrier-free learning experience prioritized.

### Open Source & Licensing
All content, code examples, and resources released under MIT license; Contributions welcome from academic and industry communities; Transparency in development process; Community-driven improvements and corrections encouraged.

### Hardware-Software Integration
Focus on tight integration between physical hardware and AI software systems; Real-world robotics applications emphasized; Both simulation and physical robot implementations required; Understanding of sensor-actuator loops and real-time constraints.

## RAG Chatbot Principles

### Zero Hallucination Rule
The chatbot must answer ONLY from the book chapters, labs, and code blocks; If information is not in the book, the chatbot must respond with "Not found in this book"; No assumptions or external knowledge allowed; Strict adherence to source material to maintain academic integrity.

### Citation Requirement
Every answer must include citations (Chapter → Section → URL); Users must be able to trace responses back to original content; Citations enable verification and deeper exploration; Academic rigor maintained through proper attribution.

### Dual Mode Functionality
Support two operational modes: 1) Full-book question answering for comprehensive queries, 2) Selected-text–only answering for user-highlighted content; Both modes must respect the zero hallucination rule; Mode selection should be intuitive for users.

### Performance Standards
Fast enough for in-page usage with minimal latency; Optimized for engineering students and researchers' workflow; Responsive interaction without sacrificing accuracy; Efficient retrieval mechanisms to maintain speed.

### Privacy-First Approach
No training on user data; User queries and interactions not stored or used for model improvement; Academic privacy standards maintained; No personal data collection or processing.

## Additional Educational Requirements

Technology stack requirements: Python, ROS, Gazebo simulation, Docker containers, embedded systems (Arduino/Raspberry Pi); Compliance with academic standards; Deployment in educational environments; Hardware compatibility across different platforms.

## Development Workflow

Code review requirements: Peer review by domain experts; Student usability testing for new content; Testing gates include both automated tests and practical laboratory validation; Deployment approval process includes pedagogical review.

## Governance

Constitution supersedes all other practices; All content and code must verify compliance with educational mission and accessibility goals; Complexity must be justified by learning objectives; Amendments require pedagogical review and approval by academic advisory board.

**Version**: 1.0.2 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-26
