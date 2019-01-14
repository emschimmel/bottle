<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    <a href="/upload" role="button" class="btn btn-sm btn-secondary active">Upload</a>
                    <a href="/config" role="button" class="btn btn-sm btn-secondary">Config</a>
                </div>
                <div class="col-3">
                    <div class="collapse show" id="search_box">
                        <input type="text" disabled class="form-control form-control-sm collapse show" placeholder="can't search during upload" id="search" value="" />
                    </div>
                </div>
            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <div>
                      <div class="modal-dialog" role="document">
                        <div class="modal-content">
                          <div class="modal-body">
                                <div class="form-group">
                                    <label for="tenant">Tenant</label>
                                    <select name="tenant" id="tenant" class="form-control" placeholder="Select Tenant">
                                      % for tenant in tenant_list:
                                        <option value="{{tenant}}"
                                            % if state_tenant is tenant:
                                                selected
                                            % end
                                        >{{tenant}}</option>
                                      % end
                                    <select>
                                </div>
                                <div class="form-group">
                                    <label for="upload">CSV file</label>
                                    <input type="file" name="upload" id="upload" class="form-control" placeholder="Select file" />
                                </div>
                                <!--
                                <div class="form-group">
                                    <label for="use_all">Use whole file</label>
                                    <input type="checkbox" name="use_all" id="use_all" class="form-control" placeholder="Use all"  onchange="document.getElementById('start').disabled = !this.checked;document.getElementById('end').disabled = !this.checked;" />
                                </div>
                                <div class="form-group">
                                    <label for="start">Start</label>
                                    <input type="number" name="start" id="start" class="form-control" placeholder="Start" />
                                </div>
                                <div class="form-group">
                                    <label for="end">End</label>
                                    <input type="number" name="end" id="end" class="form-control" placeholder="End" />
                                </div>
                                -->

                          </div>
                          <div class="modal-footer">
                            <button type="submit" id="upload_button" class="btn btn-primary collapse show">Upload</button>
                          </div>
                        </div>
                      </div>
                    </div>
                </form>
              </div>
            </div>
        </div>
         <script type="text/javascript">
            // block upload button after click
            $('#upload_button').click(function() {
                $('#upload_button').hide()
            })

        </script>
    </body>
</html>