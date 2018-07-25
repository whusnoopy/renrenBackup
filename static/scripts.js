var showComments = function (e, id) {
    var item = $(e.target).closest("div.entry-popover");
    if (item.data('details')) {
        return;
    }
    $.get('/comments/' + id, function (res) {
        var likes_html = $("<div>").addClass("item-like");
        $.each(res.likes, function(idx, like) {
            if (idx > 0) {
                likes_html.append($("<span>").text("，"));
            }
            likes_html.append($("<a>").attr('href', 'http://www.renren.com/profile.do?id=' + like.uid).attr('target', '_blank').text(res.users[like.uid].name));
        });
        likes_html.append($("<span>").text((res.likes.length && " 等人点赞。") + res.comments.length + " 条评论"));

        var popup_html = $("<div>").append(likes_html);
        if (res.comments.length > 0) {
            var comments_html = $("<div>").addClass("ui feed item-comment");
            $.each(res.comments, function(idx, comment) {
                var label = $("<div>").addClass("label");
                var head_img = $("<img>").attr("src", res.users[comment.authorId].headPic);
                $("<a>").attr('href', 'http://www.renren.com/profile.do?id=' + comment.authorId).attr('target', '_blank').append(head_img).appendTo(label);

                var content = $("<div>").addClass("content");
                var summary = $("<div>").addClass("summary").appendTo(content);
                $("<a>").attr('href', 'http://www.renren.com/profile.do?id=' + comment.authorId).attr('target', '_blank').text(comment.authorName).appendTo(summary);
                $("<div>").addClass("date").text(moment(comment.t).format("YYYY-MM-DD hh:mm:ss")).appendTo(summary);
                $("<div>").addClass("extra text").html(comment.content).appendTo(content);

                $("<div>").addClass("event").append(label).append(content).appendTo(comments_html)
            });

            popup_html.append($("<div>").addClass("ui divider")).append(comments_html);
        }

        $(e.target).popup({
            position: 'bottom right',
            on: 'click',
            html: popup_html,
            variation: 'very wide'
        }).popup('show');

        item.data('details', res);
    });
};
