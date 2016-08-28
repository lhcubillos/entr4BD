var ARROWS = {
  keyboard_arrow_up: "keyboard_arrow_down",
  keyboard_arrow_down: "keyboard_arrow_up",
};

$(document).ready(function(){
  $(".mdl-button.mdl-button--icon.mdl-js-button.mdl-js-ripple-effect.arrow").click(function() {
    var a = $(this).find("i.material-icons");
    var content = a[0].textContent;
    a.replaceWith('<i class="material-icons">'+ARROWS[content]+'</i>');
    var b = $(this).parent().parent().find(".query-card-code").toggle();
  });
});

function onClickQuery(index, db, query) {
  const url = location.href+db+'/'+query;
  window.location.replace(url);
}
