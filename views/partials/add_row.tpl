<div class="input-group" id="row_{{row.rank}}">
    <div class="input-group-prepend">
        <span class="input-group-text" id="rank">{{row.rank}}</span>
    </div>
    <input type="text" name="recommandation_id_{{row.rank}}" id="recommandation_id_{{row.rank}}" class="form-control" placeholder="Recommendation_id" {{row.id}} />
    <input type="number" name="score_{{row.rank}}" id="score_{{row.rank}}" class="form-control col-3" placeholder="score" value="{{row.score}}" />
    <div class="input-group-append">
        <a class="btn btn-secondary btn-sm text-white
        % if not enable_remove:
            disabled
        % end
        " id="remove_row_{{row.rank}}"> - </a>
    </div>
</div>

<script type="text/javascript">
    $(function() {
      $("#remove_row_{{row.rank}}").on("click",function(e) {
        console.log("clicked")
        $.post(
            "/_remove_insert_row/{{row.rank}}",
            $("#insert_form").serialize(),
            function(data) {
                location.reload();
            }
        );
      });
    });
</script>