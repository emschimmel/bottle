<div class="list-group">
    <small id="item_list">

      % for item in item_list:
        <a href="/_open_item/{{item}}" class="list-group-item list-group-item-action list-group-item-secondary p-2
        % if selected_item == item:
            active
        % end
        ">{{item}}</a>
      % end
    </small>
</div>