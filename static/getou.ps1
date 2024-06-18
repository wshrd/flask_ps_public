$OU = Get-ADOrganizationalUnit -SearchBase "OU=Accounts, DC=gusev, DC=int" -Filter * | Select-Object Name, DistinguishedName
$json = $OU | ConvertTo-Json
Write-Output $json
