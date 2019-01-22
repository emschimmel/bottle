<table class="table bg-light border recommendation">
  <thead>
    <tr>
      <th>
      <span class="text">
          % if recommendation.loaded is True:
            {{recommendation.title}}
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
        % if recommendation.loaded is True:
          Categories: {{" > ".join(recommendation.categories)}}
        % elif not offline_mode:
          Loading...
        % else:
          &nbsp;
        % end
        </span>
      </td>
    </tr>
    <tr>
      <td style="background-color:hsl({{(1-float(recommendation.score))*150}},100%,50%)">
        <span class="w-100">{{recommendation.score}}
        &nbsp; ({{recommendation.rank}})
        </span>
      </td>
    </tr>
    <tr>
      <td>
          % if recommendation.loaded is True:
              <a href="{{recommendation.url}}">{{recommendation.id}}</a>
          % else:
              <span>{{recommendation.id}}</span>
          % end
      </td>
    </tr>
    <tr>
      <td>
        <span>
            % if recommendation.loaded is True:
                price: {{recommendation.price}}
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
          % if recommendation.loaded is True or offline_mode:
            <img width="100%" height="250px" src="{{recommendation.img_url}}" />
          % elif not offline_mode:
            Loading...
          % end
      </td>
    </tr>
    <tr>
      <td>
        <span>
            % if recommendation.loaded is True:
                location: {{recommendation.location}}
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
            % if recommendation.expired:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Expired</span>
            % elif recommendation.error:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Unavailable (404)</span>
            % elif recommendation.loaded is False and not offline_mode:
                <span class="alert alert-info d-inline-block w-100 text m-0">Loading</span>
            % elif recommendation.loaded is False and offline_mode:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Data unavailable</span>
            % else:
                <span class="text"> &nbsp;</span>
            % end
        </td>
    </tr>
    <tr>
        <td>
            <small>Collected at: {{recommendation.get_enriched_moment()}}</small>
        </td>
      </tr>
  </tbody>
</table>