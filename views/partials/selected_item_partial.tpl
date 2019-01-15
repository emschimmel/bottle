<table class="table">
    <thead>
      <tr>
        <th>{{selected_ad.title}}</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span>Categories: {{" > ".join(selected_ad.categories)}}</span>
        </td>
      </tr>
      <tr>
        <td>
          <a href="{{selected_ad.url}}">{{selected_ad.id}}</a>
        </td>
      </tr>
      <tr>
        <td>
          <span>price: {{selected_ad.price}}</span>
        </td>
      </tr>
      <tr>
        <td>
          <img width="100%" height="50%" src="{{selected_ad.img_url}}" />
        </td>
      </tr>
      <tr>
        <td>
            % if selected_ad.expired:
            <span class="alert alert-danger d-inline-block w-100 m-0">Expired</span>
            % end
        </td>
      </tr>
      <tr>
        <td class="d-flex justify-content-center">
            <a href="#" onclick='reload({{selected_ad.id}})' role="button" class="btn btn-secondary btn-sm mr-2">Reload</button>
            <a href="/export/{{selected_ad.id}}" role="button" class="btn btn-secondary btn-sm mr-2">Export</button>
            % if all_data:
            <a href="/share/{{selected_ad.id}}" role="button" class="btn btn-secondary btn-sm">Share</button>
            % end
        </td>
      </tr>

    </tbody>
</table>
    <script type="text/javascript">

        // onchange amount adds per page
        function reload(val){
            $.ajax({url: "_reload/"+val, success: function(data){

            location.reload();
            }});
        }
    </script>