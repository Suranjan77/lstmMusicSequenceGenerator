window.onload = function(){
	var slider = document.getElementById("diversity");
	var output = document.getElementById("rangeValue");
	output.innerHTML = slider.value;

	slider.addEventListener('input', slided);

	function slided() {
  		output.innerHTML = this.value;
	}
}

function generateCall(theUrl, downloadPath){
	var filename = document.getElementById('filename').value;
	var genreOpt = document.getElementById('genre');
	var genre = genreOpt.options[genreOpt.selectedIndex].value;
	var length = document.getElementById('length').value;
	var diversity = document.getElementById('diversity').value;
	var apiurl = theUrl + "?" + "genre=" + genre + "&filename=" + filename + "&diversity=" + diversity + "&noteslength=" + length;
	asyncGenerator(apiurl, generatedMusic, downloadPath);
	return false;
}

function generatedMusic(data, downloadPath){
	var generatedFileUrl = data.generatedfile;
	var status = data.status;
	var genefile = generatedFileUrl.split("\\");
	var generatedfileName = genefile[genefile.length - 1];
	var base_url = "http://127.0.0.1:8080";
	var filepath = base_url+downloadPath+"?filename="+encodeURIComponent(generatedfileName);
	document.getElementById("loader").style.display = "none";
	document.getElementById("formcontainer").style.display = "block";
	document.getElementById('formcontainer').innerHTML = "<p>Download generated music</p>"
															+"<br><br><button id=\"redbtn\" onclick="
														  	+"\"window.open(\'"+filepath+"\')\">"
														  	+generatedfileName
															+"</button>";
	return false;
}

function asyncGenerator(theUrl, callback, downloadPath){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200){
            var datas = JSON.parse(xmlHttp.responseText);
            callback(datas, downloadPath);
        }
    }
    document.getElementById("formcontainer").style.display = "none";
    document.getElementById("loader").style.display = "block";
    xmlHttp.open("GET", theUrl, true);
    xmlHttp.send(null);
}