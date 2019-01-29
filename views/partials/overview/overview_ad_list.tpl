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