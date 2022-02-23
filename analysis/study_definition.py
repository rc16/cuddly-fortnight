# cohort extractor
from cohortextractor import StudyDefinition, patients

from codelists import *

# set the index date
study_start = "2018-03-01"
# set study end date - not sure if this should be 1st February 2020
# as per exclusions
study_end = "2022-01-31"

# STUDY POPULATION

study = StudyDefinition(
    default_expectations={
        "date": {
            "earliest": study_start,
            "latest": study_end,
        },  # date range for simulated dates
        "rate": "uniform",
        "incidence": 1,
    },

    population=patients.satisfying(
        """
        registered AND
        (NOT died) AND
        (age >=18 AND age <=120) AND
        (sex = 'M' OR sex = 'F') AND
        (stp != 'missing') AND
        (imd != 'missing') AND
        (household <=15)
        """,
        # registered as of 3 months prior to stusy start
        # need ethnicity, age, sex, STP varables to not be missing - add here
        registered=patients.registered_as_of("2018-01-01"),

        died=patients.died_from_any_cause(
            on_or_before=study_start,
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
            ),

        age=patients.age_as_of(
            study_start,
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
        "2018-01-01",
        returning="stp_code",
        return_expectations={
            "category": {"ratios": {"STP1": 0.3, "STP2": 0.2, "STP3": 0.5}},
        },
    ),
    # defining IMD - this should not be missing
    imd=patients.address_as_of(
            study_start,
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
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
    household=patients.household_as_of(
        study_start,
        returning="household_size",
    ),
    # returns date of inpatient admission
    hospital_admission=patients.admitted_to_hospital(
        returning="date_admitted",
        between=(study_start, study_end),
        date_format="YYYY-MM",
    ),
    # ethnicity
    ethnic_group=patients.with_these_clinical_events(
        ethnicity,
        returning="category",
        include_date_of_match="TRUE"
    ),  
),