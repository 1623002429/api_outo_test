param(
    [string]$Keyword = "",
    [switch]$ServeReport
)

$ErrorActionPreference = "Stop"

function Set-ValidJavaHome {
    if ($env:JAVA_HOME -and (Test-Path (Join-Path $env:JAVA_HOME "bin\java.exe"))) {
        return
    }

    $candidates = @(
        "C:\Program Files\Java\jdk-25",
        "C:\Program Files\Java\jdk1.8.0_261",
        "C:\Program Files\Java\jre1.8.0_261"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path (Join-Path $candidate "bin\java.exe")) {
            $env:JAVA_HOME = $candidate
            $env:Path = "$candidate\bin;$env:Path"
            Write-Host "Using JAVA_HOME=$candidate"
            return
        }
    }

    Write-Warning "JAVA_HOME is invalid and no local Java installation was found. Allure report generation may fail."
}

if ($Keyword) {
    pytest -k $Keyword
} else {
    pytest
}

Set-ValidJavaHome

if ($ServeReport) {
    allure serve reports/allure-results
} else {
    allure generate reports/allure-results -o reports/allure-report --clean
}
