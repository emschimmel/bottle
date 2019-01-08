<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    <a href="/upload" role="button" class="btn btn-sm btn-secondary">Upload</a>
                    <a href="/config" role="button" class="btn btn-sm btn-secondary active">Config</a>
                    <span>current tenant: {{tenant}}</span>

                </div>
                <div class="col-3">
                    <div class="collapse show" id="search_box">
                        <input type="text" disabled class="form-control form-control-sm collapse show" placeholder="can't search during config" id="search" value="" />
                    </div>
                </div>
            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                  <div class="row">
                    <div class="col-4 p-1">
                        <div class="border h-100 p-1">
                            <form action="/config" method="post" enctype="multipart/form-data">
                                <div class="form-group row ml-0 mr-0">
                                    <span class="alert alert-primary col-12">Change the default behaviour of the application</span>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="tenant" class="col-6">Tenant</label>
                                    <select name="tenant" id="tenant" class="form-control col-6" placeholder="Select Tenant">
                                      % for tenant_item in tenant_list:
                                        <option value="{{tenant_item}}"
                                        % if tenant is tenant_item:
                                            selected
                                        % end
                                        >{{tenant_item}}</option>
                                      % end
                                    <select>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="search_string" class="col-6">Default search string</label>
                                    <input type="text" name="search_string" id="search_string" class="form-control col-6" placeholder="default search string" value="{{search_string}}" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="selected_item" class="col-6">Default selected item</label>
                                    <input type="text" name="selected_item" id="selected_item" class="form-control col-6" placeholder="default selected item" value="{{selected_item}}" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="current_page" class="col-6">Default current page</label>
                                    <input type="text" name="current_page" id="current_page" class="form-control col-6" placeholder="default current page" value="{{current_page}}" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="max_per_page" class="col-6">Default current page</label>
                                    <select name="max_per_page" id="max_per_page" class="form-control col-6" placeholder="Select Tenant">
                                      % for selectable_amount in selectable_page_amounts:
                                        <option value="{{selectable_amount}}"
                                        % if max_per_page is selectable_amount:
                                            selected
                                        % end
                                        >{{selectable_amount}}</option>
                                      % end
                                    <select>
                                </div>
                                <div class="form-group row ml-0 mr-0 justify-content-end">
                                    <button type="submit" id="start_button" class="btn btn-primary collapse show">Save</button>
                                </div>
                            </form>
                         </div>
                     </div>


                    <div class="col-4 p-1">
                        <div class="border h-100 p-1">
                            <form action="/scrape" method="post" enctype="multipart/form-data">
                                <div class="form-group row ml-0 mr-0">
                                    <span class="alert alert-primary col-12">Pre-load data into the application</span>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <span class="col-6">Total to do</span>
                                    <div class="col-6 progress p-0">
                                      <div class="progress-bar bg-info" style="width: {{(amount_done / amount_todo * 100)}}%" role="progressbar" aria-valuenow="{{amount_done}}" aria-valuemin="0" aria-valuemax="{{amount_todo}}"></div>
                                    </div>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="use_all" class="col-6">Use whole file</label>
                                    <input type="checkbox" checked name="use_all" id="use_all" class="form-control col-6" placeholder="start all"  onchange="document.getElementById('start').disabled = this.checked;document.getElementById('end').disabled = this.checked;;document.getElementById('amount').disabled = this.checked;" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="start" class="col-6">Start</label>
                                    <input type="number" disabled name="start" id="start" class="form-control col-6" placeholder="Start id" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="end" class="col-6">End</label>
                                    <input type="number" disabled name="end" id="end" class="form-control col-6" placeholder="End id" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="end" class="col-6">Amount</label>
                                    <input type="number" disabled name="amount" id="amount" class="form-control col-6" placeholder="Amount" />
                                </div>
                                <div class="form-group row ml-0 mr-0 justify-content-end">
                                    <span class="col-6 collapse hide" id="warning">Reloading the browser will not stop the prosess</span>
                                    <button type="button" id="stop_button" class="btn btn-primary collapse hide">Stop</button>
                                    <button type="button" id="start_button" class="btn btn-primary collapse show">Start</button>
                                </div>
                            </form>
                        </div>
                    </div>
                    <div class="col-4 p-1">
                        <div class="border h-100 p-1">
                            <form action="/original" method="post" enctype="multipart/form-data">
                                <div class="form-group row ml-0 mr-0">
                                    <span class="alert alert-primary col-12">Use only items where data we have</span>
                                </div>
                                <div class="form-group row ml-0 mr-0 justify-content-end">
                                    <button type="button" id="start_button" class="btn btn-primary collapse show">Modify original csv file</button>
                                </div>
                            </form>
                         </div>
                     </div>
                   </div>

              </div>
            </div>
        </div>
         <script type="text/javascript">
            $('#start_button').click(function() {
                $('#warning').show()
                $('#start_button').hide()
                $('#stop_button').show()
                $.ajax({url: "_start_scrape/"});

            })
            $('#stop_button').click(function() {
                $('#warning').hide()
                $('#start_button').show()
                $('#stop_button').hide()
                $.ajax({url: "_stop_scrape/"});
            })

        </script>
    </body>
</html>