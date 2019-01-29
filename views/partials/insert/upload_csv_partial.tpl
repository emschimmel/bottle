<form action="/upload" method="post" enctype="multipart/form-data">
    <div class="modal-body">
        <div class="form-group form-row">
            <label for="application_mode" class="col-2">Application mode</label>
            <select name="application_mode" id="application_mode" class="form-control col-10" placeholder="Select application mode">
              % for mode in application_modes:
                <option value="{{mode}}"
                % if mode == system_mode:
                    selected
                % end
                >{{mode}}</option>
              % end
            <select>
        </div>
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

        <div class="form-group form-row">
            <label for="use_all" class="col-2">Use whole file</label>
            <input type="checkbox" checked name="use_all" id="use_all" class="form-control col-10" placeholder="Use all" onchange="document.getElementById('start').disabled = this.checked; document.getElementById('end').disabled = this.checked;" />
        </div>
        <div class="form-group form-row">
            <label for="start" class="col-2">Start line number</label>
            <input type="number" disabled name="start" id="start" class="form-control col-10" placeholder="0" />
        </div>
        <div class="form-group form-row">
            <label for="end" class="col-2">End line number</label>
            <input type="number" disabled name="end" id="end" class="form-control col-10" placeholder="1000" />
        </div>

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