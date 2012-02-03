//	Vamos a presuponer que el usuario es una persona inteligente...
var isIE = false;

//	Creamos una variable para el objeto XMLHttpRequest
var req;

//	Creamos una funcion para cargar los datos en nuestro objeto.
//	Logicamente, antes tenemos que crear el objeto.
//	Vease que la sintaxis varia dependiendo de si usamos un navegador decente
//	o Internet Explorer
function updateTTL(ttlid) {
	//	Primero vamos a ver si la URL es una URL :)
	//if(ttlid==''){
	//	return;
	//}
	rr = ttlid.name;
	ttl = ttlid.value;
	url = "/dns/ttl/"+rr+"/"+ttl+"/";
	//alert(url);
	//	Usuario inteligente...
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
		req.onreadystatechange = processReqChange(rr);
		req.open("GET", url, true);
		req.send(null);
	//	...y usuario de Internet Explorer Windows
	} else if (window.ActiveXObject) {
		isIE = true;
		req = new ActiveXObject("Microsoft.XMLHTTP");
		if (req) {
			req.onreadystatechange = processReqChange;
			//req.open("GET", url, false);
			req.open("GET", url, true);
			req.send();
		}
	}
}

//	Funcion que se llama cada vez que se dispara el evento onreadystatechange
//	del objeto XMLHttpRequest
function processReqChange(id){
	var rrtd = "ttl-"+id;
	var detalles = document.getElementById(rrtd);
	detalles.innerHTML = '<img src="/media/loading.gif" align="middle" /> ';
	//detalles.innerHTML = "mundo";
	//detalles.innerHTML = "hola";
	//alert(rrtd);
	//alert(detalles.innerHTML);

	//alert(req.readyState);
	//alert(req.responseText);

	if(req.readyState == 4){
		detalles.innerHTML = "actualizado"
		//detalles.innerHTML = req.responseText;
	} else {
		//detalles.innerHTML = '<img src="/media/loading.gif" align="middle" /> ';
		//detalles.innerHTML = "hola";
		detalles.innerHTML = "actualizando"
		//detalles.innerHTML = req.responseText;
		//detalles.innerHTML = "error"
		//setTimeout ("alert(rrtd)", 1000); 
		//setTimeout ("todobien()", 1000); 
	}
}
/*
*/
function todobien(){
	var detalles = document.getElementById("ttl-79");
	alert(id);
	detalles.innerHTML = "mundo";
}
