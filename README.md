# Météo migraine (Paris)

Un calendrier auquel on s'abonne une fois sur son téléphone : il affiche automatiquement,
sur les 7 prochains jours, les journées où la pression atmosphérique prévue à Paris
(Porte d'Aubervilliers) correspond au profil migraineux — et rien les autres jours.

- 🟠 **Météo défavorable** : baisse modérée de pression prévue (−3 à −1 hPa par rapport
  à la veille). Historiquement ~13 % de risque de crise au lieu de 10 %. Un facteur
  aggravant, **pas une alarme**.
- 🟢 **Météo favorable** : remontée franche (≥ +6 hPa). Historiquement ~6 % de risque.

Règle calibrée sur un journal de 356 jours de migraine (2017–2026) croisé avec la
réanalyse météo ERA5, et stable sur les deux moitiés de la période (risque relatif
×1,26 sur 2017–2022, ×1,27 sur 2023–2026). Les signaux les plus forts restent
non-météo : lendemain d'un jour de crise ≈ 40 % de risque ; jours 3 à 5 après une
crise ≈ 4 %.

Le fichier `meteo-migraine.ics` est régénéré automatiquement deux fois par jour
(GitHub Actions) à partir des prévisions [Open-Meteo](https://open-meteo.com/).
**Aucune donnée personnelle** : uniquement de la météo publique.

## S'abonner (une seule fois)

URL du calendrier :

```
https://raw.githubusercontent.com/reydelmambo/meteo-migraine-paris/main/meteo-migraine.ics
```

**iPhone** : Réglages → Apps → Calendrier → Comptes → Ajouter un compte → Autre →
« Ajouter un cal. avec abonnement » → coller l'URL ci-dessus.

**Android / Google Agenda** : sur un ordinateur, ouvrir [calendar.google.com](https://calendar.google.com) →
à gauche, « Autres agendas » → **+** → « À partir de l'URL » → coller l'URL.
Le calendrier apparaît ensuite sur le téléphone (Google actualise l'abonnement environ une fois par jour).

## Arrêter

Supprimer l'abonnement dans le téléphone (mêmes menus), ou supprimer ce dépôt.
