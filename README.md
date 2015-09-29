# My Sublime Customizations

#### File size

The size of a file is displayed in the status bar and is updated on_modified. The size is displayed in kilobytes like such: "0.94 KB". 

#### File save status

The status bar will display "Unsaved" if a file is unsaved. If the file is saved, the status bar gets nothing added and the "Unsaved" message is removed. 

#### Gulp integration

Something that is not included here, is the server I use to receive error messages from Gulp files. It can be found [here](https://github.com/anthonykoch/sublimegulpserver). 


## Commands

#### RemoveWhiteSpaceSelectionLinesCommand
Removes selection lines that are just whitespace. It is meant to be used after split_selection_into_lines so that only lines that have text (not just whitespace) are selected.


## Build Systems
 
#### Node

Uses babel-node to compile and run ES6 javascript. 

#### Mocha

Used to run tests. 