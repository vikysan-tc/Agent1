#!/bin/bash

# Deployment script for Landing Page and Dashboard
# This script prepares the files for production deployment

echo "🚀 Preparing Landing Page for Deployment..."

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Please run this script from the resolvx_landing directory."
    exit 1
fi

# Create a production build directory
BUILD_DIR="build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy all necessary files
echo "📦 Copying files..."
cp index.html "$BUILD_DIR/"
cp dashboard.html "$BUILD_DIR/"
cp *.css "$BUILD_DIR/" 2>/dev/null
cp *.js "$BUILD_DIR/" 2>/dev/null

# Update dashboard.js for production
echo "⚙️  Configuring for production..."
if [ -f "$BUILD_DIR/dashboard.js" ]; then
    # Update USE_LOCAL_PROXY to false
    sed -i.bak 's/const USE_LOCAL_PROXY = true;/const USE_LOCAL_PROXY = false;/g' "$BUILD_DIR/dashboard.js"
    rm "$BUILD_DIR/dashboard.js.bak" 2>/dev/null
fi

# Create netlify.toml if it doesn't exist
if [ ! -f "netlify.toml" ]; then
    echo "📝 Creating netlify.toml..."
    cat > "$BUILD_DIR/netlify.toml" << EOF
[build]
  publish = "."
  command = "echo 'No build step required'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
fi

# Create vercel.json if it doesn't exist
if [ ! -f "vercel.json" ]; then
    echo "📝 Creating vercel.json..."
    cat > "$BUILD_DIR/vercel.json" << EOF
{
  "version": 2,
  "builds": [
    {
      "src": "**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
EOF
fi

echo "✅ Build complete! Files are ready in the '$BUILD_DIR' directory."
echo ""
echo "📤 Next steps:"
echo "   1. Review files in '$BUILD_DIR'"
echo "   2. Deploy to your hosting platform:"
echo "      - Netlify: drag and drop '$BUILD_DIR' folder"
echo "      - Vercel: vercel --prod"
echo "      - GitHub Pages: push to gh-pages branch"
echo ""
echo "💡 Make sure to:"
echo "   - Verify CORS is configured on CRM server"
echo "   - Test the dashboard after deployment"
echo "   - Check browser console for errors"

