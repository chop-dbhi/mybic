(function($) {
    $(document).ready(function() {
        $('#refresh-project').click(function(e) {
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
    });
})(jQuery);
