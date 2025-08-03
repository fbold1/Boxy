# Boxy
A language made in python, hypoteticly capable of recounstructing the code in run time. 


# How does it work?
($ is used to add comments!)
Boxy uses @ to assign, and # to use blocks of code.

**assign blocks**

example: @"New Class":$Body$.
this will add a new Entity, with an Entity ID assigned to it. This ID is used to find These Entites by their Names
you can add multiple names to the same entity: @"New Class"@"Another Class":$Body$.

**find/use blocks**

example: #"New Class"/valid.
this line will return a boolean, checking if this class is actually points at az Entity.
you can add multiple names here as well: #"New Class"#"Another Class"/valid.

**sintacs**

after every command, a dot is required. This means, that creating a variable, function, calling them, reassigning, or answering should always end with dot.
* means parameters. example:
new func CreateFunction*$here come all the paramters$ new b BoolParam.$paramters also ends with a dot$ :
$body$
. $ function declaration also ends with dot$
if a command contains a body, the body should always start with a colon.

**Branches**

in order to create a branch, you will need to use this structure:
?True: $if True==?$
  !True: $ if ?==True -> True==True$
  .
  !False:$if ?==False->True==False$
  .
.
so branches work like switch!

**Answer**

Answer can be used as return. 

