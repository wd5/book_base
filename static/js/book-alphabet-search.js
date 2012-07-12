$(function(){
	$('.alphabet-container li').click(function(){
		// Редирект на поисковый запрос книг
		window.location.href = bookListUrl + '?' + 'startswith=' + $(this).text();
	});
});