    const btnDelete= document.querySelectorAll('.btn-delete');
    if(btnDelete) {
      const btnArray = Array.from(btnDelete);
      btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
          if(!confirm('Вы уверены, что хотите удалить данную запись?')){
            e.preventDefault();
          }
        });
      })
    }

    $(document).ready(function() {
        $('#documents').DataTable({
           "language": {
            "url": "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
           },
          "aLengthMenu": [[3, 5, -1], [3, 5, "Все"]],
            "iDisplayLength": 5
           }
        );
    } );

    $(function(){
        $('#documents').tablesorter();
     });

    $('.dropdown').click(function(){
       $('.dropdown-menu').toggleClass('show');
   });