<form action="/insert" method="post" id="insert_form">

      <div class="modal-body">
            <div class="form-group">
                <label for="tenant">Tenant</label>
                <select name="tenant" id="tenant" class="form-control" placeholder="Select Tenant">
                  % for tenant_item in tenant_list:
                    <option value="{{tenant_item}}"
                        % if insert_tenant is tenant_item:
                            selected
                        % end
                    >{{tenant_item}}</option>
                  % end
                <select>
            </div>

            <div class="form-group">
                <label for="start">Ad_id</label>
                <input type="text" name="ad_id" id="ad_id" class="form-control" placeholder="ad_id" value="{{insert_ad_id}}" required />
            </div>
            <div class="form-group d-flex justify-content-between">
                <span>Recommendations</span>
                <a id="add_row" class="btn btn-secondary btn-sm text-white"> Add </a>
            </div>
            <div id="repeat_form">
                % for index, row in enumerate(insert_rows):
                    % include('partials/add_row.tpl', content=row, enable_remove=len(insert_rows)>1, index=index)
                % end
            </div>

      </div>
      <div class="modal-footer">
        <button type="submit" id="insert_button" class="btn btn-primary collapse show">Insert</button>
      </div>
</form>