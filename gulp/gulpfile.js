'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var plumber = require('gulp-plumber');
var gutil = require('gulp-util');
var sublime = require('./../gulp/sublime');


var logError = function(err) {
	// Log only the first line of the error message
	gutil.log(err.message.split(/\n/)[0] || '');
}


var paths = {
	'sass': 'sass/**/*.sass',
	'sassDest': 'stylesheets',
};

gulp.task('default', ['watch']);

gulp.task('compile-sass--plumber', function () {
	// Reset the sass status message 
	sublime.set_status('Sass', '');

	return gulp.src(paths.sass).
		pipe(plumber({ errorHandler: sublime.show_error('Sass') })).
		
		pipe(sass({
			indentedSyntax: true,
		})).
	
		pipe(gulp.dest(paths.sassDest));
});

gulp.task('compile-sass', function () {
	// Reset the sass status message 
	sublime.set_status('Sass', '');

	return gulp.src(paths.sass).
		
		pipe(sass({
			indentedSyntax: true,
		})).
		on('error', sublime.show_error('Sass')).
	
		pipe(gulp.dest(paths.sassDest));
});

gulp.task('watch', function () {
	gulp.watch([
			paths.sass,
		],
		['compile-sass--plumber', 'compile-sass']
	);
	sublime.connect();
});






