<div class="row h-100 pre-scrollable">

% for index, current_ad in enumerate(item_list):
    % if not index%6:
        <div class="col-12 row">
    % end

            <div class="col-2 p-1">
               % include('partials/overview/ad_list_item.tpl')

            </div>

    % if not (index+1)%6:
        </div>
    % end
% end
</div>
</div>
% include('partials/overview/pagination_partial.tpl')

<script type="text/javascript">
    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    })
    function showMore(id_more, id_block, id_block_second, id_less) {
        $('#'+id_more).addClass("d-none");
        $('#'+id_block_second).addClass("d-none");
        $('#'+id_block).removeClass("d-none");
        $('#'+id_less).removeClass("d-none");
    }
    function showLess(id_more, id_block, id_block_second, id_less) {
        $('#'+id_more).removeClass("d-none");
        $('#'+id_block_second).removeClass("d-none");
        $('#'+id_block).addClass("d-none");
        $('#'+id_less).addClass("d-none");
    }

    function reload(val){
        $.ajax({url: "_reload/"+val, success: function(data){
            location.reload();
        }});
    }
</script>