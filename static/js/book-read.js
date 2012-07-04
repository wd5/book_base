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
		var parent = $(this).parent('.read-book');
		var postData = _getBookPostData(button);
		var readUrl = bookUrl + postData.book_id + '/will-read/';
		console.log(parent);
		sendBookReadData(readUrl, postData, parent);

		return false;
	});

	$('.unread-btn').live("click", function(event){
		var button = $(this);
		var parent = $(this).parent('.read-book');
		var postData = _getBookPostData(button);
		var readUrl = bookUrl + postData.book_id + '/unread/';

		sendBookReadData(readUrl, postData, parent);

		return false;
	});
})