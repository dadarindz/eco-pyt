#!/usr/bin/env bash
# TP2 – Azure App Service (PaaS) : réalisation complète en Azure CLI avec captures.
# Usage : ID=xx NUM=1234 ENTREPRISE="Nom" bash tp2.sh <etape>
#   etapes : login | creation | v1 | v2 | quotas | suppression
set -e
cd "$(dirname "$0")"
OUTILS=../outils
export NODE_PATH=$(npm root -g)
export TP2_RG="rg-tp2-$ID" TP2_APP="app-tp2-$ID-$NUM" TP2_PLAN="asp-tp2-$ID"
cap() { node $OUTILS/capture_terminal.js "$1" "captures/$2.png"; echo "capture $2"; }
host() { az webapp show -g "$TP2_RG" -n "$TP2_APP" --query defaultHostName -o tsv; }

case "$1" in
login)
  az login --use-device-code
  az account set --subscription "Azure for Students"
  cap 'az account list -o table' 01-account-list
  cap 'az account show --query "{Nom:name,Etat:state}" -o table' 02-account-show
  cap 'az version' 03-az-version ;;
creation)
  cap 'az group create --name "$TP2_RG" --location francecentral -o table' 04-group-create
  cap 'az appservice plan create --resource-group "$TP2_RG" --name "$TP2_PLAN" --sku F1 --location francecentral -o table' 05-plan-create
  cap 'az webapp create --resource-group "$TP2_RG" --plan "$TP2_PLAN" --name "$TP2_APP" --runtime "ASPNET:V4.8" --query "{Nom:name,Etat:state,Domaine:defaultHostName}" -o table' 06-webapp-create
  cap 'az resource list --resource-group "$TP2_RG" --query "[].{Nom:name,Type:type,Emplacement:location}" -o table' 07-resources
  cap 'az appservice plan show --resource-group "$TP2_RG" --name "$TP2_PLAN" --query "{Nom:name,SKU:sku.name,Niveau:sku.tier,Linux:reserved}" -o table' 08-plan-show
  cap 'az webapp show --resource-group "$TP2_RG" --name "$TP2_APP" --query "{Nom:name,Etat:state,Plan:serverFarmId}" -o table' 09-webapp-show
  cap 'az webapp update --resource-group "$TP2_RG" --name "$TP2_APP" --https-only true --query "{Nom:name,HTTPSuniquement:httpsOnly}" -o table' 10-https-only
  sleep 30; node $OUTILS/capture_page.js "https://$(host)" captures/11-page-defaut.png ;;
v1)
  mkdir -p ~/tp2-web
  sed "s/__ENTREPRISE__/$ENTREPRISE/g; s/__ID__/$ID/g" site/index.html > ~/tp2-web/index.html
  cd ~/tp2-web; C=$OLDPWD/captures; O=$OLDPWD/$OUTILS
  node $O/capture_terminal.js 'cat index.html && ls -l index.html' $C/12-index-v1.png
  rm -f site-v1.zip
  node $O/capture_terminal.js 'zip site-v1.zip index.html && unzip -l site-v1.zip' $C/13-zip-v1.png
  node $O/capture_terminal.js 'az webapp deploy --resource-group "$TP2_RG" --name "$TP2_APP" --src-path site-v1.zip --type zip --clean true --query "{Statut:provisioningState,Message:message}" -o table' $C/14-deploy-v1.png
  export TP2_HOST=$(host)
  node $O/capture_terminal.js 'printf "https://%s\n" "$TP2_HOST" && curl -sS -o /dev/null -w "HTTP %{http_code}\n" "https://$TP2_HOST"' $C/15-url-curl.png
  sleep 10; node $O/capture_page.js "https://$TP2_HOST" $C/16-site-v1.png ;;
v2)
  cd ~/tp2-web; C=$OLDPWD/captures; O=$OLDPWD/$OUTILS
  sed -i 's/Version 1/Version 2/' index.html
  sed -i "s#<p>Application publiée#<p>Nous proposons des solutions Cloud adaptées aux besoins des entreprises.</p>\n    <p>Application publiée#" index.html
  node $O/capture_terminal.js "grep -n 'Version\|Nous proposons' index.html" $C/17-modif-v2.png
  export TP2_HOST=$(host)
  node $O/capture_page.js "https://$TP2_HOST" $C/18-site-encore-v1.png
  rm -f site-v2.zip
  node $O/capture_terminal.js 'zip site-v2.zip index.html && unzip -l site-v2.zip' $C/19-zip-v2.png
  node $O/capture_terminal.js 'az webapp deploy --resource-group "$TP2_RG" --name "$TP2_APP" --src-path site-v2.zip --type zip --clean true --query "{Statut:provisioningState,Message:message}" -o table' $C/20-deploy-v2.png
  sleep 10; node $O/capture_page.js "https://$TP2_HOST" $C/21-site-v2.png ;;
quotas)
  export SUB=$(az account show --query id -o tsv)
  cap 'az rest --method get --url "https://management.azure.com/subscriptions/$SUB/resourceGroups/$TP2_RG/providers/Microsoft.Web/sites/$TP2_APP/usages?api-version=2023-12-01" --query "value[].{Quota:name.value,Utilise:currentValue,Limite:limit,Unite:unit}" -o table' 22-quotas
  cap 'az webapp show --resource-group "$TP2_RG" --name "$TP2_APP" --query "{Plan:serverFarmId,Etat:state,Quota:usageState}" -o table && az appservice plan show -g "$TP2_RG" -n "$TP2_PLAN" --query "{Plan:name,Tarif:sku.tier,SKU:sku.name}" -o table' 23-plan-f1 ;;
suppression)
  az group delete --name "$TP2_RG" --yes
  cap 'az group exists --name "$TP2_RG"' 24-group-exists ;;
esac
