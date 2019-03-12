$(document).ready(function() {
    $('#phonebookSearch').on('input', function() {
        var searchTerm = $(this).val().toLowerCase();
        $('#phonebookTable tbody tr').each(function() {
            var inSearch = false,
                childCell = $('td', $(this)),
                isDepartment = $(this).hasClass('department');
            if (isDepartment) {
              showDepartment = false;
              departmentId = $(this).attr('id');
            }
            $.each(childCell, function(){
              let cellValue = $(this).text().trim().toLowerCase();
              if (cellValue.indexOf(searchTerm) > -1) {
                inSearch = true;
                $('#' + departmentId).show();
              }
            });
            if (inSearch && childCell.length === 1) {
              showDepartment = true;
            }
            $(this)[inSearch || showDepartment ? 'show' : 'hide']();
        });
    });
});
