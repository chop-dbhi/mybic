(function($) {
    $(document).ready(function() {
        $('#ajax-this-link').click(function(e) {
            e.preventDefault();
            $.ajax({
                url: this.href,
                type: "GET",
                cache: false,
                success: function(data) {
                    console.log(data);
                    location.reload();
                },
                dataType: "json"
            });
        });
        $('#toggle-masquerade').click(function(e) {
            e.preventDefault();
            var toggle_link = this;
            $.ajax({
                url: this.href,
                type: "GET",
                cache: false,
                success: function(data) {
                    console.log(data);
                    if(data.state == true){
                        $( toggle_link ).text("True")
                    }else{
                        $( toggle_link ).text("False")
                    }
                    location.reload();
                },
                dataType: "json"
            });
        });
    });
})(jQuery);
