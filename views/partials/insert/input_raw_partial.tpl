<form action="/insert_raw" method="post" id="insert_raw">
      <div class="modal-body">
            <div class="form-group form-row">
                <label for="application_mode" class="col-2">Application mode</label>
                <select name="application_mode" id="application_mode" class="form-control col-10" placeholder="Select application mode">
                  % for mode in application_modes:
                    <option value="{{mode}}"
                    % if mode == system_mode:
                        selected
                    % end
                    >{{mode}}</option>
                  % end
                <select>
            </div>
            <div class="form-group form-row">
                <label for="tenant" class="col-2">Tenant</label>
                <select name="tenant" id="tenant" class="form-control col-10" placeholder="Select Tenant">
                  % for tenant_item in tenant_list:
                    <option value="{{tenant_item}}"
                        % if insert_tenant is tenant_item:
                            selected
                        % end
                    >{{tenant_item}}</option>
                  % end
                <select>
            </div>

            <div class="form-group">
                <span name="id" id="id" class="input-group">Raw input</span>

                <textarea  class="form-control" id="input_raw" name="input_raw" aria-describedby="inputRawHelp"></textarea>
                <small id="inputRawWithRecommenderHelp" class="form-text text-muted
                %if system_mode != "ad_recommenders":
                    d-none
                %end
                ">
                    columns: "ad_id,recommended_ad_id,rank,score" example input:<br />
                    <span class="border d-inline-block w-100 p-2 bg-light rounded">
                    102181900,122858750,1,0.6896<br />
                    102447794,166094071,1,0.9552<br />
                    102447794,463382718,2,0.9519<br />
                    102447794,287804816,3,0.9035
                    </span>
                </small>
                <small id="inputRawWithoutRecommenderHelp" class="form-text text-muted
                %if system_mode != "ad_list_mode":
                    d-none
                %end
                ">
                    columns: "ad_id" example input:<br />
                    <span class="border d-inline-block w-100 p-2 bg-light rounded">
                    102181900<br />
                    102447794<br />
                    166094071<br />
                    463382718
                    </span>
                </small>
                <small id="inputRawProductRecommenderHelp" class="form-text text-muted
                %if system_mode != "user_recom_mode":
                    d-none
                %end
                ">
                    columns: "lot_id,auction_id,auction_name,title,interest_group,topcategoryid,topcategory,recommendation_lot_id,recommendation_auction_id,recommendation_auction_name,recommendation_title,recommendation_interest_group,recommendation_topcategoryid,recommendation_topcategory,rating,channel,timestamp" example input:<br />
                    <span class="border d-inline-block w-100 p-2 bg-light rounded">
                    11878611,123,,,,,,,,,,,,,,,0<br />
                    todo...
                    </span>
                </small>
            </div>

            <div class="form-group" id="inputRawUserRecommender">
                <span name="id_user" id="id_user" class="input-group">Raw input</span>

                <textarea  class="form-control" id="input_raw_user" name="input_raw_user" aria-describedby="inputRawHelp"></textarea>

                <small class="form-text text-muted">
                    columns: "user,lot_id,rating,auction_id,number,lot,auction_name,title,interest_group,topcategoryid,topcategory,channel,timestamp" example input:<br />
                    <span class="border d-inline-block w-100 p-2 bg-light rounded">
                    1586903,11878611,1.9,34210,570,,,,,,,0<br />
                    todo...
                    </span>
                </small>
            </div>

      </div>
      <div class="modal-footer">
        <button type="submit" id="insert_button" class="btn btn-primary collapse show">Insert</button>
      </div>

      <script type="text/javascript">
          $("#application_mode").change(function() {
               if ($(this).children(":selected").text() === "ad_recommenders" ) {
                    $("#inputRawWithRecommenderHelp").removeClass("d-none")
                    $("#inputRawWithoutRecommenderHelp").addClass("d-none")
                    $("#inputRawProductRecommenderHelp").addClass("d-none")
                    $("#inputRawUserRecommender").addClass("d-none")
               }
               if ($(this).children(":selected").text() === "ad_list_mode" ) {
                    $("#inputRawWithRecommenderHelp").addClass("d-none")
                    $("#inputRawWithoutRecommenderHelp").removeClass("d-none")
                    $("#inputRawProductRecommenderHelp").addClass("d-none")
                    $("#inputRawUserRecommender").addClass("d-none")

               }
               if ($(this).children(":selected").text() === "user_recom_mode" ) {
                    $("#inputRawWithRecommenderHelp").addClass("d-none")
                    $("#inputRawWithoutRecommenderHelp").addClass("d-none")
                    $("#inputRawProductRecommenderHelp").removeClass("d-none")
                    $("#inputRawUserRecommender").removeClass("d-none")

               }
          });
      </script>
</form>