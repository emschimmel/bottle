<form action="/insert_raw" method="post" id="insert_raw">
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
                <textarea  class="form-control" id="input_raw" name="input_raw" aria-describedby="inputRawHelp">
                </textarea>
                <small id="inputRawHelp" class="form-text text-muted">
                    columns: "ad_id,recommended_ad_id,rank,score" example input:<br />
                    <span class="border d-inline-block w-100 p-2 bg-light rounded">
                    102181900,122858750,1,0.6896<br />
                    102447794,166094071,1,0.9552<br />
                    102447794,463382718,2,0.9519<br />
                    102447794,287804816,3,0.9035
                    </span>
                </small>
            </div>

      </div>
      <div class="modal-footer">
        <button type="submit" id="insert_button" class="btn btn-primary collapse show">Insert</button>
      </div>
</form>