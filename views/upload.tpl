<html>
    <head>
        <meta charset="utf-8" />
        <title>upload</title>
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
    </head>
    <body>
        <div class="container m-0">
            <div class="row p-1 bg-info">
                <div class="col-9">
                    <a href="/" role="button" class="btn btn-sm btn-secondary">Overview</a>
                    <a href="/upload" role="button" class="btn btn-sm btn-secondary active">Upload</a>
                    <!-- <button type="button" class="btn btn-sm btn-secondary" data-toggle="modal" data-target="#uploadModal">Upload</button> -->
                </div>
                <div class="col-3">
                    <input type="text" class="form-control form-control-sm" placeholder="search" />
                </div>
            </div>

            <div class="row h-100">
              <div class="col-12 h-100 d-inline-block">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <div>
                      <div class="modal-dialog" role="document">
                        <div class="modal-content">
                          <div class="modal-body">
                            <form>
                                <div class="form-group">
                                    <label for="tenant">Tenant</label>
                                    <select name="tenant" id="tenant" class="form-control" placeholder="Select Tenant">
                                      % for tenant in tenant_list:
                                        <option value="{{tenant}}">{{tenant}}</option>
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

                            </form>
                          </div>
                          <div class="modal-footer">
                            <button type="submit" class="btn btn-primary">Upload</button>
                          </div>
                        </div>
                      </div>
                    </div>
                </form>
              </div>
            </div>
        </div>
    </body>
</html>