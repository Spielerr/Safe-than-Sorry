// JavaScript code 
function search_hotel() { 
    let input = document.getElementById('searchbar').value 
    input=input.toLowerCase(); 
    let x = document.getElementsByClassName('portfolio-item'); 
      
    for (i = 0; i < x.length; i++) {  
        if (!x[i].innerHTML.toLowerCase().includes(input)) { 
            x[i].style.display="none"; 
        } 
        else { 
            x[i].style.display="";                  
        } 
    } 
} 

// $("#searchbar").on("keyup", function() {
// var g = $(this).val().toLowerCase();
// $(".row portfolio-container .fix label").each( function() {
// var s = $(this).text();
// if (s.indexOf(g)!=-1) {
// $(this).parent().parent().show();
// }
// else {
// $(this).parent().parent().hide();
// }
// });
// });