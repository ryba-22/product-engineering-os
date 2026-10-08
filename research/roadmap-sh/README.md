# Szkic: 171 kroków atomowych a wiedza z roadmap.sh

**Status:** SCOPED DRAFT (2026-10-08). Własny model docelowy z polskiego dokumentu użytkownika, a nie zatwierdzony kontrakt PEOS.

- [Macierz JSON](atom-crosswalk-draft.json) obejmuje dokładnie 171 atomów z 25 etapów, ich czynności, rezultaty i pytania kontrolne.
- 25 list kandydackich roadmap pochodzi z istniejącego [atlasu 95 ocen](https://github.com/ryba-22/roadmap-sh-personal-atlas/blob/main/catalog/oceny-95.json).
- Weryfikacja dopasowania pojedynczych roadmap do atomów wynosi **0/171**. Każda relacja jest na razie UNVERIFIED.
- Nie zastępuje [kanonicznego cyklu PEOS](../../00-core/lifecycle.md), nie zmienia gate G0–G11, routera ani reguł produkcji.

## Dalszy proces
1. Porównać konkretny temat źródłowy z działaniem i rezultatem atomu — nie wyłącznie podobieństwo słów.
2. Wskazać repo, SHA, plik i twierdzenie, a także lokalny test lub kontrolę oraz właściciela.
3. Oznaczyć obecne pokrycie, duplikat, brak dopasowania i prawdziwą lukę, zachowując UNKNOWN przy braku dowodu.
4. Przetestować kontrprzykład; review Jakuba i niezależna kontrola Kasi.
5. Dopiero wtedy promować wiarygodne ustalenia do właściwego repozytorium.

## Walidacja strukturalna
Uruchomić: `python scripts/validate_roadmap_atom_crosswalk.py`.

Test struktury nie dowodzi poprawności semantycznej ani skuteczności wykonania. [RMAP-02 #17](https://github.com/ryba-22/product-engineering-os/issues/17).
