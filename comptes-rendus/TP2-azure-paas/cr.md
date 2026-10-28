# TP 2 : Déploiement d'une application Web sur Azure App Service (PaaS)
> __NOM__ __PRENOM__ | Groupe __GROUPE__ | XTI304 – Fondamentaux du Cloud Computing
## Étape 1 : Vérification de l'abonnement Azure avec Azure CLI
Les commandes ont été exécutées dans un terminal Bash avec Azure CLI, connecté au compte Azure for Students.
```
az account list -o table
az account show --query "{Nom:name,Etat:state}" -o table
```
![Liste des abonnements du compte](captures/01-account-list.png)
![Abonnement actif et son état](captures/02-account-show.png)
**Question 1.** La commande az account list affiche tous les abonnements auxquels le compte a accès, avec beaucoup d'informations (nom, cloud, identifiant de l'abonnement, identifiant du tenant, état et abonnement par défaut). La commande az account show affiche seulement l'abonnement actuellement utilisé. Avec l'option --query, on ne garde que deux champs (le nom et l'état) et on les renomme en Nom et Etat. La première donne donc une vue complète de tous les abonnements, la deuxième une vue filtrée de l'abonnement actif.
![Résultat de la commande az version](captures/03-az-version.png)
**Question 2.** La version d'Azure CLI installée est la __VERSION_AZ__ (valeur azure-cli affichée par az version).
## Étape 2 : Créer une application Web et son plan gratuit
### 2.1 Création de l'application Web
Le groupe de ressources, le plan App Service gratuit F1 et l'application Web (pile ASP.NET V4.8, Windows, région France Central) ont été créés avec les commandes suivantes :
```
az group create --name rg-tp2-__ID__ --location francecentral
az appservice plan create -g rg-tp2-__ID__ -n asp-tp2-__ID__ --sku F1
az webapp create -g rg-tp2-__ID__ -p asp-tp2-__ID__ -n __APP__ --runtime "ASPNET:V4.8"
```
![Création du groupe de ressources](captures/04-group-create.png)
![Création du plan App Service F1](captures/05-plan-create.png)
![Création de l'application Web](captures/06-webapp-create.png)
### 2.2 Vérification de l'application créée
Le groupe de ressources contient bien les deux ressources : l'application Web et son plan App Service.
![Ressources du groupe rg-tp2-__ID__](captures/07-resources.png)
En ouvrant le domaine par défaut, la page d'accueil Azure s'affiche car aucune page n'a encore été publiée.
![Page par défaut de l'application](captures/11-page-defaut.png)
**Question 3.** La Web App est l'application elle-même : elle contient le code, la configuration et possède l'URL publique. L'App Service Plan représente les ressources de calcul (processeur, mémoire, stockage, région, niveau tarifaire) sur lesquelles une ou plusieurs applications s'exécutent. Le statut Exécution signifie seulement que l'application est démarrée, pas que notre page est publiée : à ce moment, l'URL affiche encore la page par défaut d'Azure.
### 2.3 Vérification du plan gratuit avec Azure CLI
```
TP2_RG="rg-tp2-__ID__"
TP2_APP="__APP__"
TP2_PLAN="asp-tp2-__ID__"
```
![Vérification du plan tarifaire](captures/08-plan-show.png)
![État de l'application et plan associé](captures/09-webapp-show.png)
L'option HTTPS uniquement a été activée :
![Activation de HTTPS uniquement](captures/10-https-only.png)
**Question 4.** az appservice plan show affiche les informations du plan App Service : ici son nom, son SKU (F1), son niveau (Free) et s'il est sous Linux (false, donc Windows). az webapp show affiche les informations de l'application Web : son nom, son état (Running) et l'identifiant du plan auquel elle est rattachée (serverFarmId), ce qui confirme qu'elle utilise bien asp-tp2-__ID__.
## Étape 3 : Préparer une page HTML
### 3.1 et 3.2 Création et personnalisation du fichier
```
mkdir -p ~/tp2-web
cd ~/tp2-web
nano index.html
cat index.html
ls -l index.html
```
Le nom de l'entreprise a été remplacé par __ENTREPRISE__, la phrase de présentation a été adaptée et XX remplacé par mon identifiant.
![Contenu du fichier index.html](captures/12-index-v1.png)
**Question 5.** Le fichier index.html est enregistré dans le dossier ~/tp2-web du terminal, c'est-à-dire sur l'espace de travail local (Cloud Shell), et pas sur Azure App Service. Il n'est donc pas accessible depuis l'URL publique de l'application : tant qu'il n'a pas été déployé, l'application continue d'afficher la page par défaut.
**Question 6.** Le fichier est toujours stocké uniquement dans ~/tp2-web. Les modifications ne sont pas visibles sur l'application Web, car modifier un fichier en local ne change rien sur le serveur : il faut faire un déploiement pour l'envoyer sur App Service.
## Étape 4 : Déploiement et vérification de l'application Web
### 4.1 Préparation et déploiement
```
cd ~/tp2-web
zip site-v1.zip index.html
unzip -l site-v1.zip
az webapp deploy --resource-group "$TP2_RG" --name "$TP2_APP" --src-path site-v1.zip --type zip --clean true
```
![Création et vérification de l'archive](captures/13-zip-v1.png)
![Déploiement de la version 1](captures/14-deploy-v1.png)
**Question 7.** L'archive site-v1.zip est le paquet de déploiement envoyé à Azure App Service. Azure la décompresse dans le dossier racine du site (wwwroot). Le fichier index.html doit être directement à la racine de l'archive pour se retrouver à la racine du site et être servi comme page par défaut quand on ouvre l'URL. S'il était dans un sous-dossier, la page ne s'afficherait pas à l'adresse principale.
### 4.2 Récupération de l'URL publique
```
TP2_HOST=$(az webapp show --resource-group "$TP2_RG" --name "$TP2_APP" --query defaultHostName -o tsv)
printf 'https://%s\n' "$TP2_HOST"
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' "https://$TP2_HOST"
```
![URL publique et test HTTP](captures/15-url-curl.png)
**Question 8.** Le code HTTP 200 signifie « OK » : la requête a réussi et le serveur a bien renvoyé la page demandée.
### 4.3 Vérification dans le navigateur
![Application Web – Version 1](captures/16-site-v1.png)
**Question 9.** Non, contrairement au TP1, je n'ai pas eu besoin d'installer de serveur Web ni d'ouvrir des ports. Avec un service PaaS, Azure gère lui-même le système, le serveur Web et l'accès réseau en HTTP/HTTPS. Il suffit de déployer les fichiers de l'application.
## Étape 5 : Mise à jour et redéploiement
### 5.1 Modification de la page HTML
```
cd ~/tp2-web
sed -i 's/Version 1/Version 2/' index.html
grep 'Version' index.html
nano index.html
```
Une nouvelle phrase a été ajoutée : « Nous proposons des solutions Cloud adaptées aux besoins des entreprises. »
![Modification du fichier index.html](captures/17-modif-v2.png)
![Le site affiche toujours la version 1](captures/18-site-encore-v1.png)
**Question 9 (bis).** La page affiche encore Version 1 car la modification a été faite uniquement sur le fichier local. Le site sert les fichiers qui ont été déployés dans App Service, et la nouvelle version n'a pas encore été envoyée.
### 5.2 Création et déploiement de la nouvelle version
```
zip site-v2.zip index.html
unzip -l site-v2.zip
az webapp deploy --resource-group "$TP2_RG" --name "$TP2_APP" --src-path site-v2.zip --type zip --clean true
```
![Archive de la version 2](captures/19-zip-v2.png)
![Déploiement de la version 2](captures/20-deploy-v2.png)
![Application Web – Version 2](captures/21-site-v2.png)
**Question 10.** Non, aucune nouvelle application n'a été créée. La version 2 a été déployée sur la même application avec le même nom et la même URL. L'option --clean true remplace l'ancien contenu par le nouveau.
## Étape 6 : Limites et scalabilité d'Azure App Service
### 6.1 Limites du plan gratuit F1
![Quotas de l'application (plan F1)](captures/22-quotas.png)
![L'application utilise toujours le plan gratuit F1](captures/23-plan-f1.png)
### 6.2 Options de mise à l'échelle
**Question 11.** Le plan F1 est gratuit et tourne sur une infrastructure partagée avec d'autres clients : 1 Go de mémoire, 1 Go de stockage, 60 minutes de processeur par jour, pas de domaine personnalisé avec certificat, pas d'option « Toujours actif » et pas de mise à l'échelle. Les plans B1 et B2 (Basic) sont payants et utilisent des machines dédiées : B1 a 1 cœur et 1,75 Go de mémoire, B2 a 2 cœurs et 3,5 Go de mémoire, avec 10 Go de stockage chacun. Ils permettent aussi les domaines personnalisés avec SSL et le scale out manuel jusqu'à 3 instances.
**Question 12.** Le scale up (mise à l'échelle verticale) consiste à passer à un plan plus puissant, avec plus de processeur, de mémoire et de fonctionnalités. Le scale out (mise à l'échelle horizontale) consiste à ajouter des instances du même plan, et la charge est répartie entre elles.
**Question 13.** Le plan F1 suffit pour ce TP car on publie une simple page HTML statique avec très peu de visites. Pour un site avec beaucoup de visiteurs il est limité : les ressources sont partagées, le temps processeur est limité à 60 minutes par jour (le site est arrêté si le quota est dépassé), il n'y a pas de scale out et pas de garantie de disponibilité.
## Étape 7 : Suppression des ressources
```
az group delete --name "$TP2_RG" --yes
az group exists --name "$TP2_RG"
```
![Vérification de la suppression du groupe de ressources](captures/24-group-exists.png)
La commande renvoie false : le groupe de ressources et ses deux ressources ont bien été supprimés.
## Conclusion
Dans le TP1, pour héberger un site sur une machine virtuelle (IaaS), il fallait créer la VM, s'y connecter en SSH, installer et configurer le serveur Web et ouvrir les ports réseau. Avec Azure App Service (PaaS), Azure s'occupe du système, du serveur Web et du HTTPS : il suffit de créer l'application et de déployer une archive. Le déploiement est beaucoup plus rapide et la mise à jour se fait avec une seule commande. En revanche, on a moins de contrôle sur la machine, et le plan gratuit F1 reste limité en ressources.
