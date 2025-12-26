# Quickstart: Physical AI & Humanoid Robotics Book Development

## Prerequisites

- Git
- Node.js (v16 or higher)
- ROS 2 Humble Hawksbill
- Python 3.8+
- Docker (for reproducible environments)

## Setup Development Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install Node.js dependencies:
```bash
cd book
npm install
```

3. Set up ROS 2 environment:
```bash
source /opt/ros/humble/setup.bash
```

4. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

## Local Development

1. Start Docusaurus development server:
```bash
cd book
npm start
```

2. The site will be available at `http://localhost:3000`

## Building the Documentation

```bash
npm run build
```

## Adding New Content

1. Create new markdown files in the appropriate module directory:
   - `book/docs/module-1-ros/` for ROS 2 content
   - `book/docs/module-2-digital-twin/` for simulation content
   - `book/docs/module-3-isaac-ai/` for AI content
   - `book/docs/module-4-vision-action/` for capstone content

2. Update `book/sidebars.js` to include the new content in the navigation

## Adding Simulation Assets

1. Place URDF files in `book/static/simulations/urdf/`
2. Place SDF files in `book/static/simulations/sdf/`
3. Place Isaac USD files in `book/static/simulations/isaac/`

## Adding Code Examples

1. Place Python examples in `book/static/code-examples/python/`
2. Place C++ examples in `book/static/code-examples/cpp/`
3. Reference examples in documentation using appropriate Docusaurus components

## Testing Simulation Assets

1. Launch Gazebo with your model:
```bash
cd book/static/simulations
ros2 launch <package_name> <launch_file>.py
```

## Multilingual Support

1. For Urdu translation, create files in the `i18n/ur/` directory
2. Use the same file structure as the English content
3. Run `npm run write-translations` to generate translation files

## Deployment

The site is automatically deployed to GitHub Pages when changes are merged to the main branch. The CI/CD pipeline handles:

- Building the Docusaurus site
- Running tests
- Deploying to GitHub Pages