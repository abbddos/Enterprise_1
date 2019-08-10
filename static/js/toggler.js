$(document).ready(function(){
  $('#warehouse').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#reports').click(function(){
    $(this).children('li').slideToggle();
  });
});
