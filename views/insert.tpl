<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    <a href="/insert" role="button" class="btn btn-sm btn-secondary active">Insert data</a>
                    <a href="/scrape" role="button" class="btn btn-sm btn-secondary">Enrich data</a>
                    <a href="/config" role="button" class="btn btn-sm btn-secondary">Config</a>
                </div>

            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                <div>
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <ul class="nav nav-tabs bg-light">
                          <li class="nav-item"><a href="/_switch_input_format/CSV" class="nav-link text-secondary
                          % if insert_preference == "CSV":
                          text-dark active
                          % end
                          ">Upload CSV</a></li>
                          <li class="nav-item"><a href="/_switch_input_format/FORM" class="nav-link text-secondary
                          % if insert_preference == "FORM":
                          text-dark active
                          % end
                          ">Form input</a></li>
                          <li class="nav-item"><a href="/_switch_input_format/RAW" class="nav-link text-secondary
                          % if insert_preference == "RAW":
                          text-dark active
                          % end
                          ">Raw input</a></li>
                        </ul>
                        % if insert_preference == "FORM":
                            % include('partials/insert/input_form_partial.tpl')
                        % elif insert_preference == "RAW":
                            % include('partials/insert/input_raw_partial.tpl')
                        % else:
                            % include('partials/insert/upload_csv_partial.tpl')
                        % end

                    </div>
                  </div>
                </div>
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