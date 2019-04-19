
<html>
    % include('partials/head.tpl')
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-6">
                    <a href="/" role="button" class="btn btn-sm btn-secondary
                    % if all_data:
                        active
                    % end
                    ">Overview</a>
                    % if not offline_mode:
                        <a href="/insert" role="button" class="btn btn-sm btn-secondary">Insert data</a>
                        <a href="/scrape" role="button" class="btn btn-sm btn-secondary">Enrich data</a>
                        <a href="/elastic" role="button" class="btn btn-sm btn-secondary">Export to ES</a>
                    % end
                    <a href="/config" role="button" class="btn btn-sm btn-secondary">Config</a>
                    <span>current tenant: {{tenant}}</span>
                </div>
                % if all_data:
                    <div class="col-3">
                        % include('partials/overview/title_filter_partial.tpl')
                    </div>
                    <div class="col-3">
                        % include('partials/overview/search_partial.tpl')
                    </div>
                % end
            </div>
            % if no_data is False and no_search_data is False:
                % if system_mode == "ad_recommenders":
	                % include('partials/overview/overview_with_recommendations.tpl')
	            % else:
	                % if system_mode == "ad_list_mode":
	                    % include('partials/overview/overview_ad_list.tpl')
	                % else:
	                    % include('partials/overview/overview_with_user_recommendations.tpl')
	                % end
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
