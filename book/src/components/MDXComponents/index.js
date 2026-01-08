/**
 * Custom MDX Components for Physical AI Textbook
 * Import these in your MDX files for enhanced content presentation
 */

import React from 'react';
import styles from './styles.module.css';

/**
 * KeyConcept - Highlight important concepts
 * Usage: <KeyConcept title="Important">Content here</KeyConcept>
 */
export function KeyConcept({ title, children }) {
  return (
    <div className={styles.keyConcept}>
      <div className={styles.keyConceptHeader}>
        <span className={styles.keyConceptIcon}>💡</span>
        <span className={styles.keyConceptTitle}>{title || 'Key Concept'}</span>
      </div>
      <div className={styles.keyConceptContent}>{children}</div>
    </div>
  );
}

/**
 * LearningObjective - Display learning goals
 * Usage: <LearningObjective>What you'll learn</LearningObjective>
 */
export function LearningObjective({ children }) {
  return (
    <div className={styles.learningObjective}>
      <div className={styles.learningObjectiveHeader}>
        <span className={styles.learningObjectiveIcon}>🎯</span>
        <span className={styles.learningObjectiveTitle}>Learning Objectives</span>
      </div>
      <div className={styles.learningObjectiveContent}>{children}</div>
    </div>
  );
}

/**
 * ModuleHeader - Styled header for module pages
 * Usage: <ModuleHeader module={1} title="ROS 2" subtitle="The Nervous System" />
 */
export function ModuleHeader({ module, title, subtitle, color }) {
  const moduleColors = {
    1: '#3b82f6',
    2: '#8b5cf6',
    3: '#76b900',
    4: '#ec4899',
  };

  const bgColor = color || moduleColors[module] || '#0ea5e9';

  return (
    <div className={styles.moduleHeader} style={{ '--module-color': bgColor }}>
      <span className={styles.moduleNumber}>Module {module}</span>
      <h1 className={styles.moduleTitle}>{title}</h1>
      {subtitle && <p className={styles.moduleSubtitle}>{subtitle}</p>}
    </div>
  );
}

/**
 * CodeExample - Enhanced code block with title and description
 * Usage: <CodeExample title="Example" lang="python">code here</CodeExample>
 */
export function CodeExample({ title, description, children }) {
  return (
    <div className={styles.codeExample}>
      {title && (
        <div className={styles.codeExampleHeader}>
          <span className={styles.codeExampleIcon}>💻</span>
          <span className={styles.codeExampleTitle}>{title}</span>
        </div>
      )}
      {description && <p className={styles.codeExampleDescription}>{description}</p>}
      <div className={styles.codeExampleContent}>{children}</div>
    </div>
  );
}

/**
 * DiagramContainer - Container for diagrams with caption
 * Usage: <DiagramContainer caption="Architecture diagram">diagram here</DiagramContainer>
 */
export function DiagramContainer({ caption, children }) {
  return (
    <figure className={styles.diagramContainer}>
      <div className={styles.diagramContent}>{children}</div>
      {caption && <figcaption className={styles.diagramCaption}>{caption}</figcaption>}
    </figure>
  );
}

/**
 * StepByStep - Numbered steps for tutorials
 * Usage: <StepByStep steps={[{title: "Step 1", content: "Do this"}]} />
 */
export function StepByStep({ steps }) {
  return (
    <div className={styles.stepByStep}>
      {steps.map((step, index) => (
        <div key={index} className={styles.step}>
          <div className={styles.stepNumber}>{index + 1}</div>
          <div className={styles.stepContent}>
            <h4 className={styles.stepTitle}>{step.title}</h4>
            <div className={styles.stepDescription}>{step.content}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

/**
 * Comparison - Side by side comparison
 * Usage: <Comparison left={{title: "Before", content: "..."}} right={{title: "After", content: "..."}} />
 */
export function Comparison({ left, right }) {
  return (
    <div className={styles.comparison}>
      <div className={styles.comparisonItem}>
        <div className={styles.comparisonHeader}>{left.title}</div>
        <div className={styles.comparisonContent}>{left.content}</div>
      </div>
      <div className={styles.comparisonDivider}>
        <span>vs</span>
      </div>
      <div className={styles.comparisonItem}>
        <div className={styles.comparisonHeader}>{right.title}</div>
        <div className={styles.comparisonContent}>{right.content}</div>
      </div>
    </div>
  );
}

/**
 * Prerequisites - Show what's needed before starting
 * Usage: <Prerequisites items={["Python 3.8+", "ROS 2 Humble"]} />
 */
export function Prerequisites({ items }) {
  return (
    <div className={styles.prerequisites}>
      <div className={styles.prerequisitesHeader}>
        <span className={styles.prerequisitesIcon}>📋</span>
        <span className={styles.prerequisitesTitle}>Prerequisites</span>
      </div>
      <ul className={styles.prerequisitesList}>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

/**
 * Quiz - Interactive quiz component
 * Usage: <Quiz question="What is ROS?" options={["A", "B", "C"]} correct={0} />
 */
export function Quiz({ question, options, correct, explanation }) {
  const [selected, setSelected] = React.useState(null);
  const [showResult, setShowResult] = React.useState(false);

  const handleSelect = (index) => {
    setSelected(index);
    setShowResult(true);
  };

  return (
    <div className={styles.quiz}>
      <div className={styles.quizHeader}>
        <span className={styles.quizIcon}>❓</span>
        <span className={styles.quizTitle}>Quick Check</span>
      </div>
      <p className={styles.quizQuestion}>{question}</p>
      <div className={styles.quizOptions}>
        {options.map((option, index) => (
          <button
            key={index}
            className={`${styles.quizOption} ${
              showResult
                ? index === correct
                  ? styles.correct
                  : index === selected
                  ? styles.incorrect
                  : ''
                : ''
            } ${selected === index ? styles.selected : ''}`}
            onClick={() => handleSelect(index)}
            disabled={showResult}
          >
            {option}
          </button>
        ))}
      </div>
      {showResult && explanation && (
        <div className={styles.quizExplanation}>
          <strong>Explanation:</strong> {explanation}
        </div>
      )}
    </div>
  );
}

/**
 * ProgressTracker - Show chapter progress
 * Usage: <ProgressTracker current={3} total={10} />
 */
export function ProgressTracker({ current, total, label }) {
  const percentage = Math.round((current / total) * 100);

  return (
    <div className={styles.progressTracker}>
      <div className={styles.progressHeader}>
        <span>{label || 'Progress'}</span>
        <span>{current} / {total}</span>
      </div>
      <div className={styles.progressBar}>
        <div className={styles.progressFill} style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}

// Export all components
export default {
  KeyConcept,
  LearningObjective,
  ModuleHeader,
  CodeExample,
  DiagramContainer,
  StepByStep,
  Comparison,
  Prerequisites,
  Quiz,
  ProgressTracker,
};
