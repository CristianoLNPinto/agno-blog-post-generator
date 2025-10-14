# 🎨 Streamlit Interface Guide

## Overview

The Streamlit interface provides a beautiful, user-friendly web application for generating AI-powered blog posts with real-time progress tracking.

## Features

### 🎯 Main Features

1. **Topic Input**: Enter any topic you want to write about
2. **Real-Time Progress**: Watch the generation process in three phases:
   - 🔍 Phase 1: Research & Source Gathering
   - 📄 Phase 2: Content Extraction
   - ✍️ Phase 3: Blog Post Creation
3. **Multiple Views**: 
   - HTML formatted view with beautiful styling
   - Raw Markdown view
   - Download options (MD and HTML)
4. **Cache Control**: Toggle caching for search, scraping, and blog generation
5. **Example Topics**: Quick-start buttons with pre-filled topics

### 🚀 Getting Started

1. **Install Dependencies**
   ```bash
   make install
   # or
   pip install -e .
   ```

2. **Configure API Key**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. **Launch Streamlit**
   ```bash
   make run-streamlit
   # or
   streamlit run streamlit_app.py
   ```

4. **Open Browser**
   - Navigate to http://localhost:8501
   - The interface will open automatically

## How to Use

### Basic Usage

1. **Enter a Topic**
   - Type your blog topic in the text input field
   - Or click one of the example topics in the sidebar

2. **Configure Settings** (Optional)
   - Use the sidebar to enable/disable caching
   - Caching speeds up repeated requests

3. **Generate Blog Post**
   - Click the "🚀 Generate Blog Post" button
   - Watch the progress in real-time

4. **View Results**
   - Switch between HTML and Markdown views
   - Download the blog post in your preferred format

### Progress Tracking

The interface shows detailed progress for each phase:

#### Phase 1: Research
- Shows number of sources found
- Lists the top sources being used
- Indicates when research is complete

#### Phase 2: Content Extraction
- Shows scraping progress
- Displays number of articles successfully extracted
- Reports any failed extractions

#### Phase 3: Blog Writing
- Indicates when AI is writing
- Shows final blog post statistics
- Displays character count and source count

### Output Options

#### HTML View
- Beautifully formatted with custom CSS
- Styled headings and sections
- Professional typography
- Color-coded elements

#### Markdown View
- Raw markdown format
- Easy to copy and paste
- Compatible with any markdown editor

#### Download Options
- **Markdown (.md)**: Plain text markdown file
- **HTML (.html)**: Standalone HTML file with embedded styles

## Tips & Best Practices

### Topic Selection
- ✅ Be specific: "The Impact of AI on Healthcare in 2024"
- ✅ Include context: "How Quantum Computing is Revolutionizing Cybersecurity"
- ❌ Too broad: "Technology"
- ❌ Too vague: "Things"

### Cache Settings
- **Enable all caches** for faster repeated generations
- **Disable caches** when you want fresh content
- **Search cache**: Reuses found articles
- **Scrape cache**: Reuses extracted content
- **Blog cache**: Reuses generated posts

### Performance
- First generation: 1-3 minutes (depending on topic)
- Cached generation: 5-10 seconds
- Network speed affects scraping time

## Troubleshooting

### Common Issues

**Issue**: "No API key found"
- **Solution**: Make sure `.env` file exists with `GOOGLE_API_KEY=your_key`

**Issue**: "Failed to find articles"
- **Solution**: Try a different topic or disable search cache

**Issue**: "Scraping failed"
- **Solution**: Some websites block scraping; the tool will skip them automatically

**Issue**: "Streamlit not found"
- **Solution**: Run `pip install streamlit` or `make install`

### Getting Help

If you encounter issues:
1. Check the terminal for error messages
2. Verify your API key is valid
3. Try disabling all caches
4. Check your internet connection

## Advanced Features

### Session State
- The app maintains session state
- Previous blog posts are stored during the session
- Refresh the page to clear session state

### Custom Styling
- The interface uses custom CSS for beautiful formatting
- HTML output includes embedded styles
- Gradient colors and modern design

### Async Processing
- The app uses async/await for efficient processing
- Multiple operations can run concurrently
- Progress updates happen in real-time

## Example Workflow

1. **Launch the app**
   ```bash
   make run-streamlit
   ```

2. **Select an example topic** or enter your own
   - Example: "The Future of AI in Healthcare"

3. **Click Generate** and watch the progress:
   - ✅ Research: Found 5 articles
   - ✅ Extraction: Scraped 4 articles
   - ✅ Writing: Generated 2,500 character blog post

4. **Review the output** in HTML view
   - Read the formatted blog post
   - Check sources and citations

5. **Download** in your preferred format
   - Markdown for editing
   - HTML for publishing

## Screenshots

### Main Interface
- Clean, modern design
- Gradient header
- Intuitive controls

### Progress Tracking
- Real-time phase updates
- Detailed status messages
- Visual feedback

### Output Display
- Professional formatting
- Multiple view options
- Easy downloads

## Next Steps

- Try different topics
- Experiment with cache settings
- Download and edit blog posts
- Integrate with your content workflow

---

**Enjoy creating amazing blog posts with AI! 🎨✨**
