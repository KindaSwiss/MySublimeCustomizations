'use strict';

var util = require('util');
var path = require('path');

var utils = require('./utils');
var createSocket = require('./socket').createSocket;


var PORT = 30048;


var IS_FAILURE = 0
var IS_SUCCESS = 1

var ACTION_UPDATE = 2
var ACTION_REMOVE = 4
var ACTION_RESET = 8

var ON_STATUS_BAR = 2


/**
 * The maximum number of times the socket will try to reconnect to sublime 
 * @type {Number}
 */
var MAX_TRIES = 10;


/**
 * This array holds functions which are added by sublime.disconnect 
 * each callback is removed right after it is called 
 * @type {Array}
 */
var tempDisconnectHandlers = [];

var socketEventHandlers = {
	close: function onSocketClosed() {
		// console.log('Connection closed');
		// console.log(tempDisconnectHandlers)
		sublime.connected = connected = false;
		
		while (tempDisconnectHandlers.length) {
			var listener = tempDisconnectHandlers.shift();
			listener();
		}

		sublime.reconnect();
	},
	error: function onSocketError() {
		// console.log('Socket error')
		this.destroy();
	},
	connect: function onSocketConnected() {
		sublime._tries = 0;
		sublime.connected = connected = true;
		// console.log('Connected to server: %s', sublime.connected);

		var handshake = { "id": "gulp", "action": -1 };
		this.send(handshake);
	},
	data: function onSocketReceived(data) {
		var data = json.loads(data.toString());
	}
}


/**
 * Whether or not the socket is connected
 * @type {Boolean}
 */
var connected = false;

var sublime = {
	_connection: null,
	_tries: 0,
	connected: false,
	/**
	 * Reconnect to sublime server  
	 * @param {Function} fn A listener to the new socket's "connect" event 
	 */
	reconnect: function (fn) {
		this._tries++;
		if (this._tries > MAX_TRIES) {
			return console.log('Max reconnect tries exceeded');
		}

		// this 
		setTimeout(function () {
			this._connection = createSocket({
				port: PORT,
				on: socketEventHandlers
			}, fn);
		}.bind(this), 5000);
	},
	/**
	 * Connect the server to sublime 
	 */
	connect: function (options, fn) {
		var port = typeof options === "object" && utils.isNumber(options.port) ? options.port : PORT;
		
		if (this._connection) {
			this._connection.destroy();
		}

		if (typeof options === "function") {
			fn = options;
		}

		this._connection = createSocket({
			host: 'localhost',
			port: port,
			on: socketEventHandlers
		}, fn);
	},
	/**
	 * Disconnect the socket. The socket will emit a close event when destroyed. 
	 * @param  {Function} fn  A function that will be called when the socket is closed 
	 */
	disconnect: function (fn) {
		if (this._connection) {
			if (typeof fn === "function" && connected) {
				tempDisconnectHandlers.push(fn);
			}
			// console.log(typeof fn === "function" ? fn.name : "", typeof fn === "function", connected)
			this._connection.destroy();
		}
	},
	/**
	 * Set a status message in Sublime 
	 * @param {String} id     The id of the status message
	 * @param {String} status The message that will be shown 
	 */
	set_status: function(id, status) {
		this._connection.send({
			action: ACTION_UPDATE, 
			target: ON_STATUS_BAR, 
			data: { status_id: id,
			 		status: status }
		});
	},
	/**
	 * Set a status message from an error 
	 * @param  {String}
	 */
	show_error: function(id) {
		var errorHandler = function show_error(err) {

			// Emit 'end' so gulp.watch doesn't stop 
			this.emit('end');

			var line = err.line || err.lineNumber;
			var file = err.file || err.fileName;

			// Use the plugin name (provided by plumber) or the id, 
			// if the plugin name does not exist
			// var pluginName = utils.capitalize(err.plugin) || show_error.id;
			var pluginName = err.plugin || show_error.id;
			
			// console.log(err.message.split(/\n/)[0] || ''); 
			
			'gulp-sass error, Line 25, File: _base.sass';

			var status = util.format('%s error, Line %s, File: %s', 
				pluginName, line, path.basename(file))

			sublime.set_status(id, status);

			return status;
		}
		errorHandler.id = id;

		return errorHandler;
	},

};

module.exports = sublime;



