$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
# Stops only this project's containers, then archives the exact run directory.
python -c "from final_validation import archive; archive()"
if ($LASTEXITCODE -ne 0) { throw 'Reset/archive failed' }
