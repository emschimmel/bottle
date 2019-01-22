<form action="/upload" method="post" enctype="multipart/form-data">
    <div class="modal-body">
        <div class="form-group form-row">
            <label for="tenant" class="col-2">Tenant</label>
            <select name="tenant" id="tenant" class="form-control col-10" placeholder="Select Tenant">
              % for tenant_item in tenant_list:
                <option value="{{tenant_item}}"
                    % if tenant is tenant_item:
                        selected
                    % end
                >{{tenant_item}}</option>
              % end
            <select>
        </div>
        <div class="form-group form-row">
            <label for="upload" class="col-2">CSV file</label>
            <input type="file" name="upload" id="upload" class="form-control col-10" placeholder="Select file" />
        </div>
        <!--
        <div class="form-group form-row">
            <label for="use_all" class="col-2">Use whole file</label>
            <input type="checkbox" name="use_all" id="use_all" class="form-control col-10" placeholder="Use all"  onchange="document.getElementById('start').disabled = !this.checked;document.getElementById('end').disabled = !this.checked;" />
        </div>
        <div class="form-group form-row">
            <label for="start" class="col-2">Start</label>
            <input type="number" name="start" id="start" class="form-control col-10" placeholder="Start" />
        </div>
        <div class="form-group form-row">
            <label for="end" class="col-2">End</label>
            <input type="number" name="end" id="end" class="form-control col-10" placeholder="End" />
        </div>
        -->

    </div>
    <div class="modal-footer">
        <span class="collapse hide" id="waiting">Uploading ...</span>
        <button type="submit" id="upload_button" class="btn btn-primary collapse show">Upload</button>
    </div>
</form>

<script type="text/javascript">
    $('#upload_button').click(function() {
        $('#waiting').show()
        $('#upload_button').hide()
    });
</script>