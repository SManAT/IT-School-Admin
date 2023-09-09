Remove-AzureADUser -ObjectID {% principal %}
Write-Host "Deleted {% principal %} ..."
