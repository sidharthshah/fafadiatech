// JavaScript Document

var overAndClick;


	function closeOtrs(id){
		if(id == 'dp'){
			document.getElementById('md').style.display = "none";
			document.getElementById('r').style.display = "none";
			document.getElementById('um').style.display = "none";
			}
		if(id == 'md'){
			document.getElementById('dp').style.display = "none";
			document.getElementById('r').style.display = "none";
			document.getElementById('um').style.display = "none";
			}
		if(id == 'r'){
			document.getElementById('dp').style.display = "none";
			document.getElementById('md').style.display = "none";
			document.getElementById('um').style.display = "none";
			}
		if(id == 'um'){
			document.getElementById('dp').style.display = "none";
			document.getElementById('md').style.display = "none";
			document.getElementById('r').style.display = "none";
			}
		}

	function activeLeftMenu(currentElement){
		for(var i=1; i<=10;i++){
				document.getElementById('a'+i).style.background = "#e8e8e8";
			}
			currentElement.style.background = "white";			
		}
		

	function activeTab(id){
		
			//sidebar starts
		   var trChk = document.getElementById(id);
				if(trChk.className == 'openTree') {
					trChk.className = 'closeTree';
					}
					else {
					trChk.className = 'openTree';
			}
			//sidebar starts
		
		
			//course submenu starts
			if(overAndClick == 'dp') {
				document.getElementById('dp1').className = "current_tb";
			}
			else {
				document.getElementById('dp1').className = "current_tb_p";				
				}
			if(overAndClick == 'md') {
				document.getElementById('md1').className = "current_tb";
			}
			else {
				document.getElementById('md1').className = "current_tb_p";				
				}
			if(overAndClick == 'r') {
				document.getElementById('r1').className = "current_tb";
			}
			else {
				document.getElementById('r1').className = "current_tb_p";				
				}
			if(overAndClick == 'um') {
				document.getElementById('um1').className = "current_tb";
			}
			else {
				document.getElementById('um1').className = "current_tb_p";				
				}
			//course submenu starts

		}
		
		
	
    function tgl_vis(id) {
		closeOtrs(id);
       var e = document.getElementById(id);
	if(e.style.display == 'block'){
		overAndClick = id;
          e.style.display = 'none';
		  abc = 'close';
		  
}
       else
          e.style.display = 'block';
			overAndClick = id;
		  abc = 'open';
		  
    }



