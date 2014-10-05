(function(){
	window.onload = function() {
		var waveEnergy = 0
		var decayConstant = 0.8
		var pastX = 0, pastY = 0
		var addEnergy = function(e) {
			var currX = e.clientX
			var currY = e.clientY
			var dx = currX  - pastX
			var dy = currY - pastY
			var dist = Math.sqrt(Math.pow(dx,2)+Math.pow(dy,2));
			waveEnergy = waveEnergy*decayConstant + dist
			pastX = currX
			pastY = currY
		}
		window.onmousemove = addEnergy
		var getAmplitude = function() {
			return waveEnergy
		}
		xDel = window.innerWidth/20 //There 10 periods of the sine wave shown
		yAxis = window.innerHeight/2

		var amplitude = getAmplitude()
		var currPath = new Array(40)
		for (var i = 0; i<40; i++) {
			if i%4 == 1 {
				currPath[i] = [xDel*i, Math.round(yAxis+amplitude)]
			}
			else if i%4 == 3 {
				currPath[i] = [xDel*i, Math.round(yAxis-amplitude)]
			}
			else {
				currPath[i] = [xDel*i, Math.round(yAxis)]
			}
		}

	var computePath = function(prevPath) {

		setTimeout(computePath,200)
	}
})();