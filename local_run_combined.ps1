# Combined Local Run Script for Agent1 Project
# This script starts all services required for local development:
# 1. CRM Server (Spring Boot on port 8080)
# 2. Greeter Agent Server (Flask on port 5000)
# 3. Email Processor Watcher (Gmail API polling)

param(
    [string]$CrmServerPath = "C:\Users\ANIKET R SHANKAR\Desktop\lablab_ibm\CRM-Server\orchestrate",
    # Email Processor Gmail credentials (for watching reachus.sherlox@gmail.com)
    [string]$GmailAccessToken = "",
    [string]$GmailRefreshToken = "",
    [string]$GmailClientId = "",
    [string]$GmailClientSecret = "",
    # Greeter Agent Gmail credentials (for sending from noreply-sherlox@gmail.com)
    [string]$GmailAccessTokenNoReply = "",
    [string]$GmailRefreshTokenNoReply = "",
    [string]$GmailClientIdNoReply = "",
    [string]$GmailClientSecretNoReply = "",
    [string]$OrchestrateUrl = "",
    [string]$OrchestrateApiKey = "",
    [switch]$SkipCrmServer = $false,
    [switch]$SkipGreeterAgent = $false,
    [switch]$SkipEmailProcessor = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Agent1 Combined Local Run Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Java is installed (required for CRM server)
if (-not $SkipCrmServer) {
    $javaVersion = java -version 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Java not found. CRM Server will not start." -ForegroundColor Yellow
        Write-Host "Install Java 17+ to run the CRM server." -ForegroundColor Yellow
        $SkipCrmServer = $true
    } else {
        Write-Host "Java found: $javaVersion" -ForegroundColor Green
    }
}

# Check if Python is installed
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.11+." -ForegroundColor Red
    exit 1
}
Write-Host "Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Set environment variables
Write-Host "Setting environment variables..." -ForegroundColor Yellow

# CRM Server URL
$env:CRM_SERVER_URL = "http://localhost:8080"
Write-Host "  CRM_SERVER_URL = $env:CRM_SERVER_URL" -ForegroundColor Gray

# Email Processor Gmail Configuration (for watching reachus.sherlox@gmail.com)
Write-Host "  Email Processor Gmail Config:" -ForegroundColor Cyan
if ($GmailAccessToken) {
    $env:GMAIL_ACCESS_TOKEN = $GmailAccessToken
    Write-Host "    GMAIL_ACCESS_TOKEN = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_ACCESS_TOKEN) {
    Write-Host "    GMAIL_ACCESS_TOKEN = [FROM ENV]" -ForegroundColor Gray
} else {
    Write-Host "    WARNING: GMAIL_ACCESS_TOKEN not set (for email processor)" -ForegroundColor Yellow
}

if ($GmailRefreshToken) {
    $env:GMAIL_REFRESH_TOKEN = $GmailRefreshToken
    Write-Host "    GMAIL_REFRESH_TOKEN = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_REFRESH_TOKEN) {
    Write-Host "    GMAIL_REFRESH_TOKEN = [FROM ENV]" -ForegroundColor Gray
}

if ($GmailClientId) {
    $env:GMAIL_CLIENT_ID = $GmailClientId
    Write-Host "    GMAIL_CLIENT_ID = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_CLIENT_ID) {
    Write-Host "    GMAIL_CLIENT_ID = [FROM ENV]" -ForegroundColor Gray
}

if ($GmailClientSecret) {
    $env:GMAIL_CLIENT_SECRET = $GmailClientSecret
    Write-Host "    GMAIL_CLIENT_SECRET = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_CLIENT_SECRET) {
    Write-Host "    GMAIL_CLIENT_SECRET = [FROM ENV]" -ForegroundColor Gray
}

# Gmail Watch Email
$env:GMAIL_WATCH_EMAIL = "reachus.sherlox@gmail.com"
Write-Host "    GMAIL_WATCH_EMAIL = $env:GMAIL_WATCH_EMAIL" -ForegroundColor Gray

# Greeter Agent Gmail Configuration (for sending from noreply-sherlox@gmail.com)
Write-Host "  Greeter Agent Gmail Config:" -ForegroundColor Cyan
if ($GmailAccessTokenNoReply) {
    $env:GMAIL_ACCESS_TOKEN_NO_REPLY = $GmailAccessTokenNoReply
    Write-Host "    GMAIL_ACCESS_TOKEN_NO_REPLY = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_ACCESS_TOKEN_NO_REPLY) {
    Write-Host "    GMAIL_ACCESS_TOKEN_NO_REPLY = [FROM ENV]" -ForegroundColor Gray
} else {
    Write-Host "    GMAIL_ACCESS_TOKEN_NO_REPLY = [NOT SET - will use OAuth2 if available]" -ForegroundColor Gray
}

