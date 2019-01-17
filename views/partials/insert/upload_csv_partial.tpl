<form action="/upload" method="post" enctype="multipart/form-data">
    <div class="modal-body">
        <div class="form-group">
            <label for="tenant">Tenant</label>
            <select name="tenant" id="tenant" class="form-control" placeholder="Select Tenant">
              % for tenant_item in tenant_list:
                <option value="{{tenant_item}}"
                    % if tenant is tenant_item:
                        selected
                    % end
                >{{tenant_item}}</option>
              % end
            <select>
        </div>
        <div class="form-group">
            <label for="upload">CSV file</label>
            <input type="file" name="upload" id="upload" class="form-control" placeholder="Select file" />
        </div>
        <!--
        <div class="form-group">
            <label for="use_all">Use whole file</label>
            <input type="checkbox" name="use_all" id="use_all" class="form-control" placeholder="Use all"  onchange="document.getElementById('start').disabled = !this.checked;document.getElementById('end').disabled = !this.checked;" />
        </div>
        <div class="form-group">
            <label for="start">Start</label>
            <input type="number" name="start" id="start" class="form-control" placeholder="Start" />
        </div>
        <div class="form-group">
            <label for="end">End</label>
            <input type="number" name="end" id="end" class="form-control" placeholder="End" />
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