
<html>
    <head>
        <meta charset="utf-8" />
        <title>Main try</title>
        <script type="text/javascript" src="/js/jquery-3.3.1.min.js"></script>
        <link href="/css/bootstrap.css" rel="stylesheet">
        <style type="text/css">
            .pre-scrollable {
                max-height: 740px;
            }
            .container {
                max-width: 100%;
            }
        </style>
        <script type="text/javascript">
            $('#uploadModal').on('shown.bs.modal', function () {
                $('#uploadModal').trigger('focus')
            })
            function changeAmountPerPage(val){
                $.ajax({url: "_amount_per_page/"+val, success: function(data){ location.reload();}});
            }
        </script>
    </head>
    <body>

        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary active">Overview</a>
                    <a href="/upload" role="button" class="btn btn-sm btn-secondary">Upload</a>
                    <!-- <button type="button" class="btn btn-sm btn-secondary" data-toggle="modal" data-target="#uploadModal">Upload</button> -->
                    <span>current tenant: {{tenant}}</span>
                </div>
                <div class="col-3">
                 <div class="collapse show" id="search_box">
                    <input type="text"
                    % if no_data is True:
                        disabled
                    % end
                    class="form-control form-control-sm collapse show" placeholder="not yet working search" id="search" value="{{search_string}}" />
                 </div>
                 <div class="collapse hide" id="search_wait">
                    <div class="progress">
                      <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 50%"></div>
                    </div>
                 </div>
                </div>
            </div>
            % if no_data is False and no_search_data is False:
                <div class="row h-100">
                  <div class="col-2 h-100 d-inline-block">

                    <div class="row bg-light">

                      <div class="col p-0">

                        <nav aria-label="Pagination">
                          <ul class="pagination pagination-sm justify-content-center mb-1">
                            <li class="page-item
                                % if current_page is 0:
                                    disabled
                                % end
                            ">
                              <a class="page-link" href="/_page/{{current_page-1}}" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                                <span class="sr-only">Previous</span>
                              </a>
                            </li>
                            % for page in page_bar:
                                <li class="page-item
                                % if current_page is page:
                                    active
                                %end
                                "><a class="page-link" href="/_page/{{page}}">{{page}}</a></li>
                            % end
                            <li class="page-item
                                % if current_page is max(page_bar):
                                    disabled
                                % end
                            ">
                              <a class="page-link" href="/_page/{{current_page+1}}" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                                <span class="sr-only">Next</span>
                              </a>
                            </li>
                          </ul>
                        </nav>
                        <span class="text-center d-block mb-1">showing
                            <select name="storeID" onchange='changeAmountPerPage(this.value)'>
                                % for amount in selectable_page_amounts:
                                    <option value="{{amount}}"
                                    % if amount is max_per_page:
                                        selected
                                    % end
                                    >{{amount}}</option>

                                % end
                            </select>
                            per page.
                        </span>

                      </div>
                    </div>
                    <div class="row">
                      <div class="col p-0 pre-scrollable">
                         <div class="list-group">
                            <small id="item_list">

                              % for item in item_list:
                                <a href="/_open_item/{{item}}" class="list-group-item list-group-item-action list-group-item-secondary p-2
                                % if selected_item == item:
                                    active
                                % end
                                ">{{item}}</a>
                              % end
                            </small>
                          </div>
                      </div>
                    </div>


                  </div>
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

                      <div class="col-3 bg-light border-right" id="selected_item">
                        <table class="table">
                            <thead>
                              <tr>
                                <td>{{selected_item_pane_title}}</td>
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                <td>
                                  <a href="{{selected_item_pane_url}}">{{selected_item_pane_id}}</a>
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <img width="100%" height="100%" src="{{selected_item_pane_img_url}}" />
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <span>{{selected_item_pane_price}}</span>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                      </div>
                      <div class="col-8 pre-scrollable" id="related_items">

                      % for index, recommendation in enumerate(recommendations):
                        % if not index%3:
                            <div class="row">
                        % end

                        <div class="col-4 p-1">
                            % if recommendation.loaded is True:
                            <table class="table bg-light">
                              <thead>
                                <tr>
                                  <td>{{recommendation.title}}</td>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td style="background-color:hsl({{(1-recommendation.score)*150}},100%,50%)">
                                    <span class="w-100">{{recommendation.score}}
                                    &nbsp; ({{recommendation.rank}})
                                    </span>
                                  </td>
                                </tr>
                                <tr>
                                  <td>
                                    <a href="{{recommendation.url}}">{{recommendation.id}}</a>
                                  </td>
                                </tr>

                                <tr>
                                  <td>
                                    <img width="100%" height="100%" src="{{recommendation.img_url}}" />
                                  </td>
                                </tr>
                                <tr>
                                  <td>
                                    <span>{{recommendation.price}}</span>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                            % else:
                            <table class="table bg-light">
                                <thead>
                                    <span>Loading...</span>
                                </thead>
                                <tbody>
                                <tr>
                                  <td style="background-color:hsl({{(1-recommendation.score)*150}},100%,50%)">
                                    <span class="w-100">Score: {{recommendation.score}}
                                    &nbsp; (Rank: {{recommendation.rank}})
                                    </span>
                                  </td>
                                </tr>
                                <tr>
                                  <td>
                                    <span>{{recommendation.id}}</span>
                                  </td>
                                </tr>
                                <tr>
                                  <td>
                                    <span>Loading...</span>
                                  </td>
                                </tr>
                            </table>
                            % end
                          </div>

                        % if not (index+1)%3:
                            </div>
                        % end
                      % end
                </div>
                % else:
                <div class="row">
                    <div class="col-12 ml-2 pr-0 mt-3">
                        <span class="alert alert-danger d-block mr-5">
                        % if selected_ad_error is True:
                            Selected add page unavailable is unavailable at the tenant
                        % else:
                            Loading...
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


        <!-- Modal -->
        <div class="modal fade" id="uploadModal" tabindex="-1" role="dialog" aria-labelledby="uploadModalLabel" aria-hidden="true">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <form>
                    <input type="text" name="tenant" />
                    <input type="file" name="upload" />
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
              </div>
            </div>
          </div>
        </div>

        <script type="text/javascript">

            var searchTimeout = null;
            $('#search').keyup(function() {
              if (searchTimeout != null) {
                clearTimeout(searchTimeout);
              }
              searchTimeout = setTimeout(function() {
                $('#search_box').hide()
                $('#search_wait').show()
                searchTimeout = null;

                $.ajax({url: "_search/"+$('#search')[0].value, success: function(data){ location.reload();}});
                //ajax code

              }, 500);
            })

        </script>

    </body>
</html>
