<div class="row bg-light">

  <div class="col p-0">

    <nav aria-label="Pagination">
      <ul class="pagination pagination-sm center mb-1">
        <li class="page-item
            % if current_page is 0:
                disabled
            % end
        ">
          <a class="page-link" href="/_page/{{current_page-1}}" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
        </li>
        % for page in page_bar:
            <li class="page-item
            % if current_page is page:
                active
            %end
            "><a class="page-link" href="/_page/{{page}}">{{page}}</a></li>
        % end
        <li class="page-item
            % if current_page is max(page_bar):
                disabled
            % end
        ">
          <a class="page-link" href="/_page/{{current_page+1}}" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
        </li>
      </ul>
    </nav>
    <span class="text-center d-block mb-1">showing
        <select name="storeID" onchange='changeAmountPerPage(this.value)'>
            % for amount in selectable_page_amounts:
                <option value="{{amount}}"
                % if amount is max_per_page:
                    selected
                % end
                >{{amount}}</option>

            % end
        </select>
        per page.
    </span>
    <script type="text/javascript">

        // onchange amount adds per page
        function changeAmountPerPage(val){
            $.ajax({url: "_amount_per_page/"+val, success: function(data){ location.reload();}});
        }
    </script>

  </div>
</div>