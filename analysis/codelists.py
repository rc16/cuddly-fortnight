from cohortextractor import codelist_from_csv

# Import codelists
medication_review_codelist = codelist_from_csv(
    "codelists/opensafely-care-planning-medication-review-simple-reference-set"
    "-nhs-digital.csv",
    system="snomed",
    column="code",)

alt_codelist = codelist_from_csv(
    "codelists/opensafely-alanine-aminotransferase-alt-tests.csv",
    system="snomed",
    column="code",)
ethnicity_codelist = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
       
)