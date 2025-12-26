#!/bin/bash
# Script to generate a chapter using Claude Code

# Usage: ./generate_chapter.sh <module_name> <chapter_name> <chapter_title>
# Example: ./generate_chapter.sh "module-1-ros" "ros-nodes" "ROS 2 Nodes and Architecture"

if [ $# -ne 3 ]; then

    echo "Usage: $0 <module_name> <chapter_name> <chapter_title>"
    echo "Example: $0 module-1-ros ros-nodes 'ROS 2 Nodes and Architecture'"
    exit 1
fi

MODULE_NAME=$1
CHAPTER_NAME=$2
CHAPTER_TITLE=$3
CHAPTER_PATH="book/docs/$MODULE_NAME/$CHAPTER_NAME.md"

# Check if chapter file already exists
if [ -f "$CHAPTER_PATH" ]; then
    echo "Error: Chapter file $CHAPTER_PATH already exists!"
    exit 1
fi

# Generate chapter content using Claude Code prompt
cat > "$CHAPTER_PATH" << EOF
---
sidebar_position: 3
title: '$CHAPTER_TITLE'
---

# $CHAPTER_TITLE

TODO: Chapter content will be generated using Claude Code based on the textbook's learning objectives and structure.

## Learning Objectives

After completing this chapter, you will be able to:
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

## Prerequisites

- [Prerequisite knowledge needed]

## Content

[Chapter content goes here]

## Lab Exercise

[Practical exercise for this chapter]

## Summary

[Chapter summary]

## Assessment

[Questions or exercises to test understanding]
EOF

echo "Chapter template created at $CHAPTER_PATH"
echo "To generate content with Claude Code, run:"
echo "  claude code --message 'Generate content for chapter: $CHAPTER_TITLE. Include learning objectives, prerequisites, detailed content, lab exercises, and summary based on the Physical AI & Humanoid Robotics textbook structure.' --file $CHAPTER_PATH"