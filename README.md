# Solar_Mining

Développements autour d'un Mineur Antminer S9 permettant la consommation de surplus solaire.
<div align="center"><img width="961" height="536" alt="Solar" src="https://github.com/user-attachments/assets/ffc4bb2c-d2b4-4375-bb6a-2bf08bf79592" /></div>

## Mes motivations

J'ai souhaité développer un système permettant de consommer le surplus de production solaire au travers d'un mineur S9, qui fonctionne de paire avec 
le projet [Module TIC](https://github.com/bastoon577-lang/Module_TIC/wiki), et permet la lecture des données issues du compteur Linky au travers du réseau LAN 
en utilisant le réseau Wifi, et permet une observation des données de consommation Linky au Mineur S9.

Un avantage certain quand la génération de cryptomonaie devient alors **gratuite par une électricité gratuite**.

## Concept

A iso-périmètre d'un switch solaire capable d'alimenter ou non un cumulus [(Projet SmartHeater)](https://github.com/bastoon577-lang/SmartHeater/wiki#r%C3%A9solution-dune-probl%C3%A9matique-technique),
ce concept utilise un Mineur S9 en écoute permanante sur le [Module TIC](https://github.com/bastoon577-lang/Module_TIC/wiki) afin de permettre sa mise en marche lorsque l'énergie solaire 
est disponible, et sa mise à l'arrêt autrement par une [stratégie de pilotage identique à celle du projet SmartHeater](https://github.com/bastoon577-lang/SmartHeater/wiki/Strat%C3%A9gie-de-pilotage#extrapolation-des-donn%C3%A9es).

## Matériel nécessaire

Le matériel se résume à la liste suivante : 
 * Un mineur S9,
 * Une carte MicroSD (pour l'installation)

> ⚠️ La **carte MicroSD** est essentiel à l'installation de BraiinOS mais non essentiel lors du fonctionnement du Mineur. 
> Il est possible de flasher la mémoire NAND à partir de la carte MicroSD après installation.

## Transformer le Mineur
> ⚠️ **ATTENTION** au boot du S9 sur carte SD.
>
> Il est nécessaire de persuader le mineur de booter sur la carte SD en suivant cette [procédure](https://academy.braiins.com/en/braiins-os/installation/install/#install-braiins-os-on-s9-s9i-s9j) tout en prenant soin d'intégrer une image spéciphique de ce repo.

J'expose 2 voies pour permettre l'intégration du mécanisme dans le Mineur Antminer S9.
 1. [Utilisation de l'image pre-compilée](#reuse) (Mode débutant)
 2. [Re-construction d'une image custom](#diy) (Mode expert)

<div id='reuse'/> 

### Utilisation de l'image pre-compilée

Je met à disposition une [image pre-compilée](https://github.com/bastoon577-lang/Solar_Mining) que vous pouvez immédiatement charger avec Rufus en suivant 
ce [tuto de flashage](https://rufus.ie/fr/). Cette image embarque tout le nécessaire à l'exploitation du mineur sur le réseau.

Puis effectuer le paramétrage sur le Mineur en suivant cette [procédure](#parameters).

### Re-construction d'une image custom

La re-construction consiste à générer l'image custom pas à pas à partir d'une image 
officielle en vue de créer l'image par vous même en suivant [cette procédure](https://github.com/bastoon577-lang/Solar_Mining/wiki/Re%E2%80%90construction-d'une-image-custom), puis d'effectuer la configuration du thermostat sur le Mineur en suivant cette [procédure](#parameters).

<div id='parameters'/>
 
## Paramétrer le Module TIC sur le Mineur

Il ne reste qu'à positionner la configuration du Module TIC `IP` et `Port`au travers de l'interface WEB du Mineur en suivant ce [tuto de configuration](https://github.com/bastoon577-lang/Solar_Mining/wiki/Interractions-avec-le-script-de-monitoring).

## Paramétrer le Mineur (stratum)

La construction du mineur étant terminée, il est maintenant nécessaire de le configurer comme vous le feriez sans l'intégration du concept de Solar_Mining :
 * Pools (Configuration -> Pools),
 * Performances (facultatif),
 * Température & Fans (facultatif).

Un test de minage est alors possible par l'onglet **Quick Actions** :
 * START BOSminer
 * STOP BOSminer
 * ...

#### Auteur : *Sébastien DALIGAULT*. 
