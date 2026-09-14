from typing import Literal

from pydantic import BaseModel

FACTEURS_ACTIVITE = {
    "sedentaire": 1.2,
    "leger": 1.375,
    "modere": 1.55,
    "actif": 1.725,
    "tres_actif": 1.9,
}

DELTA_OBJECTIF = {
    "perte": -500,
    "maintien": 0,
    "prise": 300,
}


class UserProfile(BaseModel):
    poids: float
    taille: float
    age: int
    sexe: Literal["homme", "femme"]
    niveau_activite: Literal["sedentaire", "leger", "modere", "actif", "tres_actif"]
    objectif: Literal["perte", "maintien", "prise"]


def calculer_bmr(profil: UserProfile) -> float:
    if profil.sexe == "homme":
        return 10 * profil.poids + 6.25 * profil.taille - 5 * profil.age + 5
    return 10 * profil.poids + 6.25 * profil.taille - 5 * profil.age - 161


def calculer_tdee(bmr: float, niveau_activite: str) -> float:
    return bmr * FACTEURS_ACTIVITE[niveau_activite]


def calculer_macros(calories_cible: float) -> dict:
    calories_proteines = calories_cible * 0.30
    calories_glucides = calories_cible * 0.45
    calories_lipides = calories_cible * 0.25

    return {
        "proteines_g": round(calories_proteines / 4, 1),
        "glucides_g": round(calories_glucides / 4, 1),
        "lipides_g": round(calories_lipides / 9, 1),
    }


def calculer_profil_complet(profil: UserProfile) -> dict:
    bmr = calculer_bmr(profil)
    tdee = calculer_tdee(bmr, profil.niveau_activite)
    calories_cible = tdee + DELTA_OBJECTIF[profil.objectif]
    macros = calculer_macros(calories_cible)

    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "calories_cible": round(calories_cible, 1),
        "macros": macros,
    }
