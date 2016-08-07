/**
 * app specific scripts
 */

$(document).ready(function () {


  /**
   * Tabs
   */

  // Add hash to URL on tab-click
  $('a[data-toggle="tab"]').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
    if(history.pushState) {
      history.pushState(null, null, $(this).attr('data-target'));
    }
    else {
        location.hash = $(this).attr('data-target');
    }
  });

  // show active tab on reload
  if (location.hash !== '') $('a[data-target="' + location.hash + '"]').tab('show');

  // Go-to tab with hash
  window.addEventListener("popstate", function (e) {
    var activeTab = $('a[data-target=' + location.hash + ']');
    if (activeTab.length) {
      activeTab.tab('show');
    } else {
      $('.nav-tabs a:first').tab('show');
    }
  });

  /**
   * Datatables
   */

  // Re-adjust responsive datatables on tab change
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    $($.fn.dataTable.tables(true)).DataTable()
      .columns.adjust()
      .responsive.recalc();
  });

  /**
   * Datepicker
   */

  $('input.date').datepicker({
    todayBtn: "linked",
    autoclose: true,
    todayHighlight: true
  });

  /**
   * PSA
   */

  $('.contract form').on('submit', function (e) {
    var sub = $(this).find('#form-submission');
    sub.find('input[type="submit"]').remove();
    sub.append('<p>Processing...</p>');
  });

}); // doc.ready
