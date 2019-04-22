<div class="row">
<img width="300px" height="50%" src="{{selected_ad.img_url}}" class="col-3" />
<div class="col-9">
<table class="table">
    <thead>
      <tr>
        <th colspan="2">
            <span class="card-title text m-0">
                {{selected_ad.title}}
            </span>
        </th>
        <th>
          <span class="card-title text m-0">
            <a href="{{selected_ad.url}}">{{selected_ad.id}}</a>
          </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span class="text">Categories: {{" > ".join(selected_ad.categories)}}</span>
        </td>
        <td>
          <span>location: {{selected_ad.location}}</span>
        </td>
        <td>
            <span>price: {{selected_ad.price}}</span>
        </td>
      </tr>

      <tr>
        <td>
          % if selected_ad.expired:
            <span class="alert alert-danger d-inline-block w-100 m-0">Expired</span>
          % end
        </td>

        <td class="d-flex justify-content-center">
            <a href="#" onclick='reload({{selected_ad.id}})' role="button" class="btn btn-secondary btn-sm mr-2">Reload</button>
            % if all_data:
                <a href="/share/{{selected_ad.id}}" role="button" class="btn btn-secondary btn-sm">Share</button>
            % end
        </td>
        <td>
            <small>Collected at: {{selected_ad.get_enriched_moment()}}</small>
        </td>
      </tr>
    </tbody>
</table>
</div>
</div>
<script type="text/javascript">

    // onchange amount adds per page
    function reload(val){
        $.ajax({url: "_reload/"+val, success: function(data){

        location.reload();
        }});
    }
</script>