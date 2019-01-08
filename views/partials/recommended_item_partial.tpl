<table class="table bg-light recommendation">
  <thead>
    <tr>
      <td>
      <span>
          % if recommendation.loaded is True:
          {{recommendation.title}}
          % else:
          Loading...
          % end
      </span>
      </td>
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
          % if recommendation.loaded is True:
              <a href="{{recommendation.url}}">{{recommendation.id}}</a>
          % else:
              <span>{{recommendation.id}}</span>
          % end
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
        <span>
            % if recommendation.loaded is True:
                {{recommendation.price}}
            % else:
                Loading...
            % end

        </span>
      </td>
    </tr>
  </tbody>
</table>