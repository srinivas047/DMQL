$(document).ready( function () {
    $('#myTable').DataTable({
      responsive: true,
      "pageLength": 7,
      "lengthChange": false,
      "bInfo" : false,
    //   "paging": false
        "order": [[ 2, "desc" ],[ 3, "desc" ]]
    });
} );