if ($GmailRefreshTokenNoReply) {
    $env:GMAIL_REFRESH_TOKEN_NO_REPLY = $GmailRefreshTokenNoReply
    Write-Host "    GMAIL_REFRESH_TOKEN_NO_REPLY = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_REFRESH_TOKEN_NO_REPLY) {
    Write-Host "    GMAIL_REFRESH_TOKEN_NO_REPLY = [FROM ENV]" -ForegroundColor Gray
}

if ($GmailClientIdNoReply) {
    $env:GMAIL_CLIENT_ID_NO_REPLY = $GmailClientIdNoReply
    Write-Host "    GMAIL_CLIENT_ID_NO_REPLY = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_CLIENT_ID_NO_REPLY) {
    Write-Host "    GMAIL_CLIENT_ID_NO_REPLY = [FROM ENV]" -ForegroundColor Gray
}

if ($GmailClientSecretNoReply) {
    $env:GMAIL_CLIENT_SECRET_NO_REPLY = $GmailClientSecretNoReply
    Write-Host "    GMAIL_CLIENT_SECRET_NO_REPLY = [SET]" -ForegroundColor Gray
} elseif ($env:GMAIL_CLIENT_SECRET_NO_REPLY) {
    Write-Host "    GMAIL_CLIENT_SECRET_NO_REPLY = [FROM ENV]" -ForegroundColor Gray
}

# Greeter Agent Configuration
if ($OrchestrateUrl) {
    $env:ORCHESTRATE_URL = $OrchestrateUrl
    Write-Host "  ORCHESTRATE_URL = $env:ORCHESTRATE_URL" -ForegroundColor Gray
} elseif ($env:ORCHESTRATE_URL) {
    Write-Host "  ORCHESTRATE_URL = [FROM ENV]" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: ORCHESTRATE_URL not set (required for greeter agent)" -ForegroundColor Yellow
}

if ($OrchestrateApiKey) {
    $env:ORCHESTRATE_API_KEY = $OrchestrateApiKey
    Write-Host "  ORCHESTRATE_API_KEY = [SET]" -ForegroundColor Gray
} elseif ($env:ORCHESTRATE_API_KEY) {
    Write-Host "  ORCHESTRATE_API_KEY = [FROM ENV]" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: ORCHESTRATE_API_KEY not set (required for greeter agent)" -ForegroundColor Yellow
}

$env:AGENT_NAME = "greeter"
$env:WEBHOOK_PORT = "5000"
$env:WEBHOOK_HOST = "0.0.0.0"

# Email Processor Configuration
$env:AGENT_WEBHOOK_URL = "http://localhost:5000/webhook"
$env:AGENT_WEBHOOK_URL_LOCAL = "http://localhost:5000/webhook"
$env:ENVIRONMENT = "local"
$env:GMAIL_POLL_INTERVAL = "60"
Write-Host "  AGENT_WEBHOOK_URL = $env:AGENT_WEBHOOK_URL" -ForegroundColor Gray
Write-Host "  ENVIRONMENT = $env:ENVIRONMENT" -ForegroundColor Gray

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Services..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start CRM Server
if (-not $SkipCrmServer) {
    Write-Host "1. Starting CRM Server on port 8080..." -ForegroundColor Yellow
    
    if (-not (Test-Path $CrmServerPath)) {
        Write-Host "   ERROR: CRM Server path not found: $CrmServerPath" -ForegroundColor Red
        Write-Host "   Please update the -CrmServerPath parameter" -ForegroundColor Red
        $SkipCrmServer = $true
    } else {
        Push-Location $CrmServerPath
        
        # Check if Maven wrapper exists
        if (Test-Path ".\mvnw.cmd") {
            Write-Host "   Using Maven wrapper..." -ForegroundColor Gray
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$CrmServerPath'; .\mvnw.cmd spring-boot:run" -WindowStyle Normal
            Write-Host "   CRM Server starting in new window..." -ForegroundColor Green
        } elseif (Get-Command mvn -ErrorAction SilentlyContinue) {
            Write-Host "   Using system Maven..." -ForegroundColor Gray
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$CrmServerPath'; mvn spring-boot:run" -WindowStyle Normal
            Write-Host "   CRM Server starting in new window..." -ForegroundColor Green
        } else {
            Write-Host "   ERROR: Maven not found. Please install Maven or use the Maven wrapper." -ForegroundColor Red
            $SkipCrmServer = $true
        }
        
        Pop-Location
        
        # Wait for CRM server to start
        if (-not $SkipCrmServer) {
            Write-Host "   Waiting for CRM server to start (max 30 seconds)..." -ForegroundColor Gray
            $crmReady = $false
            for ($i = 0; $i -lt 30; $i++) {
                Start-Sleep -Seconds 1
                try {
                    $response = Invoke-WebRequest -Uri "http://localhost:8080/actuator/health" -TimeoutSec 1 -ErrorAction SilentlyContinue
                    if ($response.StatusCode -eq 200) {
                        $crmReady = $true
                        Write-Host "   CRM Server is ready!" -ForegroundColor Green
                        break
                    }
                } catch {
                    # Server not ready yet
                }
            }
            if (-not $crmReady) {
                Write-Host "   WARNING: CRM Server may not be ready yet. Continuing..." -ForegroundColor Yellow
            }
        }
    }
    Write-Host ""
}

