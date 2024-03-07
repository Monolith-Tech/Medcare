# SOAP generation

from utils.tools import (
    get_openai_response,
    Models
)

from utils.prompts import SOAP_prompt


def generate_SOAP(conversation: str, verbose=True, save_to_file=None) -> str:
    """
    Generate structured SOAP note.
    """
    
    print("* Generating SOAP...")
    SOAP = get_openai_response(
        prompt = SOAP_prompt(conversation_input=conversation),
        model = Models.model_4_turbo
    )
    
    if verbose:
        print('* SOAP:\n\n' + SOAP)

    if save_to_file:
        with open(save_to_file, 'w') as file:
            file.write(SOAP)
    
    return SOAP


# main
if __name__ == "__main__":
    conversation_filename = "Demo/demo_session.txt"
    output_filename = "SOAP.test"
    
    with open(conversation_filename, 'r') as file:
        conversation = file.read().strip()
    
    generate_SOAP(
        conversation = conversation,
        verbose = True,
        save_to_file = output_filename
    )
    
