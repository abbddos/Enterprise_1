$(document).ready(function(){
  var MenuStatus = 0;
  $('#menu-icon').click(function(){
    $('.vertical-menu').animate({width: "toggle" }, 100);
    if(MenuStatus == 0){
      MenuStatus = 1;
      $("form").css('margin-left','5%');
      $("table").css('margin-left','5%');
      $('.table-in-form').css('margin-left','0%');
      $('#srch').css('margin-left','5%');
      $('.search-in-form').css('margin-left','0%');
    }

    else{
      MenuStatus = 0;
      $("form").css('margin-left','-12%');
      $("table").css('margin-left','-12%');
      $('.table-in-form').css('margin-left','0%');
      $('#srch').css('margin-left','-12%');
      $('.search-in-form').css('margin-left','0%');
    }
  });

  $('#warehouse').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#reports').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#records').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#assets').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#equities').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#liabilities').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#revenues').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#expenses').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#dividends').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#statements').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#cash-check').click(function(){
    $(this).children('li').slideToggle();
  });

  $('#budget').click(function(){
    $(this).children('li').slideToggle();
  });
});
