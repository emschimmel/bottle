<form action="/insert" method="post" id="insert_form">

      <div class="modal-body">
            <div class="form-group form-row">
                <label for="tenant" class="col-2">Tenant</label>
                <select name="tenant" id="tenant" class="form-control col-10" placeholder="Select Tenant">
                  % for tenant_item in tenant_list:
                    <option value="{{tenant_item}}"
                        % if insert_tenant is tenant_item:
                            selected
                        % end
                    >{{tenant_item}}</option>
                  % end
                <select>
            </div>

            <div class="form-group form-row">
                <label for="start" class="col-2">Ad_id</label>
                <input type="text" name="ad_id" id="ad_id" class="form-control col-10" placeholder="ad_id" value="{{insert_ad_id}}" required />
            </div>
            <div class="form-group d-flex justify-content-between">
                <span>Recommendations</span>
                <a id="add_row" class="btn btn-secondary btn-sm text-white"> Add </a>
            </div>
            <div id="repeat_form">
                <div class="input-group form-row" id="row">
                    <div class="input-group-prepend bg-light border-right-0 col-1 pr-0">
                        <span class="input-group-text col-12 bg-light" id="rank">Rank</span>
                    </div>
                    <span name="id" id="id" class="form-control bg-light border-right-0 border-left-0">Recommendation id</span>
                    <span name="score" id="score" class="form-control col-3 bg-light border-right-0 border-left-0">Score</span>
                    <div class="input-group-append"><span class="input-group-text bg-light text-white border-left-0">  </span></div>
                </div>
                % for index, row in enumerate(insert_rows):
                    % include('partials/insert/add_row.tpl', content=row, enable_remove=len(insert_rows)>1, index=index)
                % end
            </div>

      </div>
      <div class="modal-footer">
        <button type="submit" id="insert_button" class="btn btn-primary collapse show">Insert</button>
      </div>
</form>