$(document).ready(function(){
    $('.t-sheet').click(function(){
        $('#myModal1').show();
      });
    
      $('.close').click(function(){
        $('#AccountContent').find('tr').remove(); 
        $('#dbt').text('');
        $('#cdt').text(''); 
        $('#myModal1').hide();
      });
});