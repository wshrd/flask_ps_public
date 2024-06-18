Get-MailboxExportRequest | ForEach-Object { "$($_.Name) $($_.Status)" }
#Get-MailboxExportRequest | Select-Object Name, Status | Format-List