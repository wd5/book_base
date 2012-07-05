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
	$('.will-read-btn').live("click", function(event){
		var button = $(this);
		var parent = button.parents('.read-book');
		var postData = _getBookPostData(button);
		var readUrl = bookUrl + postData.book_id + '/will-read/';
		sendBookReadData(readUrl, postData, parent);

		return false;
	});

	$('.unread-btn').live("click", function(event){
		var button = $(this);
		var parent = $(this).parents('.read-book');
		var postData = _getBookPostData(button);
		var readUrl = bookUrl + postData.book_id + '/unread/';

		sendBookReadData(readUrl, postData, parent);

		return false;
	});

	$('.book-unread-than-remove').live("click", function(event){
		var button = $(this);
		var parent = $(this).parents('.book-row');
		var postData = _getBookPostData(button);
		var unReadUrl = bookUrl + postData.book_id + '/unread/';

		$.post(unReadUrl, postData, function(data) {
			console.debug('response data ', data);
			parent.remove();
		});

		return false;
	});
})