var kbmanagementcommands = {
    var: {
        "scan_url" :"/api/management/commands/scan_dir/",
        "get_sharepoint_submission_url" :"/api/management/commands/get_sharepoint_submissions/",
        "get_postgis_submission_url" :"/api/management/commands/get_postgis_submissions/",
        "geoserver_queue_cron_job" :"/api/management/commands/excute_geoserver_queue/",
        "itassets_users_sync_cron_job" :"/api/management/commands/excute_itassets_users_sync/",
        "geoserver_queue_sync_job" : "/api/management/commands/excute_geoserver_sync/",
        "run_randomize_password": "/api/management/commands/randomize_password/",
        "geoserver_layer_healthcheck": "/api/management/commands/perform_geoserver_layer_healthcheck/",
        "geoserver_auto_enqueue": "/api/management/commands/geoserver_auto_enqueue/",
    },
    run_scanner: function() {
        $('#scanner-job-response-success').html('');
        $('#scanner-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-scanner').attr('disabled','disabled');
        $('#run-scanner-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.scan_url,
            type: 'POST',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#scanner-job-response-success').html("Completed");
                $('#run-scanner').removeAttr('disabled');
                $('#run-scanner-loader').hide();
            },
            error: function (error) {
                $('#scanner-job-response-error').html("Error running job");
                $('#run-scanner').removeAttr('disabled');
                $('#run-scanner-loader').hide();
            },
        });
    },
    run_randomize_password: function(){
        $('#geoserver-randomize-password-job-response-success').html('');
        $('#geoserver-randomize-password-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-randomize-password').attr('disabled','disabled');
        $('#run-randomize-password-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.run_randomize_password,
            type: 'POST',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#geoserver-randomize-password-job-response-success').html("Completed");
                $('#run-randomize-password').removeAttr('disabled');
                $('#run-randomize-password-loader').hide();
            },
            error: function (error) {
                $('#geoserver-randomize-password-job-response-error').html("Error running job");
                $('#run-randomize-password').removeAttr('disabled');
                $('#run-randomize-password-loader').hide();
            },
        });
    },
    run_postgis_submissions: function() {
        $('#postgis-scanner-job-response-success').html('');
        $('#postgis-scanner-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-postgis-scanner').attr('disabled','disabled');
        $('#run-postgis-scanner-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.get_postgis_submission_url,
            type: 'POST',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#postgis-scanner-job-response-success').html("Completed");
                $('#run-postgis-scanner').removeAttr('disabled');
                $('#run-postgis-scanner-loader').hide();
            },
            error: function (error) {
                $('#postgis-scanner-job-response-error').html("Error running job");
                $('#run-postgis-scanner').removeAttr('disabled');
                $('#run-postgis-scanner-loader').hide();
            },
        });
    },
    run_sharepoint_submissions: function() {
        $('#sharepoint-scanner-job-response-success').html('');
        $('#sharepoint-scanner-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-sharepoint-scanner').attr('disabled','disabled');
        $('#run-sharepoint-scanner-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.get_sharepoint_submission_url,
            type: 'POST',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#sharepoint-scanner-job-response-success').html("Completed");
                $('#run-sharepoint-scanner').removeAttr('disabled');
                $('#run-sharepoint-scanner-loader').hide();
            },
            error: function (error) {
                $('#sharepoint-scanner-job-response-error').html("Error running job");
                $('#run-sharepoint-scanner').removeAttr('disabled');
                $('#run-sharepoint-scanner-loader').hide();
            },
        });
    },
    run_itassets_users_sync_cron_job: function() {
        console.log('here')
        $('#itassets-users-sync-job-response-success').html('');
        $('#itassets-users-sync-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-itassets-users-sync').attr('disabled','disabled');
        $('#run-itassets-users-sync-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.itassets_users_sync_cron_job,
            type: 'POST',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#itassets-users-sync-job-response-success').html("Completed");
                $('#run-itassets-users-sync').removeAttr('disabled');
                $('#run-itassets-users-sync-loader').hide();
            },
            error: function (error) {
                $('#itassets-users-sync-job-response-error').html("Error running job");
                $('#run-itassets-users-sync').removeAttr('disabled');
                $('#run-itassets-users-sync-loader').hide();
            },
        });
    },
    run_geoserver_queue_cron_job: function() {
        console.log('aho2')
        $('#geoserver-queue-job-response-success').html('');
        $('#geoserver-queue-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-geoserver-queue').attr('disabled','disabled');
        $('#run-geoserver-queue-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.geoserver_queue_cron_job,
            type: 'POST',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#geoserver-queue-job-response-success').html("Completed");
                $('#run-geoserver-queue').removeAttr('disabled');
                $('#run-geoserver-queue-loader').hide();
            },
            error: function (error) {
                $('#geoserver-queue-job-response-error').html("Error running job");
                $('#run-geoserver-queue').removeAttr('disabled');
                $('#run-geoserver-queue-loader').hide();
            },
        });
    },
    run_geoserver_layer_healthcheck_job: function(){
        let res_success = $('#geoserver-layer-healthcheck-job-response-success').html('');
        let res_error = $('#geoserver-layer-healthcheck-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        let run_btn = $('#run-geoserver-layer-healthcheck').attr('disabled','disabled');
        let loader = $('#run-geoserver-layer-healthcheck-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.geoserver_layer_healthcheck,
            type: 'POST',
            data: JSON.stringify({}),
            dataType: 'json',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                res_success.html("Completed");
                run_btn.removeAttr('disabled');
                loader.hide();
            },
            error: function (error) {
                text = error?.responseJSON?.detail ?? '' 
                res_error.html("Error running job. " + text);
                run_btn.removeAttr('disabled');
                loader.hide();
            },
        });
    },
    run_geoserver_sync_cron_job: function(items_to_sync) {
        $('#geoserver-sync-' + items_to_sync + '-job-response-success').html('');
        $('#geoserver-sync-' + items_to_sync + '-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        $('#run-geoserver-sync-' + items_to_sync).attr('disabled','disabled');
        $('#run-geoserver-sync-' + items_to_sync + '-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.geoserver_queue_sync_job,
            type: 'POST',
            data: JSON.stringify({'items_to_sync': items_to_sync}),
            dataType: 'json',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                $('#geoserver-sync-' + items_to_sync + '-job-response-success').html("Completed");
                $('#run-geoserver-sync-' + items_to_sync).removeAttr('disabled');
                $('#run-geoserver-sync-' + items_to_sync + '-loader').hide();
            },
            error: function (error) {
                text = error?.responseJSON?.detail ?? '' 
                $('#geoserver-sync-' + items_to_sync + '-job-response-error').html("Error running job. " + text);
                $('#run-geoserver-sync-' + items_to_sync).removeAttr('disabled');
                $('#run-geoserver-sync-' + items_to_sync + '-loader').hide();
            },
        });
    },
    run_geoserver_auto_enqueue_job: function(){
        let res_success = $('#geoserver-auto-enqueue-job-response-success').html('');
        let res_error = $('#geoserver-auto-enqueue-job-response-error').html('');
        var csrf_token = $("#csrfmiddlewaretoken").val();
        let run_btn = $('#run-geoserver-auto-enqueue').attr('disabled','disabled');
        let loader = $('#run-geoserver-auto-enqueue-loader').show();
        $.ajax({
            url: kbmanagementcommands.var.geoserver_auto_enqueue,
            type: 'POST',
            data: JSON.stringify({}),
            dataType: 'json',
            headers: {'X-CSRFToken' : csrf_token},
            contentType: 'application/json',
            success: function (response) {
                res_success.html("Completed");
                run_btn.removeAttr('disabled');
                loader.hide();
            },
            error: function (error) {
                text = error?.responseJSON?.detail ?? '' 
                res_error.html("Error running job. " + text);
                run_btn.removeAttr('disabled');
                loader.hide();
            },
        });
    },
    init: function() {
        console.log('init')
        $( "#run-scanner" ).click(function() {
            kbmanagementcommands.run_scanner();
        });
        $( "#run-sharepoint-scanner" ).click(function() {
            kbmanagementcommands.run_sharepoint_submissions();
        });
        $( "#run-postgis-scanner" ).click(function() {
            kbmanagementcommands.run_postgis_submissions();
        });
        $( "#run-geoserver-queue" ).click(function() {
            kbmanagementcommands.run_geoserver_queue_cron_job();
        });
        $( "#run-itassets-users-sync" ).click(function() {
            kbmanagementcommands.run_itassets_users_sync_cron_job();
        });
        $( "#run-geoserver-sync-layers" ).click(function() {
            kbmanagementcommands.run_geoserver_sync_cron_job('layers');
        });
        $( "#run-geoserver-sync-roles" ).click(function() {
            kbmanagementcommands.run_geoserver_sync_cron_job('roles');
        });
        $( "#run-geoserver-sync-groups" ).click(function() {
            kbmanagementcommands.run_geoserver_sync_cron_job('groups');
        });
        $( "#run-geoserver-sync-rules" ).click(function() {
            kbmanagementcommands.run_geoserver_sync_cron_job('rules');
        });
        $( "#run-geoserver-sync-users" ).click(function() {
            kbmanagementcommands.run_geoserver_sync_cron_job('users');
        });
        $( "#run-geoserver-layer-healthcheck" ).click(function() {
            kbmanagementcommands.run_geoserver_layer_healthcheck_job();
        });
        $( "#run-geoserver-auto-enqueue" ).click(function() {
            kbmanagementcommands.run_geoserver_auto_enqueue_job();
        });
        $( "#run-randomize-password" ).click(function() {
            kbmanagementcommands.run_randomize_password();
        });
        $('#run-scanner-loader').hide();
        $('#run-sharepoint-scanner-loader').hide();
        $('#run-postgis-scanner-loader').hide();
        $('#run-geoserver-queue-loader').hide();
        $('#run-itassets-users-sync-loader').hide();
        $('#run-geoserver-auto-enqueue-loader').hide();
    }
}