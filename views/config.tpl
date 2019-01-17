<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    % if not offline_mode:
                        <a href="/insert" role="button" class="btn btn-sm btn-secondary">Insert data</a>
                        <a href="/scrape" role="button" class="btn btn-sm btn-secondary">Enrich data</a>
                    % end
                    <a href="/config" role="button" class="btn btn-sm btn-secondary active">Config</a>
                    <span>current tenant: {{tenant}}</span>
                </div>
            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                <div>
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <span>Change the default behaviour of the application</span>
                        </div>
                        <form action="/config" method="post" enctype="multipart/form-data">
                            <div class="modal-body">
                                <div class="form-group row ml-0 mr-0">
                                    <label for="tenant" class="col-5">Tenant</label>
                                    <select name="tenant" id="tenant" class="form-control col-7" placeholder="Select Tenant">
                                      % for tenant_item in tenant_list:
                                        <option value="{{tenant_item}}"
                                        % if tenant == tenant_item:
                                            selected
                                        % end
                                        >{{tenant_item}}</option>
                                      % end
                                    <select>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="search_string" class="col-5">Default search string</label>
                                    <input type="text" name="search_string" id="search_string" class="form-control col-7" placeholder="default search string" value="{{search_string}}" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="selected_item" class="col-5">Default selected item</label>
                                    <input type="text" name="selected_item" id="selected_item" class="form-control col-7" placeholder="default selected item" value="{{selected_item}}" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="max_per_page" class="col-5">Default amount per page</label>
                                    <select name="max_per_page" id="max_per_page" class="form-control col-7" placeholder="Select Tenant">
                                      % for selectable_amount in selectable_page_amounts:
                                        <option value="{{selectable_amount}}"
                                        % if max_per_page is int(selectable_amount):
                                            selected
                                        % end
                                        >{{selectable_amount}}</option>
                                      % end
                                    <select>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="offline_mode" class="col-5">Use offline</label>
                                    <input type="checkbox" name="offline_mode" id="offline_mode" class="form-control col-7" placeholder="offline"
                                     % if offline_mode:
                                        checked
                                     % end
                                     />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="insert_preference" class="col-5">Input preference</label>
                                    <select name="insert_preference" id="insert_preference" class="form-control col-7" placeholder="Select input preference">
                                      % for item in input_options:
                                        <option value="{{item}}"
                                        % if item == insert_preference:
                                            selected
                                        % end
                                        >{{item}}</option>
                                      % end
                                    <select>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="submit" id="save_button" class="btn btn-primary collapse show">Save</button>
                            </div>
                        </form>
                     </div>
                  </div>
                </div>
              </div>
            </div>
        </div>

    </body>
</html>