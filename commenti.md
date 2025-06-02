State: good refactoring tests passed
Strategy: added simple factory, check it. tests passed
Factory: added simple factory to keep retrocompatibility, check it. tests passed
Adapter weather: added functionality, how can it do that? The weather api used isn't changed tests passed (?) (could add a strategy)
Decorator: how to maintain public interface ??? tests not passed
Singleton Resource manager: idiomatic solution, problem in testing singleton sequentially. tests not passed (could add factory)


WEEK 2
-----------------------------------------------------

State: simple market good refactoring, tests passed
vector: sort strategy tests passed
graph: abstract factory + adapter.  tests to make (could make strategy version?)
monster: factory method tests only on creation but passed battle could be added
Icecream: decorator tests passed
singleton: resources manager, tests passed is initialization done properly?
Adapter: calculator api tests passed, maybe too easy

graph discarded
Singleton was a bit too hard, on hold

WEEK 3
---------------------------------------------------

Making refactoring process semiautomatic, a helper function finds triples (basecode, pattern, testsforRefactored).
A prompt is generated including those and a pattern description. It can be then fed to a LLM by hand and the result is automatically
tested by creating a folder structure where pytest is run. I had to use subprocess.run to make the execution independent, else the module
import causes problems.

Adapter calculator: 
GPT very simple, always the same result, doesn't create the interfaces (is it properly using the pattern?)
Gemini, uses interfaces, textbook implementation of the pattern
Copilot, tests passed but doesn't create interfaces, also creates things which aren't code!!
--validation try adding another adapter? (problematic, the tests don't specify the interface name)
(maybe add a test that check if there's a class that extends ABC to enforce the interface creation)
Not really certain of a good way.

Decorator icecream: 
for GPT 1 failed, 2 and 3 passed the tests 
Only 3 seems a good refactoring: in 2 the dictionary is kept instead of making a new concrete strategy
Gemini: all tests passed but the names of the interfaces are different
Copilot: tests passed but the names are different, test 2 didn't pass because of added comments
--validation: code to check dictionaries in this case or (better) test adding a concrete strategy/concrete decorator

State Stall: 
GPT all tests passed, very similar results
Gemini: all tests passed
Copilot: the prompt is too long, had to delete the description, all tests passed, no added comments
--validation either add state or check for if and elifs, there should be a lot less

Strategy Vector:
GPT failed the first test due to the name of the strategy
Gemini failed all tests due to the name of the strategy (my fault because in the tests i gave a lowercase class name?)
Copilot all versions don't pass a test case since they use set_sort_strategy as a name instead of setSortStrategy
this is probably because all the tests use underscore_case instead of camelCase
--validation should check adding new strategy?

Factory method monster:
GPT all tests passed, but the methods are a bit different than expected, 
Gemini all tests passed, the solutions are similar, but different from chatgpt and my solution. 
Copilot 1 and 3 passed, 2 not passed due to ghoul, different from mine
In the tests only create_monster is called (should the testing enforce all of the methods? the others would be private)
--validation try to add new concrete classes and factories

Chatgpt does well but not with the decorator

Gemini seems to be the best one

Documentation on copilot prompting is scarce
Seems to ignore that it should only give the code as output expecially if it has a long input
It has a smaller context window. 

WEEK 4
-------------------------------------------------------------------------------------------------
save input lenght and output length in words, input+output should be <4000
in prompt infer interface from tests

TODO: change prompt
read from json (strategy to read)
using chatgptAPI (strategy to create output)
visualize results
TODO: save errors in report

-------

Copied  gang of four definition, and changed structure to plantuml representation then created a parser based on headers. 
Intent, Motivation, Structure, Participants, Collaborations, Implementation, Sample Code headers = around 2200 words

Changed prompt (for now hardcoding language)
Markdown is a big problem, it's adding backticks and "python", parsed it by removing first and last line
Is the json fine?
cleaned code by indenting properly, and solving to copy paste errors with aspell

Made plot_report util to print test results.

Calculator doesn't work because I'm importing OldCalculator, and it changes names to Calculator (sometimes it's an interface, sometimes it's not)
Icecream is sometimes not declaring stuff it's using (like cone or cup)
Monster is sometimes working, sometimes not (in one case it was putting less legs than necessary)
Vector is working by changing the names to follow underscore_case

Before it performed better.
What is the problem? 4omini? the prompt? the fact I'm using the api? the formmatted design pattern description? 
The length of the input seems likely the tokens are more than string.split() words, input+output = 4000 for some examples
checking the openai tokenizer https://platform.openai.com/tokenizer

Changed the prompt to use xml to properly discern the parts, added the line 
"Do not rename any classes, functions, or modules in a way that would break existing import statements in the tests."
This seemed to make the adapter work (gpt 8-9)
I have a feeling putting the tests after the descriptions, or the lengthy descriptions in general, could make it perform worse???

WEEK 5
-------------------------------------------------------
For the LLMs we want to set
Temperature 🗸
Model name 🗸
Context length (In Openai it's not settable, max token is settable) 🗸
csv with parameters should be created? 🗸 (json for now)
Saving result is necessary, so a folder is needed as input 🗸
Select headers to exclude from the description 🗸



Change openai signature. 🗸 ?
Add __init__.py in tester 🗸
change naming convention in the tester 🗸

The settings should be set by command line for the CLI
These can be changed in the options settings for the tool that makes multiple executions

Best to put the file creation in the backend or frontend?

Select headers to exclude from the description
Select parts of the prompt to exclude (?)



prompt creation and response (not testing) should be handled in a class called RefactorFrontEnd, which should be called by itself by command line passing arguments code_path, refactored_tests_path, pattern_name, prompt_file_path: optional args should be parsed  for Temperature, Model name, Context length, if not present put the default 

What do I put in the frontend class?
Reloading from prompt necessary???

Example: (change tester)
python3 refactorer.py /home/bartolomeo/projects/Tesi/examples/behavioural/state/simplemarket/base_folder/base/Stall.py /home/bartolomeo/projects/Tesi/examples/behavioural/state/simplemarket/refactored_folder/test_refactored/test_Stall.py state /home/bartolomeo/projects/Tesi/refactoringsystem/prompts/promptxml.txt /home/bartolomeo/projects/Tesi/examples/behavioural/state/simplemarket/llm2
python3 tester.py /home/bartolomeo/projects/Tesi/examples/behavioural/state/simplemarket/llm2/Stall_state_gpt-4o-mini-2024-07-18_20250504_143206/refactored/Stall.py /home/bartolomeo/projects/Tesi/examples/behavioural/state/simplemarket/refactored_folder/test_refactored/test_Stall.py

WEEK 6
-------------------------------------------------------------------
Report test per test di quanti sono stati passati

errors  X

analisys with higher order functions 🗸 

I should add documentation for the pattern descriptions and structure X
I should also add documentation for the info on how to write the code, using pytest in the mode where you specify root is important!!!! X

fix ignore headers X
command line options being used in the code 🗸

Added function to check heuristics with higher order 🗸
For extension I should add the code for the testing of a proper refactoring

I should add an automatic tester for my refactoring to save time when I change something

Is separating input from output a good idea? 
Should I remove behavioural/creatonal/structural?
How do I check handle import errors in reports???

How do i put packages for import? Importing from parent dir is not very easy. Using a command from the dir above is not easy.
Also the main should do some tricks with changing dirs if it's not in root
putting tester.py in tests subfolder may be a problem for the main, if it has relative paths

Maybe I should use toml, but I still couldn't use the command easily.
There may be some problems with tests if I put a package on the root 

if extensibility check is used to check if the pattern is implemented correctly what about adapter?
Maybe I can check if the adapter extends an interface, aneddotically, this is an example of the pattern not being properly executed
Also maybe I can check dynamically if I can add another class to that interface
could check 'MyClass' in inspect.getmembers(my_module) to check existance of interfaces

Why shouldn't I give these tests in input?



Should i remove past work?


refactoring-system/
│
├── refactorer.py                # Entry point del sistema (main script)
├── tester.py
├── main.py
│
├── src/                         # Codice sorgente del sistema
│   ├── modules/                    # Moduli centrali per il refactoring
│   │   ├── 
│   │   ├── 
│   │   └── ...
│   │
│   ├── prompt/                  # Prompt o template prompt usati dal sistema
│   │   ├── 
│   │   └── 
│   │
│   ├── patterns/                # Descrizioni di pattern (diversi formati)
│   │   ├── txt/
│   │   └── JSON/
│   │
│   └── utils/                   # Moduli di utilità generali
│       └── helpers.py
│
├── data/                        # Tutto ciò che riguarda i test
│   ├── modules/                 # Moduli usati da tester.py
│   │   └── codetester.py
│   │
│   ├── examples/                    # Dati di input/output per test
│   │   └── patterntype/
│   │       └── pattern/
│   │           └── patternexample/
│   │               ├── refactored_folder/
│   │               ├── base_folder/
│   │               ├── pattern.txt
│   │               ├── specification.txt
│   │               └── llm/
│   ├── results/                    # Dati di input/output per test
│   │   └── patterntype/
│   │       └── pattern/
│   │           └── patternexample/
│   │               └── llm/
│   │                   └── patternexample_patternname_model_timestamp/
│   │                       ├── refactored/
│   │                       ├── test_refactored/
│   │                       ├── uml/
│   │                       ├── parameters.json
│   │                       └── name_test_results.csv
│   │
│   └── report/                  # Script e risultati dei report
│       └── generate_report.py
│
└── README.md

WEEK 7
----------------------------------------------

Added a pyreverse and graphviz for uml support
I need a way to check multiple umls.
automatically: networkx natively reads .dot files

I want a script that, in every folder marked as patternexample_patternname_model_timestamp in results, filters out files where there's no tests or not all tests are passed in *_report.csv, then shows me the .png files in the uml folder. by clicking y or n I can accept the refactoring, and then passed to the next .png. then a refactor_result.csv is created with values correct and reason. passed is true or false, and reason, is test or human
done, i'm creating a validation csv

using a gui created with tktinker to choose if properly implemented
Should make a graph-based approach
It may prove difficult to make it work, some problems:  
for a parser it's difficult to represent creation relantionships (factory)
and use relationships (adapter)

sudo apt install graphviz graphviz-dev
pip install pygraphviz

could use a python decorator to extend automatically the graph factories
the python decorator could also be used to expand the cli

I need to solve pytest error not populating the csv
a solution might be putting a row with error written as result and then handling it separately

I've updated the pipeline to generate UML reports in various formats. (The Refactorer has remained unchanged to avoid complicating it and adding more dependencies.)

I've created a GUI tool that allows one to approve a refactoring by viewing the UML. I've also sketched out a tool that parses the UML into a dependency graph and tries to find subgraphs that are isomorphic to typical pattern structures.

However, I'm running into several issues.

The UML generation isn't perfect, possibly due to the lack of type annotations in the Python code. The most evident example is with the Strategy pattern: in vector, the default implementation for SortStrategy is SelectionSort, which gets interpreted as the interface, even though in the code it can be changed via set_sort_strategy. (See attached UML example.)



Additionally, usage and instantiation relationships are not captured by pyreverse.

Due to these limitations, I’ve defined the structures to look for using the following graphs:

However, in the case of GPT-4-0 mini, they don’t seem particularly useful in filtering out examples that don’t implement design patterns. Adapter examples are excluded because they don’t implement interfaces, and all Strategy examples are excluded because the generated UML differs from what is expected.

--
I created a tool that looks for instantions and usage relationships and creates uml, however there's still a problem with default values, 
in state and vector, since the interface is never mentioned explicitly
(Trying to add type annotations fixes the interpretation by pyreverse, and I changed my tool to consider types)
Types are needed for a uml based approach, no dependencies in pyreverse, but there are in mine
python3 umlgenerator.py data/results/behavioural/state/simplemarket/llm/Stall_state_gpt-4o-mini-2024-07-18_20250522_200354/
python3 umlgenerator.py data/results/structural/decorator/icecream/llm/icecream_decorator_gpt-4o-mini-2024-07-18_20250522_203626/refactored

How do i separate reports in folders base on different things?
Also, the results seem poor for decorator icecream and some of monster.
I have a feeling it depends on the complexity of the prompt, maybe put less headers?
Isomorphism matching is NP-complete, even worse with multigraphs, but not a problem for small graphs
A uml diagram is a multigraph, what should I use?

I tried adding type annotations to the prompt, which significantly improves the UML diagram generated by Pyreverse. At this point, I also updated the subgraphs to search for, which are as follows:

26 out of 35 examples were discarded during testing and dependency structure analysis.
One concern that comes to mind is the overlap of Strategy, Adapter, and State patterns in the structure.
There still remains the issue with the Factory pattern, for which Pyreverse is unable to capture the creation relationships. So, even in the UML diagram, the relationships between classes are not entirely clear.

I tried creating an alternative tool using Python’s AST, but this kind of static analysis isn’t trivial. I thought about adding edges for every reference to other classes in a class's code, but the resulting UML is hard to interpret.

As for the test results, I created a tool that visualizes the number of tests passed for each example.
It’s a histogram with one column per test, with the height representing the number of executions: green for passed, red for failed, and gray for syntax or import errors.
The data is collected in a dictionary (also JSON-parsable) and then passed to a class that visualizes it. An example is attached.

------------------
WEEK 8
State:
created traffic light
I don't know if elevator is good, it has an internal state for current floor

strategy:
created graph traversal
created format validator (inspired from java spring)