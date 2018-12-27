
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
                    <input type="text"
                    % if no_data is True:
                        disabled
                    % end
                    class="form-control form-control-sm" placeholder="not yet working search" value="{{search_string}}" onKeyUp="" />
                </div>
            </div>
            % if no_data is False:
                <div class="row h-100">
                  <div class="col-2 h-100 d-inline-block">

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
                    % if selected_ad_complete is True:

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
                        <span class="alert alert-danger d-block mr-5">Loading...</span>
                    </div>
                </div>
                % end
            % else:
                <div class="row h-100">
                    <span>No data. Please upload a CSV file.</span>
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

    </body>
</html>
