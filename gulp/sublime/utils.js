
var capitalize = function(str) {
	return str.charAt(0).toUpperCase() + str.slice(1);
}

var isNumber = function(value) {
	return typeof value === "number" && value === value;
}




exports.capitalize = capitalize;
exports.isNumber = isNumber;


