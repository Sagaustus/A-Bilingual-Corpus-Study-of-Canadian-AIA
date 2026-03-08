[![Build Status](https://travis-ci.com/canada-ca/aia-eia-js.svg?branch=master)](https://travis-ci.com/canada-ca/aia-eia-js/)

([Français](#gabarit-pour-dépôts-de-code-source-ouvert-du-gouvernement-du-canada))

# Algorithmic Impact Assessment

This project hosts a prototype of the Algorithmic Impact Assessment (AIA) developed in Typescript.

The AIA is a critical piece of the [Directive on Automated Decision-Making](http://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=32592) and we want to ensure its development is done in the open.

The users of this project will be Government of Canada employees assessing the impact of using an automated decision system, including Artificial Intelligence, as part of their programs and services.

As this assessment tool is open source, other countries and individuals may wish to also leverage it and even contribute back to it.

It leverages the [SurveyJS library](https://surveyjs.io/Overview/Library/) to generate questions and answers. The primary source of the content, the file to edit if you want to change the questions and answers, is the `survey-enfr.json`, located in the `/src` folder.

Editing a JSON file directly may not be easy so you can use the web based [SurveyJS Builder](https://surveyjs.io/create-survey/) app to help you out.
However, please note that the way we are using the library is a little different than it was initially designed for so the native layout of the Builder may not be entirely intuitive.

For example, we have introduced weights in answers so that we can measure the score.
As such, answers have a very standard way of being created:

```json
"choices": [
                {
                    "value": "item1-3",
                    "text": {
                        "default": "Yes",
                        "fr": "Oui"
                    }
                },
                {
                    "value": "item2-0",
                    "text": {
                        "default": "No",
                        "fr": "Non"
                    }
                }
            ]
```

The above example shows how answers are listed; the value names are defined as `item<#>-<weight>` where the `<#>` is an incremental answer number and the `<weight>` is the weight given to that answer for the score.

That is because the overall tool we have built is an Impact Assessment tool, not a simple survey.
As such, some answers have weights that are used in a specific way in order to provide an impact assessment combining raw impact score and mitigation score.

The text of the answer, what will be displayed to the users, can then be defined in English and French by assigning the English value to `default` and the French value to `fr`.

To render the web application, we also make use of the Vue.js framework.
You can see all the components built in `/src/components` and all the views in `/src/views`.

Finally, if you would like to render the web application without the Government of Canada template and branding, you can remove the line 32 of the index.html file which sits in the /public folder.

Line to remove:

```html
<script type="text/javascript" src="helper/wet.js"></script>
```

Please note that we will not be removing the branding ourselves at this point but this may become more configurable as we break down the project in various components.

## Local PostgreSQL Database

The corpus is stored in a local PostgreSQL database named **`aia_corpus`** with 27 tables covering 1,178 rows of structured AIA data.

### Quick start

```bash
# Create and populate the database
psql -d postgres -c "CREATE DATABASE aia_corpus;"
psql -d aia_corpus -f etl/schema.sql

# Load all data (lookups → datasets → junctions → forms → sections)
for t in organizations subjects keywords resource_types languages formats; do
  psql -d aia_corpus -c "\COPY $t FROM 'etl/output/$t.csv' CSV HEADER"
done
psql -d aia_corpus -c "\COPY datasets FROM 'etl/output/datasets.csv' CSV HEADER"
psql -d aia_corpus -c "\COPY resources FROM 'etl/output/resources.csv' CSV HEADER"
for t in dataset_subjects dataset_keywords dataset_resource_types dataset_languages dataset_formats; do
  psql -d aia_corpus -c "\COPY $t FROM 'etl/output/$t.csv' CSV HEADER"
done
psql -d aia_corpus -c "\COPY questions FROM 'etl/output/questions.csv' CSV HEADER"
psql -d aia_corpus -c "\COPY form_submissions FROM 'etl/output/form_submissions.csv' CSV HEADER"
for t in project_details reasons_for_automation risk_profile project_authority \
         about_the_algorithm about_the_decision individual_impacts about_the_data \
         consultation data_quality_bias fairness privacy_security; do
  psql -d aia_corpus -c "\COPY $t FROM 'etl/output/section/$t.csv' CSV HEADER"
done
```

### Connect

```bash
psql -d aia_corpus
```

### Schema overview

- **6 lookup tables** — organizations (10), subjects (9), keywords (121), resource_types (6), languages (3), formats (5)
- **1 core table** — datasets (32 AIA datasets from open.canada.ca)
- **5 junction tables** — many-to-many links for subjects, keywords, resource types, languages, formats
- **1 resources table** — 137 downloadable file URLs
- **2 form tables** — questions (103 AIA form questions), form_submissions (114 source files)
- **12 section tables** — 30 rows each, one per JSON submission, covering project details, risk profile, fairness, privacy, and more
- **1 view** — `v_datasets_flat` denormalized view of the dataset layer

See [CORPUS_PIPELINE.md](CORPUS_PIPELINE.md) for full pipeline documentation and example research queries.

## Getting Started

See the [Wiki](../../wiki)

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

Unless otherwise noted, the source code of this project is covered under Crown Copyright, Government of Canada, and is distributed under the [MIT License](LICENSE).

The Canada wordmark and related graphics associated with this distribution are protected under trademark law and copyright law. No permission is granted to use them outside the parameters of the Government of Canada's corporate identity program. For more information, see [Federal identity requirements](https://www.canada.ca/en/treasury-board-secretariat/topics/government-communications/federal-identity-requirements.html).

______________________

# Évaluation de l'incidence algorithmique

Ce projet accueillera un prototype de la prochaine itération de l'étude d'impact algorithmique (EIA) développé en JavaScript.

Il se composera de deux capacités principales :

* Offrir une interface simple permettant à l'équipe administrative de mettre à jour les questions, les réponses et le mécanisme de notation du questionnaire.
* Proposer un questionnaire en ligne aux utilisateurs finaux pour évaluer leur système automatisé de prise de décision.

L'EIA est un élément essentiel de la [Directive sur la prise de décisions automatisée](http://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=32592) et nous voulons nous assurer que son élaboration se fasse au grand jour.

Les utilisateurs de ce projet seront des employés du gouvernement du Canada qui évalueront l'incidence de l'utilisation d'un système automatisé de décision, y compris l'intelligence artificielle, dans le cadre de leurs programmes et services.

Comme cet outil d'évaluation est publié sous une licence libre, d'autres pays et individus peuvent souhaiter l'utiliser également et même y contribuer.

## Comment utiliser

Voir le [wiki](../../wiki)

## Comment contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md)

## Licence

Sauf indication contraire, le code source de ce projet est protégé par le droit d'auteur de la Couronne du gouvernement du Canada et distribué sous la [licence MIT](LICENSE).

Le mot-symbole « Canada » et les éléments graphiques connexes liés à cette distribution sont protégés en vertu des lois portant sur les marques de commerce et le droit d'auteur. Aucune autorisation n'est accordée pour leur utilisation à l'extérieur des paramètres du programme de coordination de l'image de marque du gouvernement du Canada. Pour obtenir davantage de renseignements à ce sujet, veuillez consulter les [Exigences pour l'image de marque](https://www.canada.ca/fr/secretariat-conseil-tresor/sujets/communications-gouvernementales/exigences-image-marque.html).
