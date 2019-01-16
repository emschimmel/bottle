<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    <a href="/insert" role="button" class="btn btn-sm btn-secondary active">Insert</a>
                    <a href="/upload" role="button" class="btn btn-sm btn-secondary">Upload CSV</a>
                    <a href="/config" role="button" class="btn btn-sm btn-secondary">Config</a>
                </div>
                <div class="col-3">
                    <div class="collapse show" id="search_box">
                        <input type="text" disabled class="form-control form-control-sm collapse show" placeholder="can't search during insert" id="search" value="" />
                    </div>
                </div>
            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                <form action="/insert" method="post" id="insert_form">
                    <div>
                      <div class="modal-dialog" role="document">
                        <div class="modal-content">
                          <div class="modal-body">
                                <div class="form-group">
                                    <label for="tenant">Tenant</label>
                                    <select name="tenant" id="tenant" class="form-control" placeholder="Select Tenant">
                                      % for tenant in tenant_list:
                                        <option value="{{tenant}}"
                                            % if insert_tenant is tenant:
                                                selected
                                            % end
                                        >{{tenant}}</option>
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
                        </div>
                      </div>
                    </div>
                </form>
              </div>
            </div>
        </div>
        <script type="text/javascript">
            $(function() {
              $("#add_row").on("click",function(e) {
                console.log("clicked")
                $.post(
                    "/_add_insert_row",
                    $("#insert_form").serialize(),
                    function(data) {
                        location.reload();
                    }
                );
              });
            });
        </script>
    </body>
</html>