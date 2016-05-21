# My Sublime Customizations

#### File size

The size of a file is displayed in the status bar and is updated on_modified_async every time there is a change in 32 characters. The size is displayed in kilobytes e.g. `0.94 KB`. 

#### File save status

The status bar will display "Unsaved" if a file is unsaved. If the file is saved, the status bar gets nothing added and the "Unsaved" message is removed. 

#### Gulp integration

I also run a local server which can receive and display error messages from Gulp Tasks, which may be [found here](https://github.com/anthonykoch/editorconnect-sublime). 


## Commands

#### RemoveWhiteSpaceSelectionLinesCommand

Removes selection lines that are just whitespace. Each line must be separately selected (e.g. after running split_selection_into_lines) in order for it to work properly. 


## Build Systems

#### Node

Runs a JavaScript file with ES6 syntax enabled. 

#### InfoNode

Runs a JavaScript file with ES6 syntax enabled. This build option also set's the trace-opt flag so that V8 will output optimization information. 

#### Tape

Runs a JavaScript file and pipes its output to tap-spec. This assumes the file tap-spec is available to the file being run. 

#### Mocha

Used to run mocha tests (indivdual files) with ES6 syntax enabled. Babel must be globally installed from npm first.  