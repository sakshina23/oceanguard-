import os
from dotenv import load_dotenv
from local_llm import LocalLLM
from gemini_llm import GeminiLLM
from deepseek_llm import DeepSeekLLM

# Load environment variables
load_dotenv()

def test_llm_analysis(llm_type):
    """
    Test LLM analysis with the specified LLM type.
    Args:
        llm_type: 'local', 'gemini', or 'deepseek'
    """
    try:
        # Initialize the selected LLM
        if llm_type == 'local':
            llm = LocalLLM()
            print(f"\nTesting {llm_type.upper()} LLM...")
        elif llm_type == 'gemini':
            llm = GeminiLLM()
            print(f"\nTesting {llm_type.upper()} LLM...")
        elif llm_type == 'deepseek':
            llm = DeepSeekLLM()
            print(f"\nTesting {llm_type.upper()} LLM...")
        else:
            print(f"Unknown LLM type: {llm_type}")
            return False
        
        # Test location and result
        test_location = "Beach near Marine Drive, Mumbai"
        test_result = "Plastic Present"
        
        # Get analysis from LLM
        analysis = llm.analyze_plastic_pollution(test_location, test_result)
        
        # Print the response
        print(f"\n=== {llm_type.upper()} LLM Analysis Test Results ===")
        print("\nTest Location:", test_location)
        print("Test Result:", test_result)
        print("\nLLM Response:")
        print(analysis)
        print(f"\n=== {llm_type.upper()} Test Completed Successfully ===")
        
        return True
        
    except Exception as e:
        print(f"\n=== {llm_type.upper()} Test Failed ===")
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    # Get the LLM type from environment variable or default to all
    llm_type = os.getenv('LLM_TYPE', 'all')
    
    if llm_type == 'all':
        # Test all LLM types
        test_llm_analysis('local')
        test_llm_analysis('gemini')
        test_llm_analysis('deepseek')
    else:
        # Test the specified LLM type
        test_llm_analysis(llm_type) 