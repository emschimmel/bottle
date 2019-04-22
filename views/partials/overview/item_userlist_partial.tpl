<div class="list-group">
    <small id="item_user_list">

      % for item in item_user_list:
        <a href="/_open_item_for_user/{{item}}/{{all_data}}" class="list-group-item list-group-item-action list-group-item-secondary p-2
        % if selected_user_item == item:
            active
        % end
        ">{{item}}</a>
      % end
    </small>
</div>