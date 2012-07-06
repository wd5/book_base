function _getBookPostData(book) {
	// Информация о книге для читать\не читать
	return {
		book_id: book.attr('data-book-id'),
		csrfmiddlewaretoken: csrfTocken
	};
}

$(function() {
	$('.order-book-form-render').live("click", function(event){
		var button = $(this);
		var orderContainer = button.parents('.order-book-form-container');

		var postData = _getBookPostData(button);
		$.post(orderBookRenderFormUrl, postData, function(data) {
			console.debug('response data ', data);
			orderContainer.html(data);
		});

		return false;
	});
	$('.order-book-make').live("click", function(event){
		var button = $(this);
		var orderForm = button.parents('.order-book-form');
		var orderContainer = button.parents('.order-book-form-container');

		var postData = orderForm.serialize();

		$.post(
			orderBookMakeUrl,
			postData,
			function(data){
				orderContainer.html(data);
			}
		);
		return false;
	});
})