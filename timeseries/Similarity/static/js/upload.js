$(function() {
  $('a#requestTS').bind('click', function() {
    $.getJSON("/search_upload/results", {},
    	function(data) {
      $("#tss").text(data.result);
    });
    return false;
  });
});