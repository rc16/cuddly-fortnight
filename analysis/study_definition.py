# cohort extractor
from cohortextractor import StudyDefinition, codelist_from_csv, patients

# Import codelists
medication_review_codelist = codelist_from_csv(
    "codelists/opensafely-care-planning-medication-review-simple-reference-set-nhs-digital.csv",
    system="snomed",
    column="code",)

alt_codelist = codelist_from_csv(
    "codelists/opensafely-alanine-aminotransferase-alt-tests.csv",
    system="snomed",
    column="code",)

# set the index date
index_date = "2018-03-01"
# set study end date - not sure if this should be 1st February 2020
# as per exclusions
end_date = "2022-01-31"

# STUDY POPULATION

study = StudyDefinition(
    default_expectations={
        "date": {
            "earliest": index_date,
            "latest": end_date,
        },  # date range for simulated dates
        "rate": "uniform",
        "incidence": 1,
    },

    population=patients.satisfying(
        """
        registered AND
        (NOT died) AND
        (age >=18 AND age <=120) AND
        (sex = 'M' OR sex = 'F')
        """,
        # need 3 months registration prior to index - add it here?
        registered=patients.registered_as_of(index_date),

        died=patients.died_from_any_cause(
            on_or_before=index_date,
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
            ),

        age=patients.age_as_of(
            index_date,
            return_expectations={
                "rate": "universal",
                "int": {"distribution": "population_ages"},
            },
        ),

        sex=patients.sex(
            return_expectations={
                "rate": "universal",
                "category": {"ratios": {"M": 0.49, "F": 0.5, "U": 0.01}},
            }
        ),
    ),  
    # defining stp - this should not be missing
    stp=patients.registered_practice_as_of(
        index_date,
        returning="stp_code",
        return_expectations={
            "category": {"ratios": {"STP1": 0.3, "STP2": 0.2, "STP3": 0.5}},
        },
    ),
    # defining IMD - this should not be missing
    imd=patients.categorised_as(
        {
            "0": "DEFAULT",
            "1": """index_of_multiple_deprivation >=1
            AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5
            AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5
            AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5
            AND index_of_multiple_deprivation < 32844*4/5""",
            "5": """index_of_multiple_deprivation >= 32844*4/5
            AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            index_date,
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.05,
                    "1": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5": 0.19,
                }
            },
        },
    ),

)