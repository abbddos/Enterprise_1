$(document).ready(function(){
    $('#srch').keyup(function(){
      search_table($(this).val());
    });

    function search_table(value){
      $('.table-row').each(function(){
        
        $(this).each(function(){
          if($(this).text().toLocaleLowerCase().indexOf(value.toLocaleLowerCase()) >= 0){ $(this).show();}
          else{$(this).hide();}
        });
      });
    }
  });