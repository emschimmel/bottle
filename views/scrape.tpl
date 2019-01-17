<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    <a href="/insert" role="button" class="btn btn-sm btn-secondary">Insert data</a>
                    <a href="/scrape" role="button" class="btn btn-sm btn-secondary active">Enrich data</a>
                    <a href="/config" role="button" class="btn btn-sm btn-secondary">Config</a>
                    <span>current tenant: {{tenant}}</span>

                </div>

            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                <div>
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <span>Pre-load data into the application</span>
                        </div>
                        <form action="/scrape" method="post" id="scrape_form" enctype="multipart/form-data">
                            <div class="modal-body">
                                <div class="form-group row ml-0 mr-0">
                                    <span class="col-5">Total to do</span>
                                    <div class="col-7 progress p-0">
                                      <div class="progress-bar bg-info" style="width: {{100 if amount_todo is 0 else (amount_done / amount_todo * 100)}}%" role="progressbar" aria-valuenow="{{amount_done}}" aria-valuemin="0" aria-valuemax="{{amount_todo}}" aria-describedby="progresHelp">{{100 if amount_todo is 0 else round(amount_done / amount_todo * 100)}}%</div>
                                    </div>
                                    <small id="progresHelp" class="offset-5 form-text text-muted">{{amount_done}} / {{amount_todo}}</small>
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="use_all" class="col-5">Use whole file</label>
                                    <input type="checkbox" checked name="use_all" id="use_all" class="form-control col-7" placeholder="start all"  onchange="document.getElementById('start').disabled = this.checked;document.getElementById('end').disabled = this.checked;;document.getElementById('amount').disabled = this.checked;" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="start" class="col-5">Start id</label>
                                    <input type="text" disabled name="start" id="start" class="form-control col-7" placeholder="Start id" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="end" class="col-5">End id</label>
                                    <input type="text" disabled name="end" id="end" class="form-control col-7" placeholder="End id" />
                                </div>
                                <div class="form-group row ml-0 mr-0">
                                    <label for="amount" class="col-5">Amount</label>
                                    <input type="number" disabled name="amount" id="amount" class="form-control col-7" placeholder="Amount" aria-describedby="amountHelp" />
                                    <small id="amountHelp" class="form-text text-muted pl-3">The amount is based on adds to scrape within the optional start id/end id range. <br />If none provided, the whole range will be used. Amount ads will also scrape the recommended adds.</small>
                                </div>
                            </div>
                            <div class="modal-footer">
                                % if amount_todo>0 and (amount_done / amount_todo * 100) <100:
                                    <span class="collapse hide" id="warning">Reloading the browser will not stop the prosess</span>
                                    <button type="button" id="start_button" class="btn btn-primary collapse show">Start</button>
                                 % else:
                                    <span class="collapse hide" id="warning">All data available</span>
                                % end
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
                var form = $('#scrape_form')
                $('#warning').show()
                $('#start_button').hide()
                $.ajax({type: "POST", url: "_start_scrape", data:form.serialize()});
            });
        </script>
    </body>
</html>