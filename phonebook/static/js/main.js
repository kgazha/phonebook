$(document).ready(function() {
  $('#phonebookSearch').on('input', function() {
    var searchTerm = $(this).val().toLowerCase();
    $('#phonebookTable tbody tr').each(function() {
      var inSearch = false,
        childCell = $('td', $(this)),
        is_department = $(this).hasClass('department');
      if (is_department) {
        showDepartment = false;
        department_id = $(this).attr('id');
      }
      $.each(childCell, function(){
        let cellValue = $(this).text().trim().toLowerCase();
        if (cellValue.indexOf(searchTerm) > -1) {
          inSearch = true;
          $('#' + department_id).show();
        }
      });
      if (inSearch && childCell.length === 1) {
        showDepartment = true;
      }
      $(this)[inSearch || showDepartment ? 'show' : 'hide']();
    });
  });
  $('.toggle--open').click(function() {
    $('.sidebar').toggleClass('sidebar--active');
    $('.overlay').toggleClass('overlay--active');
  });
  $('.toggle--close').click(function() {
    $('.sidebar').toggleClass('sidebar--active');
    $('.overlay').toggleClass('overlay--active');
  });

  $('.overlay').click(function() {
    $('.sidebar').toggleClass('sidebar--active');
    $('.overlay').toggleClass('overlay--active');
  });

  $(window).resize(function(){
    if($('.toggle--open').is(':hidden')){
      $('.sidebar').removeClass('sidebar--active');
      $('.overlay').removeClass('overlay--active');
    }
  });
});
