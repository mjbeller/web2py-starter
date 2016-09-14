/*
http://jsfiddle.net/mjbeller/o080dmd7/32/
http://codepen.io/mjbeller/pen/esLly?editors=1011
*/

jQuery(document).ready(function($) {

    $('.bookmark-btn')
        .click(function() {
            var btn = $(this);

            var ajaxAdd = $(this).data("ajax-add");
            var ajaxDelete = $(this).data("ajax-delete");
            var bookmarkObj = $(this).data("bookmark-obj");
            // var url = window.location.pathname;
            // var context = $(this).data("context");
            // var contextAction = $(this).data("context-action");
            // var contextId = $(this).data("context-id");

            var bookmarkData = {
                bookmark_obj: bookmarkObj,
                // url: url,
                // context: context,
                // context_action: contextAction,
                // context_id: contextId
            }

            if (btn.hasClass("active")) {

                $.ajax({
                    url: ajaxDelete,
                    type: 'POST',
                    data: bookmarkData,
                    success: function( data ) {
                      web2py_component('/' + w2p_app_name + '/bookmark/list.load', 'bookmark_list');
                      btn.removeClass("active");
                    }
                });  // ajax

            } else {

                $.ajax({
                    url: ajaxAdd,
                    type: 'POST',
                    data: bookmarkData,
                    success: function( data ) {
                      web2py_component('/' + w2p_app_name + '/bookmark/list.load', 'bookmark_list');
                      btn.addClass("active");
                    }
                });  // ajax

            }
        });


            // var jqxhr = $.ajax({
            //     url: '/echo/html/',
            //     dataType: 'json',
            //     data:{ id: $('form input').val() }
            // })
            // .success(function(data) {
            //     alert("success"+data);
            // })
            // .error(function(err) {
            //     alert("error"+err);
            // })
            // .complete(function(stuff) {
            //     alert("complete"+stuff);
            // });

});
