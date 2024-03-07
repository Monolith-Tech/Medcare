# Differential diagnosis generation

"""
Differential diagnosis is defined as the process of differentiating between probability of one disease-
versus that of other diseases with similar symptoms that could possibly account for illness in a patient.
"""

# Import the necessary utility function
from utils.tools import (
    get_openai_response,
    Models
)

# Example prompt function for differential diagnosis; this needs to be defined in utils/prompts.py or wherever relevant
from utils.prompts import DD_prompt


def generate_DD(patient_symptoms: str, patient_history: str, physical_examination: str, test_results: str, verbose=True, save_to_file=None) -> str:
    """
    Generate a differential diagnosis based on the patient's symptoms, history, physical examination findings, and test results.
    """

    print("* Generating Differential Diagnosis...")
    DD = get_openai_response(
        prompt=DD_prompt(patient_symptoms=patient_symptoms, patient_history=patient_history,
                         physical_examination=physical_examination, test_results=test_results),
        model=Models.model_4_turbo
    )

    if verbose:
        print('* Differential Diagnosis:\n\n' + DD)

    if save_to_file:
        with open(save_to_file, 'w') as file:
            file.write(DD)

    return DD


# main
if __name__ == "__main__":
    # Example inputs; in a real scenario, these would be gathered from a patient's records or consultation
    patient_symptoms = "Example symptoms text here"
    patient_history = "Example patient history here"
    physical_examination = "Example physical examination findings here"
    test_results = "Example test results here"
    output_filename = "DD_output.txt"

    # Generate the differential diagnosis
    generate_DD(
        patient_symptoms=patient_symptoms,
        patient_history=patient_history,
        physical_examination=physical_examination,
        test_results=test_results,
        verbose=True,
        save_to_file=output_filename
    )
