param(
    [string]$mailbox
)
$filepath = '\\s-veeam\EMAIL_ARCHIVES\2024\'+$mailbox+'_mail.pst'
New-MailboxExportRequest -Mailbox $mailbox -FilePath $filepath -Name $mailbox
