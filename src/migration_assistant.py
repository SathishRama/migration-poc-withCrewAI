import os
from crewai import Agent, Task, Crew, Process
from langchain.chat_models import ChatOpenAI
from crewai_tools import BaseTool
import ast, json
#ignore LangChainDeprecationWarning
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

class ProcessInputTextTool(BaseTool):
    name: str = "Input text tool"
    description: str = "Takes a user input text and pass to Agent."

    def _run(self, argument: str) -> str:
        # Your tool's logic here
        print("User text : ",argument)
        return argument

#os.environ["OPENAI_API_KEY"] = "your key"

# It can be a local model through Ollama / LM Studio or a remote
# model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)

# Define your agents with roles and goals
cpp_code_explainer = Agent(
  role='C++ Code Explainer',
  goal='Explain the following C++ code in detail {input}',
  backstory="""You are expert in explaning C++ code in detail. Highlight the inputs, outputs, logic, and error handling in the code.""",
  verbose=False,
  allow_delegation=False,
  # You can pass an optional llm attribute specifying what model you wanna use.
  llm=ChatOpenAI(model_name="gpt-4o")
)

# Create tasks for your agents
task1 = Task(
  description="""Analyse the {input} provided C++ code to explain the purpose and functionality. List critical inputs, outputs, logic, and error handling""",
  expected_output="A summary of the provided C++ code with following sections : 1) Overview 2) Inputs 3)Outputs 4)logic 5) Error handling""",
  agent=cpp_code_explainer,
  human_input=False
)

# Instantiate your crew with a sequential process
code_explain_crew = Crew(
  agents=[cpp_code_explainer],
  tasks=[task1],
  verbose=False,
  process = Process.sequential
)

#create a agent, tasks and its crew to migrate C++ code to Java
java_code_migrator = Agent(
  role='Java Code Migrator',
  goal='''Migrate the following C++ code to Java code with good comments and provide explaination on the migrated java code. C++ Code:\n{input}''',
  backstory="""You are expert in migrating C++ code to Java. Make sure the code is well-structured, efficient, and error-free. 
  Add detailed comments in the java code to explain the logic and functionality. Ensure the code follows Java best practices.
  And provide a detailed explaination of the migrated Java code including the import statements etc.""",
  verbose=False,
  allow_delegation=False,
  # You can pass an optional llm attribute specifying what model you wanna use.
  llm=ChatOpenAI(model_name="gpt-4o")
)

# Create tasks for your agents
task2 = Task(
  description="""Migrate the {input} provided C++ code to Java""",
  expected_output="A json dictionary with two values : 1) Java Code 2) Explaination""",
  agent=java_code_migrator,
  human_input=False
)

# Instantiate your crew with a sequential process
java_code_migration_crew = Crew(
  agents=[java_code_migrator],
  tasks=[task2],
  verbose=False,
  process = Process.sequential
)


def analyze_cpp_files(input_file_name):
    if input_file_name.endswith(".cpp") or input_file_name.endswith(".h"):
        with open(input_file_name, "r") as file:
            code_snippet = file.read()
            print(f"    Analyzing {input_file_name}...")
            code_explaination = code_explain_crew.kickoff(inputs={"input": code_snippet})
            print(f"    Completed Analyzing {input_file_name}")
    return code_explaination

