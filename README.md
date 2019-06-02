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
* Make Shell* run a list of proc's that can be joined later
  * Shell - return pass/fail, return code, output text
  * ShellAsync - return handle
  * ShellWaitForAsync - pass in handle, waits, returns pass/fail, return code, output text
  * 

### *FEATURES*
* 
  
### *TESTS*
* Single input
* List of inputs
* 