function goDoSomething(data_id){       
  var woid = data_id;
  var infoModal = $('#exampleModal');
  const Http = new XMLHttpRequest();
  // const url='https://jsonplaceholder.typicode.com/posts';
  const url = "http://"+document.location.host+"/api/get_data/woid?wo="+data_id;
  Http.open("GET", url);
  Http.send();
  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
    infoModal.find('.modal-body').html(Http.responseText);
    infoModal.modal('show');
  }
}

function goDoTakeId(data_id){    
  // console.log("HMMM");   
  var datasid = data_id;
  var infoModal = $('#printviewModal');
  // console.log("data-id:"+data_id); 
  var splitit = data_id.split(",");
  var woid = splitit[0];
  var num = splitit[1]
  
  // const Http = new XMLHttpRequest();
  // // const url='https://jsonplaceholder.typicode.com/posts';
  // const url = "http://"+document.location.host+"/api/get_data/woid?wo="+data_id;
  // Http.open("GET", url);
  // Http.send();
  // Http.onreadystatechange = (e) => {
  //   console.log(Http.responseText)
  //   // document.getElementById('akum').innerHTML = obj.akum_mach;
  //   // var obj = JSON.parse(Http.responseText); 
  //   infoModal.find('#modalbody').html(Http.responseText);
  //   infoModal.modal('show');
  // }
}

function printAll(){
  console.log("printall");
  
  const Http = new XMLHttpRequest();
  const url = "http://"+document.location.host+"/api/reprint";
  Http.open("GET", url);
  Http.send();
  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }
}

function printdatas(data_id){
  // var woid = data_id;
  console.log("data-id: "+data_id);
  const Http = new XMLHttpRequest();
  const url = "http://"+document.location.host+"/api/sreprint?param="+data_id;
  
  Http.open("GET", url);
  Http.send();
  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }
}