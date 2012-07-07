$(function() {
	$('.order-book-form-render').live("click", function(event){
		var button = $(this);
		var orderContainer = button.parents('.order-book-form-container');

		var postData = {
			book_id: button.attr('data-book-id'),
			csrfmiddlewaretoken: csrfTocken
		};

		$.post(orderBookFormUrl, postData, function(data) {
			orderContainer.html(data);
		});

		return false;
	});

	$('.order-book-make').live("click", function(event){
		var phoneInput = $('#phone_id');
		if (!phoneInput.val().length){
			alert('Укажите контактный телефон');
			return false;
		}

		var button = $(this);
		var orderForm = button.parents('.order-book-form');
		var orderContainer = button.parents('.order-book-form-container');

		var postData = orderForm.serialize();
		postData.csrfmiddlewaretoken = csrfTocken;

		$.post(orderBookMakeUrl, postData, function(data){
			orderContainer.html(data);
		});

		return false;
	});

	$('.order-book-cancel').live("click", function(event){
		var button = $(this);
		var orderContainer = button.parents('.order-book-form-container');

		var postData = {
			order_id: button.attr('data-order-id'),
			csrfmiddlewaretoken: csrfTocken
		};

		$.post(orderBookCancelUrl, postData, function(data){
			orderContainer.html(data);
		});

		return false;
	});
})