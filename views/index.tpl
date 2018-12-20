
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
                </div>
                <div class="col-3">
                    <input type="text" disabled class="form-control form-control-sm" placeholder="search" />
                </div>
            </div>

            <div class="row h-100">
              <div class="col-2 h-100 d-inline-block">

                <div class="row">
                  <div class="col p-0 pre-scrollable">
                     <div class="list-group">
                        <small id="item_list">

                          % for item in item_list:
                            {{item}}
                          % end
                            <a href="#" class="list-group-item list-group-item-action list-group-item-secondary p-2 active">title (1234)</a>
                            <a href="#" class="list-group-item list-group-item-action list-group-item-secondary p-2">title (2345)</a>
                            <a href="#" class="list-group-item list-group-item-action list-group-item-secondary p-2">title (3456)</a>
                        </small>
                      </div>
                  </div>
                </div>


              </div>
              <div class="col border-1">
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
                            <td>Title</td>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>
                              <a href="#">1234</a>
                            </td>
                          </tr>
                          <tr>
                            <td>
                              <img width="100%" height="100%" src="x.jpg" />
                            </td>
                          </tr>
                          <tr>
                            <td>
                              <span>price</span>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                  </div>
        <!-- marker -->
                  <div class="col-8 pre-scrollable" id="related_items">
                    <div class="row">
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
             <!-- marker -->
                    <div class="row">
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
              <!-- marker -->
                    <div class="row">
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div class="col-4 p-1">
                        <table class="table bg-light">
                          <thead>
                            <tr>
                              <td>Title</td>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <span class="w-100">score (color)
                                &nbsp; (rank)
                                </span>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <a href="#">1234</a>
                              </td>
                            </tr>
                            
                            <tr>
                              <td>
                                <img width="100%" height="100%" src="x.jpg" />
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <span>price</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>


                  </div>
                </div>

              </div>

            </div>
          </div>

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
