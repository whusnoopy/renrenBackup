$().ready(function() {
  var hotkeySupport = function(e) {
    var e = e || event;
    var k = e.keyCode || e.which || e.charCode; //获取按键代码
    if (k == 37) {
      var prevPage = $(".js-prev-page");
      if (prevPage.length) {
        prevPage[0].click();
      }
    } else if (k == 39) {
      var nextPage = $(".js-next-page");
      if (nextPage.length) {
        nextPage[0].click();
      }
    }
  };

  document.onkeydown = hotkeySupport;
});
