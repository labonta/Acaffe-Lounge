param([ValidateSet('inspect','configure','status')][string]$Action='inspect')
$ErrorActionPreference='Stop'
$credentialRequest = "protocol=https`nhost=github.com`n`n"
$credentialLines = $credentialRequest | git credential fill
if ($LASTEXITCODE -ne 0) { throw 'Не удалось получить существующую авторизацию GitHub.' }
$credentialFields = @{}
foreach ($credentialLine in $credentialLines) {
  $credentialPair = $credentialLine -split '=',2
  if ($credentialPair.Count -eq 2) { $credentialFields[$credentialPair[0]]=$credentialPair[1] }
}
if (-not $credentialFields['password']) { throw 'Существующая авторизация GitHub не найдена.' }
$requestHeaders = @{
  'Authorization' = 'Bearer ' + $credentialFields['password']
  'Accept' = 'application/vnd.github+json'
  'X-GitHub-Api-Version' = '2022-11-28'
  'User-Agent' = 'Acaffe-Lounge-Publish'
}
$apiRoot='https://api.github.com/repos/labonta/Acaffe-Lounge'
try {
  $repository = Invoke-RestMethod -Uri $apiRoot -Headers $requestHeaders
  if ($repository.full_name -cne 'labonta/Acaffe-Lounge') { throw 'Ответ API относится к другому репозиторию.' }
  if ($Action -eq 'inspect') {
    [ordered]@{repository=$repository.full_name;private=$repository.private;admin=$repository.permissions.admin;push=$repository.permissions.push;pages=$repository.has_pages;default_branch=$repository.default_branch} | ConvertTo-Json
  } elseif ($Action -eq 'configure') {
    $configuration=@{build_type='legacy';source=@{branch='main';path='/'}} | ConvertTo-Json -Depth 4
    if ($repository.has_pages) { $method='Put' } else { $method='Post' }
    $null = Invoke-RestMethod -Method $method -Uri "$apiRoot/pages" -Headers $requestHeaders -ContentType 'application/json' -Body $configuration
    $pages = Invoke-RestMethod -Uri "$apiRoot/pages" -Headers $requestHeaders
    [ordered]@{url=$pages.html_url;status=$pages.status;build_type=$pages.build_type;branch=$pages.source.branch;path=$pages.source.path;https_enforced=$pages.https_enforced} | ConvertTo-Json
  } else {
    $pages=Invoke-RestMethod -Uri "$apiRoot/pages" -Headers $requestHeaders
    $build=Invoke-RestMethod -Uri "$apiRoot/pages/builds/latest" -Headers $requestHeaders
    [ordered]@{url=$pages.html_url;status=$pages.status;build_status=$build.status;commit=$build.commit;error=$build.error.message;updated_at=$build.updated_at} | ConvertTo-Json
  }
} finally {
  $credentialLines=$null
  $credentialFields.Clear()
  $requestHeaders.Clear()
}
