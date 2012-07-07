function _getBookPostData(book) {
	// Информация о книге для читать\не читать
	return {
		book_id: book.attr('data-book-id'),
		csrfmiddlewaretoken: csrfTocken
	};
}

function sendBookReadData(url, data, parent){
	$.post(url, data, function(data) {
		console.debug('response data ', data);
		parent.html(data);
	});
}

$(function() {
	$('.bookmark-add-btn').live("click", function(event){
		var button = $(this);
		var parent = button.parents('.read-book');
		var postData = _getBookPostData(button);

		sendBookReadData(bookmarkAddUrl, postData, parent);

		return false;
	});

	$('.bookmark-del-btn').live("click", function(event){
		var button = $(this);
		var parent = $(this).parents('.read-book');
		var postData = _getBookPostData(button);

		sendBookReadData(bookmarkDelUrl, postData, parent);

		return false;
	});

	$('.book-bookmark-del-than-remove-row').live("click", function(event){
		var button = $(this);
		var parent = $(this).parents('.book-row');
		var postData = _getBookPostData(button);

		$.post(bookmarkDelUrl, postData, function(data) {
			console.debug('response data ', data);
			parent.remove();
		});

		return false;
	});

	$('.bookmark-del-all').live("click", function(event){
		if (!confirm("Очистить все закладки?"))
			return false;

		$('.pager').remove(); // Пагинатор
		$('.bookmark-control-btn').remove(); // Кнопки управления закладкками
		$('.book-row').each(function(index){ $(this).remove(); }); // Строки с закладками
		$('.book-list').html('<h3 align="center">Закладки удалены</h3>');

		// Отправляем путой POST запрос
		$.post(bookmarkDelAllUrl, {csrfmiddlewaretoken: csrfTocken}, function(data) {
			console.debug('response data ', data);
		});

		return false;
	});
})