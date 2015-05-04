'use strict';

var net = require('net');


function socket_send(data) {
	this.write(JSON.stringify(data));
};


/**
 * A factory for creating sockets 
 * @param {Object} options  The options for connecting the port 
 * @param {Function} fn     The on connect handler 
 */
function createSocket(options, fn) {
	if (typeof options !== "object") {
		throw new Error('Socket options were not specified');
	}

	var host = options.host || 'localhost';
	var port = Number(options.port);

	if (typeof port !== 'number' || port !== port) {
		throw new Error('The port specified is invalid: ' + port)
	}

	var socket = net.createConnection(port, host || 'localhost');
	socket.setEncoding('utf8');

	// Add event handlers to the socket 
	if (typeof options.on === "object") {
		for (var eventName in options.on) {
			if ( ! options.on.hasOwnProperty(eventName)) { continue; }
			var eventHandler = options.on[eventName];
			socket.on(eventName, eventHandler);
		}
	}

	// Add the fn, which is the on connect handler 
	if (typeof fn === "function") {
		socket.on('connect', fn);
	}

	socket.send = socket_send;

	return socket;
};


module.exports.createSocket = createSocket;