# Start Greeter Agent Server
if (-not $SkipGreeterAgent) {
    Write-Host "2. Starting Greeter Agent Server on port 5000..." -ForegroundColor Yellow
    
    $greeterAgentPath = Join-Path $PSScriptRoot "greeter_agent"
    if (-not (Test-Path $greeterAgentPath)) {
        Write-Host "   ERROR: Greeter agent directory not found: $greeterAgentPath" -ForegroundColor Red
        $SkipGreeterAgent = $true
    } else {
        # Check if requirements are installed
        $requirementsFile = Join-Path $greeterAgentPath "requirements.txt"
        if (Test-Path $requirementsFile) {
            Write-Host "   Installing/updating Python dependencies..." -ForegroundColor Gray
            Push-Location $greeterAgentPath
            python -m pip install -q -r requirements.txt
            Pop-Location
        }
        
        Push-Location $greeterAgentPath
        # Set environment variables for greeter agent (all tools are in greeter_agent folder)
        # Use separate Gmail credentials for greeter agent (NO_REPLY variants)
        $greeterEnvVars = "cd '$greeterAgentPath'; "
        $greeterEnvVars += "`$env:CRM_SERVER_URL='http://localhost:8080'; "
        $greeterEnvVars += "`$env:ORCHESTRATE_URL='$env:ORCHESTRATE_URL'; "
        $greeterEnvVars += "`$env:ORCHESTRATE_API_KEY='$env:ORCHESTRATE_API_KEY'; "
        $greeterEnvVars += "`$env:AGENT_NAME='greeter'; "
        $greeterEnvVars += "`$env:WEBHOOK_PORT='5000'; "
        $greeterEnvVars += "`$env:PYTHONPATH='$greeterAgentPath'; "
        # Add greeter agent Gmail credentials (NO_REPLY variants)
        if ($env:GMAIL_ACCESS_TOKEN_NO_REPLY) {
            $greeterEnvVars += "`$env:GMAIL_ACCESS_TOKEN_NO_REPLY='$env:GMAIL_ACCESS_TOKEN_NO_REPLY'; "
        }
        if ($env:GMAIL_REFRESH_TOKEN_NO_REPLY) {
            $greeterEnvVars += "`$env:GMAIL_REFRESH_TOKEN_NO_REPLY='$env:GMAIL_REFRESH_TOKEN_NO_REPLY'; "
        }
        if ($env:GMAIL_CLIENT_ID_NO_REPLY) {
            $greeterEnvVars += "`$env:GMAIL_CLIENT_ID_NO_REPLY='$env:GMAIL_CLIENT_ID_NO_REPLY'; "
        }
        if ($env:GMAIL_CLIENT_SECRET_NO_REPLY) {
            $greeterEnvVars += "`$env:GMAIL_CLIENT_SECRET_NO_REPLY='$env:GMAIL_CLIENT_SECRET_NO_REPLY'; "
        }
        $greeterEnvVars += "python server.py"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $greeterEnvVars -WindowStyle Normal
        Pop-Location
        
        Write-Host "   Greeter Agent Server starting in new window..." -ForegroundColor Green
        
        # Wait for greeter agent to start
        Write-Host "   Waiting for Greeter Agent to start (max 10 seconds)..." -ForegroundColor Gray
        $greeterReady = $false
        for ($i = 0; $i -lt 10; $i++) {
            Start-Sleep -Seconds 1
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 1 -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    $greeterReady = $true
                    Write-Host "   Greeter Agent Server is ready!" -ForegroundColor Green
                    break
                }
            } catch {
                # Server not ready yet
            }
        }
        if (-not $greeterReady) {
            Write-Host "   WARNING: Greeter Agent may not be ready yet. Continuing..." -ForegroundColor Yellow
        }
    }
    Write-Host ""
}

