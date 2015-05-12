# My Sublime Customizations



#### Gulp integration
I use a local server in Sublime to communicate with gulp files so Sass compilation errors can be shown in Sublime Text's status bar. It makes it nice not to have to go back and forth between Sublime and the command line. 

#### File size
The size of a file is displayed in the status bar and is updated on_modified. The size is displayed in kilobytes like such: "0.94 KB". 

#### File save status
The status bar will display "Unsaved" if a file is unsaved. If the file is saved, the status bar gets nothing added and the "Unsaved" message is removed. 


<br>


## Commands

#### RemoveWhiteSpaceSelectionLinesCommand
Removes selection lines that are just whitespace. It is meant to be used after split_selection_into_lines so that only lines that have text (not just whitespace) are selected.

#### TrimTrailingWhiteSpaceInSelectionCommand
Removes trailing whitespace in a selection of text. 


<br>


## Build Systems
 
#### Node
Used to run NodeJS files with --harmony flag so fat arrow functions, proxies, etc. can be used.



