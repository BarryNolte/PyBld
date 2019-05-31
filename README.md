# PyBld

### *TODO*
---
* PyPi classifiers
* Copyright and license issues
* Readme file
* Update template
* GraphViz graph output

graph TD;
    All-->Tlink;
    Tlink-->Tprint;
    Tprint1-->Tcompile;
    Tlink-->Tcompile;
    Tprint-->Tprint1;
    Tlink-->Tprint1;

* single items vs. lists of items (can we make a list of one and have it make sense)
* Make sh() run a list of proc's that can be joined later
  * Shell - return pass/fail, return code, output text
  * ShellAsync - return handle
  * WaitForShellAsync - pass in handle, waits, returns pass/fail, return code, output text
  * 
  * ShellListAsync ??
  * ShellList ??

### *FEATURES*
* Environment get/set to pass info between makefiles
* 
  
### *TESTS*
* Single input
* List of imputs
* 