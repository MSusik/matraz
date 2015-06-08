$( document ).ready(function() {

    var uri = null;
    var repo = null;
    var owner = null;
    var current_message = null;
    var socket = io.connect('http://' + document.domain + ':' + 
                            location.port + '/badge');
    socket.on('info', function(msg) {
        current_message = msg;
        put_info('contact', current_message['contact']);
        put_info('doi', current_message['doi'][0]);
        put_info('license', current_message['license'][0]);
        if(current_message['documentation'])
            put_info('docs', "Available");
        else
            put_info('docs', null);
    });

    var put_info = function(id, content){
        $('.fa-' + id).removeClass('fa-spin fa-spinner fa-check');
        if(content){
            $('.fa-' + id).addClass('fa-check');
            $( "input#" + id ).val(content);
        } else {
            $('.fa-' + id).addClass('fa-remove');
        }
    }

    var reload_triggers = function() {
        $('.fa-2x').removeClass("fa-check fa-remove");
        $('.fa-2x').addClass("fa-spinner fa-spin");
        $("input#contact").val("")
        $("input#doi").val("")
        $("input#license").val("")
        $("input#docs").val("")
        socket.emit('get_info', {
            repo: repo,
            owner: owner,
            refresh: true
        });
    };

    var split_uri = function() {
        uri = window.location.href;
        var parser = document.createElement('a');
        parser.href = uri;
        var repo_and_owner = parser.pathname.split('/');
        owner = repo_and_owner[1];
        repo = repo_and_owner[2];
    }


    $('[data-toggle="tooltip"]').tooltip();

    $('.btn-success').click(function() {
        reload_triggers();
    });

    $('.submit').click(function() {
        reload_triggers();
    });

    split_uri();
    socket.emit('get_info', {
        repo: repo,
        owner: owner
    });

});