
<html>
    % include('partials/head.tpl')
    <body>

        <div class="container m-0">


            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary
                    % if all_data:
                        active
                    % end
                    ">Overview</a>
                    % if not offline_mode:
                        <a href="/insert" role="button" class="btn btn-sm btn-secondary">Insert data</a>
                    % end
                    <a href="/config" role="button" class="btn btn-sm btn-secondary">Config</a>
                    <span>current tenant: {{tenant}}</span>
                </div>
                % if all_data:
                <div class="col-3">
                    % include('partials/search_partial.tpl')
                </div>
                % else:
                <div class="col-3">
                    <div class="collapse show" id="search_box">
                        <input type="text" disabled class="form-control form-control-sm collapse show" placeholder="can't search during upload" id="search" value="" />
                    </div>
                </div>
                % end
            </div>
            % if no_data is False and no_search_data is False:
                <div class="row h-100">
                  % if all_data:

                  <div class="col-2 h-100 d-inline-block">


                    <div class="row">
                      <div class="col p-0 pre-scrollable">
                        % include('partials/item_list_partial.tpl')

                      </div>
                    </div>
                    % include('partials/pagination_partial.tpl')

                  </div>
                  % end

                  <div class="col border-1">
                    % if selected_ad_complete is True and selected_ad_error is False:

                    <div class="row h-100">

                      <!--
                      <div class="col-1 bg-dark text-white d-block">
                        <a href="#" role="button" class="text-white h-100 d-inline-block ">
                          <i class="fa fa-chevron-left"></i>
                        </a>
                      </div>
                      -->

                      <div class="col-3 bg-light border-right pre-scrollable" id="selected_item">
                        % include('partials/selected_item_partial.tpl')
                      </div>
                      <div class="col-8 pre-scrollable" id="related_items">

                      % for index, recommendation in enumerate(recommendations):
                        % if not index%3:
                            <div class="row">
                        % end

                        <div class="col-4 p-1">
                           % include('partials/recommended_item_partial.tpl')

                        </div>

                        % if not (index+1)%3:
                            </div>
                        % end
                      % end
                      % if not_loaded and not offline_mode:
                        <script type="text/javascript">
                            var reloadTimeout = setTimeout(function() {
                                location.reload()
                              }, 1000);
                        </script>
                      % end
                </div>
                % else:
                <div class="row">
                    <div class="col-12 ml-2 pr-0 mt-3">
                        <span class="alert alert-danger d-block mr-5">
                        % if selected_ad_error is True:
                            Selected add page unavailable is unavailable at the tenant
                        % else:
                            % if not offline_mode:
                                Loading...
                                <script type="text/javascript">
                                    var reloadTimeout = setTimeout(function() {
                                        location.reload()
                                      }, 2000);
                                </script>
                            % else:
                                Data unavailable
                            % end
                        % end
                        </span>
                    </div>
                </div>
                % end
            % else:
                <div class="row h-100">
                    <span>
                      % if no_data:
                        No data. Please upload a CSV file.
                      % else:
                        No search results
                      % end
                    </span>
                </div>
            % end

    </body>
</html>
