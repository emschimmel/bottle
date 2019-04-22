
<div class="row h-100">

  % if all_data:

  <div class="col-2 h-100 d-inline-block">

    <span class="text row">Select a product:</span>
    <div class="row">

      <div class="col p-0 pre-scrollable">
        % include('partials/overview/item_list_partial.tpl')

      </div>
    </div>
    % include('partials/overview/pagination_partial.tpl')

  </div>
  % end

    <div class="col border-1">
    % if selected_ad_complete is True and selected_ad_error is False:

    <div class="row h-100">


      <div class="col-2 bg-light d-block">
        <span class="text row">Select a user:</span>
            <div class="row">

              <div class="col p-0 pre-scrollable">
                % include('partials/overview/item_userlist_partial.tpl')
              </div>
            </div>
      </div>
      <div class="col-10" id="related_items">
      <div class="card">
        <div class="card-body p-0">
        % include('partials/overview/selected_item_horizontal_partial.tpl')
        </div>
        <div class="card-header">
            <span>Product recommendations</span>
        </div>
        <div class="card-body pre-scrollable">
      % for index, recommendation in enumerate(recommendations):
        % if recommendations_limit is not False and index == recommendations_limit:
            <div class="row alert alert-secondary">
                <div class="mx-auto">
                    <a href="/_show_more/{{recommendations_limit + 6}}" class="btn btn-secondary">Show more</a>
                    <a href="/_show_all" class="btn btn-secondary">Show all</a>
                </div>
            </div>
        % elif  recommendations_limit is False or index < recommendations_limit:
            % if not index%3:
                <div class="row">
            % end

            <div class="col-4 p-1">
               % include('partials/overview/recommended_item_partial.tpl')

            </div>

            % if not (index+1)%3:
                </div>
            % end
        % end
      % end
        </div>
        </div>
        <div class="card-header">
            <span>User recommendations</span>
        </div>
        <div class="card-body pre-scrollable">
      % for index, recommendation in enumerate(user_recommendations):
        % if recommendations_limit is not False and index == recommendations_limit:
            <div class="row alert alert-secondary">
                <div class="mx-auto">
                    <a href="/_show_more/{{recommendations_limit + 6}}" class="btn btn-secondary">Show more</a>
                    <a href="/_show_all" class="btn btn-secondary">Show all</a>
                </div>
            </div>
        % elif  recommendations_limit is False or index < recommendations_limit:
            % if not index%3:
                <div class="row">
            % end

            <div class="col-4 p-1">
               % include('partials/overview/recommended_item_partial.tpl')

            </div>

            % if not (index+1)%3:
                </div>
            % end
        % end
      % end
        </div>
        </div>
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
            Selected add is unavailable at the tenant (404)
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