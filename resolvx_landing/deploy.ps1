# Deployment script for Landing Page and Dashboard (PowerShell)
# This script prepares the files for production deployment

Write-Host "🚀 Preparing Landing Page for Deployment..." -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "index.html")) {
    Write-Host "❌ Error: index.html not found. Please run this script from the resolvx_landing directory." -ForegroundColor Red
    exit 1
}

# Create a production build directory
$BUILD_DIR = "build"
if (Test-Path $BUILD_DIR) {
    Remove-Item -Recurse -Force $BUILD_DIR
}
New-Item -ItemType Directory -Path $BUILD_DIR | Out-Null

# Copy all necessary files
Write-Host "📦 Copying files..." -ForegroundColor Yellow
Copy-Item "index.html" $BUILD_DIR
Copy-Item "dashboard.html" $BUILD_DIR
Copy-Item "*.css" $BUILD_DIR -ErrorAction SilentlyContinue
Copy-Item "*.js" $BUILD_DIR -ErrorAction SilentlyContinue

# Update dashboard.js for production
Write-Host "⚙️  Configuring for production..." -ForegroundColor Yellow
$dashboardJs = Join-Path $BUILD_DIR "dashboard.js"
if (Test-Path $dashboardJs) {
    $content = Get-Content $dashboardJs -Raw
    $content = $content -replace 'const USE_LOCAL_PROXY = true;', 'const USE_LOCAL_PROXY = false;'
    Set-Content $dashboardJs $content
}

# Create netlify.toml if it doesn't exist
if (-not (Test-Path "netlify.toml")) {
    Write-Host "📝 Creating netlify.toml..." -ForegroundColor Yellow
    $netlifyConfig = @"
[build]
  publish = "."
  command = "echo 'No build step required'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"@
    Set-Content (Join-Path $BUILD_DIR "netlify.toml") $netlifyConfig
}

# Create vercel.json if it doesn't exist
if (-not (Test-Path "vercel.json")) {
    Write-Host "📝 Creating vercel.json..." -ForegroundColor Yellow
    $vercelConfig = @"
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
"@
    Set-Content (Join-Path $BUILD_DIR "vercel.json") $vercelConfig
}

Write-Host "✅ Build complete! Files are ready in the '$BUILD_DIR' directory." -ForegroundColor Green
Write-Host ""
Write-Host "📤 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Review files in '$BUILD_DIR'"
Write-Host "   2. Deploy to your hosting platform:"
Write-Host "      - Netlify: drag and drop '$BUILD_DIR' folder"
Write-Host "      - Vercel: vercel --prod"
Write-Host "      - GitHub Pages: push to gh-pages branch"
Write-Host ""
Write-Host "💡 Make sure to:" -ForegroundColor Yellow
Write-Host "   - Verify CORS is configured on CRM server"
Write-Host "   - Test the dashboard after deployment"
Write-Host "   - Check browser console for errors"

