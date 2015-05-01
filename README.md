# My Sublime Customizations


<dl>
	<dt>Gulp integration</dt>
	<dd>
		I use a local server in Sublime to communicate with gulp files so Sass and JS compilation errors display in Sublime's status bar. An example error message is as such: "gulp-sass error, Line 9, File: _base.sass". Multiple gulp files can connect to Sublime's server at one time. 
	</dd>

	<dt>File size</dt>
	<dd>
		The size of a file is displayed in the status bar and is updated on_modified. The size is displayed in kilobytes like such: "0.94 KB". 
	</dd>

	<dt>File save status</dt>
	<dd>
		The status bar will display "Unsaved" if a file is unsaved. If the file is saved, the status bar gets nothing added and the "Unsaved" message is removed. 
	</dd>
</dl>
<br>

## Commands
<dl>
	<dt>RemoveWhiteSpaceSelectionLinesCommand</dt>
	<dd>
		Removes selection lines that are just whitespace. It is meant to be used after split_selection_into_lines so that only lines that have text (not just whitespace) are selected.
	</dd>
	<dt>TrimTrailingWhiteSpaceInSelectionCommand</dt>
	<dd>
		Removes trailing whitespace in a selection of text. 
	</dd>

</dl>
<br>


## Build Systems
<dl>
 	<dt>NodeBuild</dt>
 	<dd>Used to run NodeJS files.</dd>
</dl> 



