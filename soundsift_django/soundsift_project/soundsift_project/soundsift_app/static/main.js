(function(){
	window.onload = function() {
		// wave physics
		var waveEnergy = 0
		var decayConstant = 0.8

		// mouse tracking
		var pastX = 0, pastY = 0

		// sine rendering
		var xDel = window.innerWidth/20 // 20/4 = 5 periods of the sine wave shown
		var yAxis = window.innerHeight/2
		var pathElement = document.getElementById('ola')
		var currPath = new Array(41)
		var amplitude = 0


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

		var getAmplitude = function() {
			return waveEnergy
		}

		var init = function() {
			amplitude = getAmplitude()
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
		}

		var setPath = function(path) {
			var pathString = 'M'
			for (var i=0; i<path.length; i+=2) {
				if i==0 {
					pathString += path[i][0].toString() + ',' + path[i][1].toString() + ' '
					pathString += 'C' + Math.round((path[i][0]+path[i+1][0])/2).toString() + ',' +  path[i+1][1].toString() + ' '
					pathString += Math.round((path[i+1][0]+path[i+2][0])/2).toString() + ',' + path[i+2][1].toString() + ' '
					pathString += path[i+2][0].toString() + ',' + path[i+2][1].toString() + ' '
				}
				else {
					pathString += 'C' + Math.round((path[i][0]+path[i+1][0])/2).toString() + ',' +  path[i+1][1].toString() + ' '
					pathString += Math.round((path[i+1][0]+path[i+2][0])/2).toString() + ',' +  path[i+2][1].toString() + ' '
					pathString += path[i+2][0].toString() + ',' + path[i+2][1].toString() + ' '
				}
			}
			pathElement.setAttribute('d',pathString)
		}

		var computePath = function() {
			amplitude = getAmplitude()
			for (var i = 0; i<41; i++) {
				if i%4 == 1 {
					currPath[i][1] = [Math.round(yAxis+amplitude)]
				}
				else if i%4 == 3 {
					currPath[i][1] = [Math.round(yAxis-amplitude)]
				}
			}
			setPath(currPath)
			setTimeout(function() {computePath(currPath)},200)
		}

		window.onmousemove = addEnergy
		init()
		computePath()
	}
})();