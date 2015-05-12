# My Sublime Customizations



#### Gulp integration
I got sick of going back to to command prompt every time I got a Sass error. I use a local server in Sublime to communicate with gulp files. 

<!-- I use a local server in Sublime to communicate with gulp files so Sass and JS compilation errors display in Sublime's status bar. An example error message is as such: "gulp-sass error, Line 9, File: _base.sass". Multiple gulp files can connect to Sublime's server at one time.  -->

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



