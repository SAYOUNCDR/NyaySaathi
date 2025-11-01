# 🏛️ NyaySaathi - Your AI Legal Companion

<div align="center">

![NyaySaathi Logo](public/LogoSaathi.svg)

**Empowering Citizens with Verified Indian Legal Information**

[![React](https://img.shields.io/badge/React-18.x-61dafb?logo=react)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-38bdf8?logo=tailwind-css)](https://tailwindcss.com/)
[![Vite](https://img.shields.io/badge/Vite-5.x-646cff?logo=vite)](https://vitejs.dev/)
[![Framer Motion](https://img.shields.io/badge/Framer_Motion-11.x-ff69b4?logo=framer)](https://www.framer.com/motion/)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 📖 About

**NyaySaathi** is an AI-powered legal assistant designed to make Indian legal information accessible to everyone. Built with a focus on accuracy and reliability, NyaySaathi is trained exclusively on verified Indian legal sources to provide trustworthy guidance on legal matters.

Whether you're dealing with landlord disputes, consumer rights, or need to understand legal procedures, NyaySaathi is here to help you navigate the complexities of Indian law with confidence.

---

## ✨ Features

### 🤖 AI-Powered Chat Interface

- **Intelligent Conversations**: Interactive chatbot that understands your legal queries
- **Context-Aware Responses**: Maintains conversation history for relevant answers
- **Auto-Expanding Input**: Dynamic text input that grows with your message
- **Real-time Response**: Instant AI-generated legal guidance

### 📚 Comprehensive Legal Resources

- **NyayShala**: Educational content about Indian laws and legal procedures
- **NyayMap**: Interactive legal resources and documentation
- **Verified Sources**: Information backed by authentic Indian legal databases
- **Step-by-Step Guides**: Easy-to-follow instructions for common legal processes

### 🎨 Modern User Experience

- **Responsive Design**: Fully optimized for mobile, tablet, and desktop
- **Clean Interface**: Intuitive navigation with collapsible sidebar
- **Smooth Animations**: Powered by Framer Motion for fluid transitions
- **Accessibility First**: Built with ARIA labels and keyboard navigation support

### 🔒 Trustworthy Information

- **Verified Legal Data**: All information sourced from official Indian legal repositories
- **Transparent Sources**: Clear citations and references for all legal advice
- **Up-to-Date**: Regular updates to reflect current Indian laws

---

## 🚀 Installation

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/SAYOUNCDR/NyaySaathi.git
   cd NyaySaathi
   ```

2. **Install dependencies**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Install Framer Motion** (if not already installed)

   ```bash
   npm install framer-motion
   # or
   yarn add framer-motion
   ```

4. **Start the development server**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   - Navigate to `http://localhost:5173` (or the port shown in your terminal)

---

## 💻 Usage

### Chat with AI Saathi

1. Navigate to the **AI Saathi** section from the sidebar
2. Type your legal question in the input box
3. Press Enter or click the send button
4. Receive instant, verified legal guidance

### Explore Learning Resources

1. Visit the **Learning & Resources** section on the homepage
2. Toggle between **NyayShala** (learning materials) and **NyayMap** (legal guides)
3. Click on any topic to expand and view detailed information

### Navigate the Platform

- Use the collapsible sidebar for quick navigation
- Access emergency legal help via the "Get Emergency" button
- Browse through verified legal sources and case studies

---

## 🛠️ Tech Stack

### Frontend Framework

- **React 18** - Modern UI library with hooks and functional components
- **Vite** - Next-generation frontend build tool for fast development

### Styling & UI

- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Framer Motion** - Production-ready animation library for smooth transitions
- **Custom Components** - Reusable sidebar, navbar, and chat interface components

### Routing & State Management

- **React Router** - Client-side routing for single-page application
- **React Hooks** - useState, useEffect, useRef for state and side effects

### Development Tools

- **ESLint** - Code quality and consistency
- **PostCSS** - CSS processing and optimization

---

## 📁 Project Structure

```
NyaySaathi/
├── public/
│   ├── LogoSaathi.svg       # Main logo
│   ├── Collapse.svg         # Sidebar collapse icon
│   └── ...                  # Other static assets
├── src/
│   ├── components/
│   │   ├── ChatInterface/
│   │   │   └── Chatbot.jsx  # AI chat component
│   │   ├── Footer/
│   │   │   └── Footer.jsx   # Site footer
│   │   ├── Main/
│   │   │   └── Hero.jsx     # Homepage content
│   │   ├── Navbar/
│   │   │   └── Nav.jsx      # Navigation bar
│   │   └── Sidebar/
│   │       └── SideBar.jsx  # Collapsible sidebar
│   ├── App.jsx              # Main app component with routing
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── eslint.config.js         # ESLint configuration
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── package.json             # Dependencies and scripts
```

---

## 🎯 Key Features Explained

### Auto-Expanding Chat Input

The chat interface features a smart textarea that automatically expands vertically as you type longer messages, with a maximum height limit to prevent overflow.

### Responsive Sidebar

A collapsible sidebar that:

- Shows icons + labels when expanded
- Shows only icons when collapsed
- Automatically positions below the navbar
- Fully responsive across all screen sizes

### Interactive Accordion

Learning resources use Framer Motion-powered accordions for smooth expand/collapse animations with proper ARIA accessibility attributes.

### Adaptive Layout

The application intelligently adjusts padding and spacing based on screen size:

- Mobile: Compact layout with sidebar accommodation
- Tablet: Medium spacing with responsive images
- Desktop: Full layout with optimal content width

---

## 🤝 Contributing

We welcome contributions to NyaySaathi! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style and component structure
- Ensure all components are responsive (test on mobile, tablet, desktop)
- Add appropriate ARIA labels for accessibility
- Test thoroughly before submitting PR

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Sayoun Parui**

- GitHub: [@SAYOUNCDR](https://github.com/SAYOUNCDR)

---

## 🙏 Acknowledgments

- Indian Legal Database providers for verified legal information
- React and Tailwind CSS communities for excellent documentation
- All contributors who help make legal information more accessible

---

## 📞 Support

If you encounter any issues or have questions:

- Open an issue on [GitHub Issues](https://github.com/SAYOUNCDR/NyaySaathi/issues)
- Contact via the emergency help button in the app

---

<div align="center">

**Made with ❤️ for empowering citizens with legal knowledge**

⭐ Star this repo if you find it helpful!

</div>
