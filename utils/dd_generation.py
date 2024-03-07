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


def generate_DD(SOAP: str, test_results: str, verbose=True, save_to_file=None) -> str:
    """
    Generate a differential diagnosis based on the patient's:
        - SOAP
        - test results (summarized)
    """

    print("* Generating Differential Diagnosis...")
    DD = get_openai_response(
        prompt=DD_prompt(
            SOAP = SOAP,
            test_results = test_results
        ),
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
    SOAP_filename = "Demo/demo_soap.txt"
    with open(SOAP_filename, 'r') as file:
        SOAP = file.read().strip()
    test_results = """
    DEMO TEST RESULTS SUMMARIZED HERE
    """
    output_filename = "DD_output.txt"

    # Generate the differential diagnosis
    generate_DD(
        SOAP = SOAP,
        test_results = test_results,
        verbose = True,
        save_to_file = output_filename
    )
