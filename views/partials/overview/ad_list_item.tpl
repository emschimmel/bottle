<table class="table bg-light border current_ad">
  <thead>
    <tr>
      <th>
      <span class="text">
          % if current_ad.loaded is True:
            {{current_ad.title}}
          % elif not offline_mode:
            Loading...
          % else:
            &nbsp;
          % end
      </span>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <span class="text">
        % if current_ad.loaded is True:
          Categories: {{" > ".join(current_ad.categories)}}
        % elif not offline_mode:
          Loading...
        % else:
          &nbsp;
        % end
        </span>
      </td>
    </tr>

    <tr>
      <td>
          % if current_ad.loaded is True:
              <a href="{{current_ad.url}}">{{current_ad.id}}</a>
          % else:
              <span>{{current_ad.id}}</span>
          % end
      </td>
    </tr>
    <tr>
      <td>
        <span>
            % if current_ad.loaded is True:
                price: {{current_ad.price}}
            % elif not offline_mode:
                Loading...
            % else:
                &nbsp;
            % end

        </span>
      </td>
    </tr>
    <tr>
      <td>
          % if current_ad.loaded is True or offline_mode:
                <img width="250px" height="200px" src="{{current_ad.img_url}}"
            % if "no_data.png" not in current_ad.img_url:
                 data-toggle="tooltip" data-placement="right" data-html="true" title="<img src='{{current_ad.img_url}}' />"
            % end
                 />
          % elif not offline_mode:
            Loading...
          % end
      </td>
    </tr>
    <tr>
      <td>
          % if current_ad.loaded is True or offline_mode:
            % for index, image in enumerate(current_ad.extra_images):
                % if index == 4:
                    <button id="img_more_{{current_ad.id}}" class="btn btn-sm mt-1 btn-outline-secondary w-100" onclick="showMore('img_more_{{current_ad.id}}', 'img_block_{{current_ad.id}}', 'img_block_{{current_ad.id}}', 'img_less_{{current_ad.id}}')">Show more</button>
                    <div id="img_block_{{current_ad.id}}" class="d-none">
                % end
                <img src="{{image[0]}}" width="62px" height="85px" data-toggle="tooltip" data-placement="right" data-html="true" title="<img src='{{image[1]}}' />" />
                % if index>4 and index == len(current_ad.extra_images)-1:
                    <button id="img_less_{{current_ad.id}}" class="btn btn-sm mt-1 btn-outline-secondary w-100 d-none" onclick="showLess('img_more_{{current_ad.id}}', 'img_block_{{current_ad.id}}', 'img_block_{{current_ad.id}}', 'img_less_{{current_ad.id}}')">Show less</button>
                    </div>
                % end
            % end
            % for i in range(len(current_ad.extra_images), 4):
                <img width="62px" height="85px" src="/static/img/dummy.png" />
            % end
            % if len(current_ad.extra_images)<5:
                <button class="btn-sm mt-1 btn-outline-light w-100" >&nbsp;</button>
            % end

          % elif not offline_mode:
            Loading...
          % end
      </td>
    </tr>
    <tr>
      <td>
        <span>
            % if current_ad.loaded is True:
                location: {{current_ad.location}}
            % elif not offline_mode:
                Loading...
            % else:
                &nbsp;
            % end

        </span>
      </td>
    </tr>
    <tr>
      <td class="p-1">
          % if current_ad.loaded is True or offline_mode:
            <table class="table table-sm small border-1" id="extra_info_block_less_{{current_ad.id}}">
            % for index, data_item in enumerate(current_ad.extra_data):
                % if index == 5:
                <tr>
                    <td class="border-0" colspan="2">
                        <button id="extra_info_more_{{current_ad.id}}" class="btn btn-sm mt-1 btn-outline-secondary w-100" onclick="showMore('extra_info_more_{{current_ad.id}}', 'extra_info_block_more_{{current_ad.id}}', 'extra_info_block_less_{{current_ad.id}}', 'extra_info_less_{{current_ad.id}}')">Show more</button>
                    </td>
                </tr>
                % elif index <5:
                <tr>
                    <td class="border-0"><span>{{data_item[0]}}</td>
                    <td class="border-0">{{data_item[1]}}</span></td>
                </tr>
                % end
            % end
            % for i in range(len(current_ad.extra_data), 5):
                <tr>
                    <td colspan="2" class="border-0">&nbsp;</td>
                </tr>
            % end
            % if len(current_ad.extra_data)<6:
                <tr>
                    <td class="border-0" colspan="2">
                        <button class="btn-sm mt-1 btn-outline-white border-white w-100" >&nbsp;</button>
                    </td>
                </tr>
            % end
            </table>

            <table class="table table-sm small border-1 d-none" id="extra_info_block_more_{{current_ad.id}}">
            % for data_item in current_ad.extra_data:
                <tr>
                    <td class="border-0"><span>{{data_item[0]}}</td>
                    <td class="border-0">{{data_item[1]}}</span></td>
                </tr>
            % end
                <tr>
                    <td colspan="2" class="border-0">
                        <button id="extra_info_less_{{current_ad.id}}" class="btn btn-sm mt-1 btn-outline-secondary w-100" onclick="showLess('extra_info_more_{{current_ad.id}}', 'extra_info_block_more_{{current_ad.id}}', 'extra_info_block_less_{{current_ad.id}}', 'extra_info_less_{{current_ad.id}}')">Show less</button>
                    </td>
                </tr>
            </table>
          % elif not offline_mode:
            Loading...
          % end
      </td>
    </tr>
    <tr>
        <td>
            % if current_ad.expired:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Expired</span>
            % elif current_ad.error:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Unavailable (404)</span>
            % elif current_ad.loaded is False and not offline_mode:
                <span class="alert alert-info d-inline-block w-100 text m-0">Loading</span>
            % elif current_ad.loaded is False and offline_mode:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Data unavailable</span>
            % else:
                <span class="text"> &nbsp;</span>
            % end
        </td>
    </tr>
    <tr>
        <td>
            <small>Collected at: {{current_ad.get_enriched_moment()}}</small>
        </td>
    </tr>
    <tr>
        <td class="d-flex justify-content-center">
            <a href="#" onclick='reload({{current_ad.id}})' role="button" class="btn btn-secondary btn-sm mr-2">Reload</button>
        </td>
    </tr>
  </tbody>
</table>