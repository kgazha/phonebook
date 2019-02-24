$(document).ready(function() {
    $('#phonebookSearch').on('input', function() {
        var searchTerm = $(this).val().toLowerCase();
        $('#phonebookTable tbody tr').each(function() {
            var lineStr = $(this).text().toLowerCase();
            if (lineStr.indexOf(searchTerm) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
});