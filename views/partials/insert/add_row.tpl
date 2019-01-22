<div class="input-group form-row" id="row_{{index}}">
    <div class="input-group-prepend col-1 pr-0">
        <span class="input-group-text col-12" id="rank_{{index}}">{{row.rank}}</span>
    </div>
    <input type="text" name="id_{{index}}" id="id_{{index}}" class="form-control" placeholder="Recommendation id" value="{{row.id}}" required />
    <input type="number" name="score_{{index}}" id="score_{{index}}" class="form-control col-3" placeholder="score" value="{{row.score}}" />
    <div class="input-group-append">
        <a class="btn btn-secondary btn-sm text-white
        % if not enable_remove:
            disabled
        % end
        " id="remove_row_{{row.rank-1}}"> - </a>
    </div>
</div>

<script type="text/javascript">
    $(function() {
      $("#remove_row_{{index}}").on("click",function(e) {
        console.log("clicked")
        $.post(
            "/_remove_insert_row/{{index}}",
            $("#insert_form").serialize(),
            function(data) {
                location.reload();
            }
        );
      });
    });
</script>