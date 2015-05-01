'use strict';

var util = require('util');
var path = require('path');
var net = require('net');
var gutil = require('gulp-util');




String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}




var IS_FAILURE = 0
var IS_SUCCESS = 1

var ACTION_UPDATE = 2
var ACTION_REMOVE = 4
var ACTION_RESET = 8

var ON_STATUS_BAR = 1




var reconnectTries = 0;
var socket = null;

function onSocketClosed() {
	socket = null;
	// gutil.log('Connection closed');
	reconnectSocket();
}

function onSocketError() {
	// gutil.log('Socket error')
	if (socket !== null) {
		socket.destroy();
	}
}

function onSocketConnected() {
	gutil.log('Connected to server');
	reconnectTries = 0;
	var handshake = { "id": "gulp", "action": -1 };
	socket.send(handshake);
}

function onSocketReceived(data) {
	var data = json.loads(data.toString());
}

/**
 * Reconnect the socket, but only try a maximum of 10 times 
 */
function reconnectSocket() {
	reconnectTries++;
	if (reconnectTries > 10) {
		return gutil.log('Maximum reconnect tries exceeded');
	}
	setTimeout(function () {
		// log('Reconnecting Socket')
		createSocket();
	}, 4000);
}

/**
 * Create the socket to connect to sublime 
 */
function createSocket() {
	var PORT = 30048;
	socket = net.createConnection(PORT, 'localhost');
	socket.setEncoding('utf8');

	socket.on('close', onSocketClosed);
	socket.on('error', onSocketError);
	socket.on('connect', onSocketConnected);
	socket.on('data', onSocketReceived);

	socket.send = function socket_send(data) {
		if (socket !== null) {
			socket.write(JSON.stringify(data));
		}
	};
};




var sublime = {
	/**
	 * Set a status message in Sublime 
	 * @param {String} id     The id of the status message
	 * @param {String} status The message that will be shown 
	 */
	set_status: function(id, status) {
		socket.send({
			action: ACTION_UPDATE, 
			perform_on: ON_STATUS_BAR, 
			status_id: id,
			status: status });
	},
	/**
	 * Set a status message from an error 
	 * @param  {String}
	 */
	show_error: function(id) {
		return function (err) {
			// Emit 'end' so gulp watch doesn't stop 
			this.emit('end');

			var line = err.line || err.lineNumber;
			var file = err.file || err.fileName;
			var pluginName = err.plugin.capitalize();
			
			gutil.log(err.message.split(/\n/)[0] || ''); 

			var status = util.format('%s error, Line %s, File: %s', 
				pluginName, line, path.basename(file))
			sublime.set_status(id, status);
		}
	},

};

createSocket();




module.exports = sublime;



