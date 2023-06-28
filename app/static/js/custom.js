$(document).ready(function() {
    $('#image_to_text').click(function(event) {
      event.preventDefault();
      $('#file').trigger('click');
    });
  
    $('#pdf_to_text').click(function(event) {
      event.preventDefault();
      $('#file').trigger('click');
    });
  
    $('#file').change(submitForm);
  
    function submitForm() {
      $('#file_form').off('submit').on('submit', function(event) {
        event.preventDefault();
        $('#sheet').removeClass('d-none');
        var formData = new FormData(this)
        $.ajax({
            data: formData,
            type: 'POST',
            url: '/',
            contentType: false,
            processData: false,
        })
        .done(function(response){
            if(response != '0'){
                $('#sheet').addClass('d-none');
                $('#zohoLink').attr('href', response);
                $('#resultModal').modal('show');
            }
            else{
                console.error('Error generating response');
            }
        })
        .fail(function(xhr, status, error){
            console.error(xhr.responseText);
            console.error(error);
            console.error(status);
        });

      });
      $('#file_form').submit();
    }
  
});
  