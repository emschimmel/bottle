<div class="collapse show" id="filter_box">
    <input type="text"
    % if no_data is True:
        disabled
    % end
    class="form-control form-control-sm collapse show" placeholder="filter for title" id="filter" value="{{filter_string}}" />
</div>
<div class="collapse hide" id="filter_wait">
    <div class="progress">
      <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 50%"></div>
    </div>
</div>

<script type="text/javascript">

    // onkeyup filter. Will delay so you can type
    var filterTimeout = null;
    $('#filter').keyup(function() {
      if (filterTimeout != null) {
        clearTimeout(filterTimeout);
      }
      filterTimeout = setTimeout(function() {
        $('#filter_box').hide()
        $('#filter_wait').show()
        filterTimeout = null;

        $.ajax({url: "_filter/"+$('#filter')[0].value, success: function(data){ location.reload();}});
      }, 1000);
    })

</script>
