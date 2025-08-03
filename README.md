Boxy
A programming language made in Python, hypothetically capable of reconstructing its own code at runtime.

How does it work?
($ is used for comments!)
Boxy uses @ to assign blocks and # to reference or use existing ones.

Assigning Blocks
Example:
@"New Class":$Body$.

This creates a new Entity, assigning it a unique internal ID. Entities can later be accessed by their names.

You can assign multiple names to the same entity like this:
@"New Class"@"Another Class":$Body$.

Accessing or Using Blocks
Example:
#"New Class"/valid.

This line returns a boolean value indicating whether the given name points to an existing Entity.

Multiple names can also be checked at once:
#"New Class"#"Another Class"/valid.

Syntax
Every command must end with a dot (.).
This applies to:

variable creation

function declaration

function calls

reassignment

return statements

Parameters are defined using * and wrapped in $...$.

Example:

ruby
Másolás
Szerkesztés
new func CreateFunction*$parameter list$ new b BoolParam.$
:
$function body$
.
The function body always starts with a colon (:)

The declaration ends with a dot (.)

Branches
To create a branch, use the following structure:

sql
Másolás
Szerkesztés
?Condition:
  !True: $if Condition == True$
  .
  !False: $if Condition == False$
  .
.
This works like a switch statement. The ? holds the value to evaluate, and each ! is a possible case.

Answering
Use Answer to return a value from a block or function — similar to the return keyword in other languages.
