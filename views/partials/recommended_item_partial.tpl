<table class="table bg-light recommendation">
  <thead>
    <tr>
      <th>
      <span class="text">
          % if recommendation.loaded is True:
          {{recommendation.title}}
          % else:
          Loading...
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
        % else:
          Loading...
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
            % else:
                Loading...
            % end

        </span>
      </td>
    </tr>
    <tr>
      <td>
          % if recommendation.loaded is True:
            <img width="100%" height="250px" src="{{recommendation.img_url}}" />
          % else:
            <span>Loading...</span>
          % end

      </td>
    </tr>
    <tr>
        <td>
            % if recommendation.expired:
                <span class="alert alert-danger d-inline-block w-100 text m-0">Expired</span>
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