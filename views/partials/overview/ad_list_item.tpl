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
            <img width="250px" height="200px" src="{{current_ad.img_url}}" />
          % elif not offline_mode:
            Loading...
          % end
      </td>
    </tr>
    <tr>
      <td>
          % if current_ad.loaded is True or offline_mode:
            % for image in current_ad.extra_images:
                <img width="50px" height="35px" src="{{image}}" />
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
      <td>
          % if current_ad.loaded is True or offline_mode:
            % for data_item in current_ad.extra_data:
                <span>{{data_item}}</span>
            % end
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
  </tbody>
</table>