console.log("work fine")

const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function(e) { 
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr('action'),

        dataType: "json",

        success: function (response) {
            console.log("Comment saved to DB...")
            
            if(response.bool == true){
                $(".review-res").html("Review added successfully!")
                $(".hide-comment-form").hide()
                $(".add-rev").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="{% static "assets/imgs/blog/author-2.png" %}" alt="" />'
                    _html += '<br>'
                    _html += '<a href="#" class="font-heading text-brand">' + response.context.user + '</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">{{r.date|date:"d M, Y"}}</span>'
                    _html += '</div>'

                    for(let i = 1; i <= response.context.rating; i++){
                        _html+='<i class="fas fa-star text-warning"></i>'
                    }
                    
                    _html += '</div>'
                    _html += '<p class="mb-10">' + response.context.review + '</p>'

                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'

                    $(".comment-list").prepend(_html)
            }
        }
    })
})


//add to cart functionality
/*$(".add-to-cart-btn").on("click", function () {
    let this_val = $(this)
    let  index = this_val.attr("data-index")

    let quantity = $("#product-quantity").val()
    let product_title = $(".product-title").val()
    let product_id= $(".product-id").val()
    let product_price = $(".current_product-price").text()

    console.log("Quantity:",quantity);
    console.log("Title:",product_title);
    console.log("Price:",product_price);
    console.log("ID:",product_id);
    console.log("Current Element:",this_val);

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id': product_id,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: "json",

        beforeSend: function(){
            console.log("Adding product to cart....");
        },
        success: function (response) {
            this_val.html("Item added to cart!")
            console.log("Added product to cart!");
            $(".cart-items-count").text(response.totalcartitems)
        }
    });
});*/

$(document).ready(function(){
    $(".filter-checkbox").on("click", function(){
        console.log("A button has been clicked!");

        let filter_object = {}

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            //console.log("Filter value is:", filter_value);
            //console.log("Filter key is:", filter_key);
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter object is: ", filter_object ); 
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("Sending data...");
            },
            success: function(response ) {
                console.log(response);
                $("#filtered-product").html(response.data)

            }
        });

        })
    //add to cart functionality
    $(".add-to-cart-btn").on("click", function () {
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id= $(".product-id-" + index).val()
        let product_price = $(".current_product-price-" + index).text()
        let product_pid= $(".product-pid-" + index).val()
        let product_image= $(".product-image-" + index).val()

        console.log("Quantity:",quantity);
        console.log("Title:",product_title);
        console.log("Price:",product_price);
        console.log("ID:",product_id);
        console.log("PID:",product_pid); 
        console.log("Image:",product_image);
        console.log("Index:",index);
        console.log("Current Element:",this_val);

        $.ajax({
          url: '/add-to-cart',
        data:{
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: "json",

        beforeSend: function(){
            console.log("Adding product to cart....");
        },
        success: function (response) {
            this_val.html("✓")
            console.log("Added product to cart!");
            $(".cart-items-count").text(response.totalcartitems)
        }
        });
    })
    // Use event delegation to attach the event to dynamically loaded elements
    $(document).on("click", ".delete-product", function(){
        let p_id = $(this).attr("data-product");
        this_val = $(this);

        console.log("Product ID", p_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": p_id
        },
            dataType: "json",
            beforeSend: function () {
                this_val.hide();  // You can use a spinner or loading animation here
        },
            success: function (response) {
                this_val.show();
            // Update cart items count
                $(".cart-items-count").text(response.totalcartitems);
            // Update the cart list with the new HTML from the server
                $("#cart-list").html(response.data);
        },
        error: function (xhr, status, error) {
                 console.log("Error:", error);
        }
        });
    });
//updte button
    $(document).on("click", ".qty-up", function() {
        let inputField = $(this).closest('.detail-qty').find('.qty-val');
        let currentVal = parseInt(inputField.val());
        if (!isNaN(currentVal)) {
            inputField.val(currentVal + 1);
        }
    });
    
    $(document).on("click", ".qty-down", function() {
        let inputField = $(this).closest('.detail-qty').find('.qty-val');
        let currentVal = parseInt(inputField.val());
        if (!isNaN(currentVal) && currentVal > 1) {
            inputField.val(currentVal - 1);
        }
    });
    

// Event delegation for updating the product quantity
  $(document).on("click", ".update-product", function() {
    let p_id = $(this).attr("data-product");  // Get the product ID
    let this_val = $(this);  // Reference the clicked button
    let product_qty = $(".product-qty-" + p_id).val();  // Get the quantity from the input field with class 'product-qty-{p_id}'

    console.log("Product ID", p_id);
    console.log("Product QTY", product_qty);

    // AJAX request to update cart
    $.ajax({
        url: "/update-cart",  // Update this to your correct URL for updating the cart
        data: {
            "qty": product_qty,
            "id": p_id
        },
        dataType: "json",
        beforeSend: function() {
            this_val.hide();  // Hide the button or show a loading spinner
        },
        success: function(response) {
            this_val.show();  // Show the button again once the update is done
            // Update cart items count
            $(".cart-items-count").text(response.totalcartitems);
            // Update the cart list with the new HTML from the server
            $("#cart-list").html(response.data);
        },
        error: function(xhr, status, error) {
            console.log("Error:", error);
        }
    });
  });

})