#func to migrate C++ code to Java
def cpp_to_java(output_file_name, input_file_name):
    response = {
        "success": False,
        "message": "Not yet migrated"
    }
    if input_file_name.endswith(".cpp") or input_file_name.endswith(".h"):
        with open(input_file_name, "r") as file:
            code_snippet = file.read()
            print(f"    Migrating {input_file_name}...")
            migration_agent_response = java_code_migration_crew.kickoff(inputs={"input": code_snippet})
            print(f"    Completed migrating {input_file_name}")
            #print(f"Response: {migration_agent_response.raw}")

            # Attempt to parse the response as JSON
            try:
                # Remove any code block markers and parse the JSON
                response_content = migration_agent_response.raw.strip().strip("```json").strip("```")
                output_json = json.loads(response_content)
                #print("Parsed JSON:", output_json)

                # Extract Java code and explanation from the output_json
                output_json_list = list(output_json.values())
                java_code = output_json_list[0]
                code_explaination = output_json_list[1]
                response["success"] = True
                response["message"] = "Code successfully migrated"

            except Exception as e:
                print("     Exception Occurred in migrating code :", e)
                response["success"] = False
                response["message"] = f"Error occurred while migrating code: {str(e)}"
                java_code = ""
                code_explaination = ""

            # print(f"Java code: {java_code}")
            # print(f"Explained code: {code_explaination}")

            try:
            # Save the Java code to the output file
                with open(output_file_name, "w") as file:
                    file.write(java_code)
                print(f"    Java code saved to {output_file_name}")
                # save the explanation to a separate file
                explaination_file_name = f'''{output_file_name.split('.')[0]}_explaination.txt'''
                with open(explaination_file_name, "w") as file:
                    file.write(code_explaination)
                print(f"    Explained code saved to {explaination_file_name}")
            except Exception as e:
                print("     Exception occurred while saving java files :", e)
                response["success"] = False
                response["message"] = f"Error occurred while saving java files: {str(e)}"

    return response

def run_directory_migration():
    #Take the User Inputs for C++ Project Directory and Output Java Project Directory
    files_migration_status = []
    num_cpp_readme_docs = 0
    print("Enter the path to the C++ project directory:  ")
    cpp_project_dir = input()
    print("Enter the path to the output Java project directory:  ")
    java_project_dir = input()

    # Check if the provided directories exist
    if not os.path.exists(cpp_project_dir) or not os.path.exists(java_project_dir):
       print("Provided directory does not exist.")
       exit(1)

    # Iterate over each C++ file in the project directory
    cpp_files = [f for f in os.listdir(cpp_project_dir) if f.endswith(".cpp") or f.endswith(".h")]
    print(f"Found {len(cpp_files)}  C++ files: ")
    print("## Starting migration...")
    for cpp_file in cpp_files:
        print(f"    Processing {cpp_file}...")
        cpp_file_path = os.path.join(cpp_project_dir, cpp_file)
        cpp_file_type = cpp_file.split('.')[-1]
        if cpp_file_type == "cpp":
            output_java_file_name = cpp_file.split('.')[0] + ".java"
        elif cpp_file_type == "h":
            output_java_file_name = cpp_file.split('.')[0] + "_functions.java"
        else:
            print(f"    Unsupported file type for {cpp_file}. Skipping...")

        output_java_file_path = os.path.join(java_project_dir, output_java_file_name)
        code_explaination = analyze_cpp_files(cpp_file_path)
        #print(f"CPP Explained code: {code_explaination}")
        #create a readthedocs directory in java project directory if not exists
        readthedocs_dir = os.path.join(java_project_dir, "cpp_readthedocs")
        if not os.path.exists(readthedocs_dir):
            os.makedirs(readthedocs_dir)

        # Save the Markdown file with the explained code for each C++ file in the readthedocs directory
        md_file_path = os.path.join(readthedocs_dir, cpp_file.split('.')[0] + ".md")
        try:
           with open(md_file_path, "w") as md_file:
               md_file.write(code_explaination.raw)
               num_cpp_readme_docs = num_cpp_readme_docs + 1
        except Exception as e:
           print(f"     Exception occurred while saving Markdown file for {cpp_file}:", e)

        response = cpp_to_java(output_java_file_path, cpp_file_path)
        files_migration_status.append((cpp_file, response['message']))
        #display number of files processsed and % of completion
        print(f"    ==> {len(files_migration_status)} out of {len(cpp_files)} files processed.")


    print("\n###  Migration Status ####")
    for cpp_file, status in files_migration_status:
        print(f"    {cpp_file}: {status}")
    print(f"    Total number of C++ README files created: {num_cpp_readme_docs}")

    print("\n### Migration process completed. Review the generated Java files and Markdown files for any errors.")
    return

if __name__ == "__main__":
    #This program can be used to migrate a C++ application to a Java application
    print("     ### This is DEMO of C++ to Java Migration using GenAI ")
    run_directory_migration()

