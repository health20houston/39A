//PILGRIM.js
//By Sean Herron
$(document).ready(function(){function t(){var t=e.width();t>1200&&$("div.pilgrim").each(function(){var e=$(this).data("src"),t=$(this).data("alt");$(this).html("<img src='"+e+"' alt='"+t+"'><hr>")});t<1200&&$("div.pilgrim").html("")}var e=$(window);t();$(window).resize(t)});