$(document).ready(function(){
    $('#srch').keyup(function(){
      search_table($(this).val());
    });

    $('#srch-itm').keyup(function(){
      search_itm($(this).val());
    });

    $('#srch-pkg').keyup(function(){
      search_pkg($(this).val());
    });

    $('#srch-srv').keyup(function(){
      search_srv($(this).val());
    });

    function search_table(value){
      $('.table-row').each(function(){
        
        $(this).each(function(){
          if($(this).text().toLocaleLowerCase().indexOf(value.toLocaleLowerCase()) >= 0){ $(this).show();}
          else{$(this).hide();}
        });
      });
    }

    function search_itm(value){
      $('.table-row-itm').each(function(){
        
        $(this).each(function(){
          if($(this).text().toLocaleLowerCase().indexOf(value.toLocaleLowerCase()) >= 0){ $(this).show();}
          else{$(this).hide();}
        });
      });
    }

    function search_pkg(value){
      $('.table-row-pkg').each(function(){
        
        $(this).each(function(){
          if($(this).text().toLocaleLowerCase().indexOf(value.toLocaleLowerCase()) >= 0){ $(this).show();}
          else{$(this).hide();}
        });
      });
    }

    function search_srv(value){
      $('.table-row-srv').each(function(){
        
        $(this).each(function(){
          if($(this).text().toLocaleLowerCase().indexOf(value.toLocaleLowerCase()) >= 0){ $(this).show();}
          else{$(this).hide();}
        });
      });
    }

  });