# Start Email Processor Watcher
if (-not $SkipEmailProcessor) {
    Write-Host "3. Starting Email Processor Watcher..." -ForegroundColor Yellow
    
    $emailProcessorPath = Join-Path $PSScriptRoot "email_processor"
    if (-not (Test-Path $emailProcessorPath)) {
        Write-Host "   ERROR: Email processor directory not found: $emailProcessorPath" -ForegroundColor Red
        $SkipEmailProcessor = $true
    } else {
        # Check if requirements are installed
        $requirementsFile = Join-Path $emailProcessorPath "requirements.txt"
        if (Test-Path $requirementsFile) {
            Write-Host "   Installing/updating Python dependencies..." -ForegroundColor Gray
            Push-Location $emailProcessorPath
            python -m pip install -q -r requirements.txt
            Pop-Location
        }
        
        Push-Location $emailProcessorPath
        # Set environment variables for email processor (use regular Gmail credentials, not NO_REPLY)
        $emailProcessorEnvVars = "cd '$emailProcessorPath'; "
        $emailProcessorEnvVars += "`$env:CRM_SERVER_URL='http://localhost:8080'; "
        $emailProcessorEnvVars += "`$env:GMAIL_WATCH_EMAIL='$env:GMAIL_WATCH_EMAIL'; "
        # Add email processor Gmail credentials (regular variants, not NO_REPLY)
        if ($env:GMAIL_ACCESS_TOKEN) {
            $emailProcessorEnvVars += "`$env:GMAIL_ACCESS_TOKEN='$env:GMAIL_ACCESS_TOKEN'; "
        }
        if ($env:GMAIL_REFRESH_TOKEN) {
            $emailProcessorEnvVars += "`$env:GMAIL_REFRESH_TOKEN='$env:GMAIL_REFRESH_TOKEN'; "
        }
        if ($env:GMAIL_CLIENT_ID) {
            $emailProcessorEnvVars += "`$env:GMAIL_CLIENT_ID='$env:GMAIL_CLIENT_ID'; "
        }
        if ($env:GMAIL_CLIENT_SECRET) {
            $emailProcessorEnvVars += "`$env:GMAIL_CLIENT_SECRET='$env:GMAIL_CLIENT_SECRET'; "
        }
        $emailProcessorEnvVars += "`$env:AGENT_WEBHOOK_URL='$env:AGENT_WEBHOOK_URL'; "
        $emailProcessorEnvVars += "`$env:ENVIRONMENT='local'; "
        $emailProcessorEnvVars += "python gmail_watcher.py"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $emailProcessorEnvVars -WindowStyle Normal
        Pop-Location
        
        Write-Host "   Email Processor Watcher starting in new window..." -ForegroundColor Green
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All Services Started!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services running:" -ForegroundColor Green
if (-not $SkipCrmServer) {
    Write-Host "  - CRM Server: http://localhost:8080" -ForegroundColor White
    Write-Host "    API: http://localhost:8080/api/tickets" -ForegroundColor Gray
}
if (-not $SkipGreeterAgent) {
    Write-Host "  - Greeter Agent Server: http://localhost:5000" -ForegroundColor White
    Write-Host "    Webhook: http://localhost:5000/webhook" -ForegroundColor Gray
    Write-Host "    Health: http://localhost:5000/health" -ForegroundColor Gray
}
if (-not $SkipEmailProcessor) {
    Write-Host "  - Email Processor: Watching $env:GMAIL_WATCH_EMAIL" -ForegroundColor White
    Write-Host "    Polling interval: $env:GMAIL_POLL_INTERVAL seconds" -ForegroundColor Gray
}
Write-Host ""
Write-Host "To stop services, close the PowerShell windows." -ForegroundColor Yellow
Write-Host ""
Write-Host "Testing:" -ForegroundColor Cyan
Write-Host "  1. Test CRM Server: Invoke-WebRequest http://localhost:8080/api/tickets" -ForegroundColor Gray
Write-Host "  2. Test Greeter Agent: Invoke-WebRequest http://localhost:5000/health" -ForegroundColor Gray
Write-Host "  3. Send a test email to $env:GMAIL_WATCH_EMAIL to trigger the email processor" -ForegroundColor Gray
Write-Host ""

