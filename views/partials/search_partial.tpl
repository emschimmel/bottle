<div class="collapse show" id="search_box">
    <input type="text"
    % if no_data is True:
        disabled
    % end
    class="form-control form-control-sm collapse show" placeholder="not yet working search" id="search" value="{{search_string}}" />
</div>
<div class="collapse hide" id="search_wait">
    <div class="progress">
      <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 50%"></div>
    </div>
</div>

<script type="text/javascript">

    // onkeyup search. Will delay so you can type
    var searchTimeout = null;
    $('#search').keyup(function() {
      if (searchTimeout != null) {
        clearTimeout(searchTimeout);
      }
      searchTimeout = setTimeout(function() {
        $('#search_box').hide()
        $('#search_wait').show()
        searchTimeout = null;

        $.ajax({url: "_search/"+$('#search')[0].value, success: function(data){ location.reload();}});
      }, 1000);
    })

</script>
