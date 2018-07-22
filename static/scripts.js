var showStatusDetail = function (e) {
    var item = $(e.target).closest(".status-item");
    if (item.data('details')) {
        return;
    }
    $.get('/status/' + item.attr('id').split('-')[1], function (res) {
        var likes_html = $("<div>").addClass("status-like");
        $.each(res.likes, function(idx, like) {
            if (idx > 0) {
                likes_html.append($("<span>").text("，"));
            }
            likes_html.append($("<a>").attr('href', 'http://www.renren.com/profile.do?id=' + like.uid).attr('target', '_blank').text(res.users[like.uid].name));
        });
        likes_html.append($("<span>").text(" " + (res.status.like > 8 ? '等 ' : '') + res.status.like + " 人点赞。" + res.status.comment + " 条评论"));

        var popup_html = $("<div>").append(likes_html);
        if (res.status.comment > 0) {
            var comments_html = $("<div>").addClass("ui feed status-comment");
            $.each(res.comments, function(idx, comment) {
                var content = $("<div>").addClass("content");
                var summary = $("<div>").addClass("summary").appendTo(content);
                $("<a>").attr('href', 'http://www.renren.com/profile.do?id=' + comment.authorId).attr('target', '_blank').text(comment.authorName).appendTo(summary);
                $("<div>").addClass("date").text(moment(comment.t).format("YYYY-MM-DD hh:mm:ss")).appendTo(summary);
                $("<div>").addClass("extra text").html(comment.content).appendTo(content);
                $("<div>").addClass("event").append(content).appendTo(comments_html)
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
