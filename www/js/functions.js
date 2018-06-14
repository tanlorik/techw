
document.question_count = 1


function submit_form(element){
    submit = element.closest('form').find(':submit').val();
    data = element.serialize() + '&sub='+submit;
    url = element.attr('action');
    console.log(url)
    $.post(url, data).done(function(ret){
        console.log(ret);
    });
}

$("#q1_type").change(function(){

    if($(this).val() != "text")
    {
        nr = parseInt(prompt("Number of options: "));
        q = $(this).attr("id");
        const regex = /q([0-9]*)_type/gm;
        id = regex.exec(q)[1];
        console.log(id);
        $(this).parent().children().last().html("");
        html_data = "";
        for(i=1; i<=nr; i++)
        {
            html_data += '<label for="qdata_' + i + '_name" class="form_label">Option ' + i +':</label>';
            html_data += '<input type="text" name="q' + id + 'data' + i + '" placeholder="option ' + i + '" id="q' + id + 'data' + i + '">';
            html_data += '<br />';
        }

        $(this).parent().children().last().html(html_data);
    }
    else{
        $(this).parent().children().last().html("");

    }

});


$("#add_question").click(function(){

    nr = ++document.question_count;

    html_data = '<span id="q' + nr + '_span"><label for="q' + nr + '_name" class="form_label">Question ' + nr + ':</label><input type="text" name="q' + nr + '_name" placeholder="question" id="q' + nr + '_name"> <br /><label for="q' + nr + '_type" class="form_label">Type:</label><select id="q' + nr + '_type" name="q' + nr + '_type" class="question_select"><option value="text">Text</option><option value="select">Select</option><option value="checkbox">Checkbox</option></select><br /><span id="q' + nr + '_data_span"></span></span><hr>';
    $("#add_form").append(html_data);

    $("#q" + nr + "_type").change(function(){

        if($(this).val() != "text")
        {
            nr = parseInt(prompt("Number of options: "));
            $(this).parent().children().last().html("");
            q = $(this).attr("id");
            const regex = /q([0-9]*)_type/gm;
            id = regex.exec(q)[1];
            console.log(id);
            console.log(q)
            html_data = "";
            for(i=1; i<=nr; i++)
            {
                html_data += '<label for="qdata_' + i + '_name" class="form_label">Option ' + i +':</label>';
                html_data += '<input type="text" name="q' + id + 'data' + i + '" placeholder="option ' + i + '" id="q' + id + 'data' + i + '">';
                html_data += '<br />';
            }
    
            $(this).parent().children().last().html(html_data);
        }
        else{
            $(this).parent().children().last().html("");
    
        }
    
    });

});

function prepQuestion(q, iid){

    html = "";
    html += "<p>" + q.name +"</p>";
    q.data = JSON.parse(q.data)

    if(q.qtype == 0){

        html+='<input type=text name="i' + iid + "q" + q.id + '">'

    }else{

        if(q.qtype == 1){

            html+='<select name="i' + iid + "q" + q.id + '">'
            q.data.forEach(function(i){

                html+= '<option value="' + i + '">' + i + '</option>'; 

            });

            html+="</select>";
        }else{
            if(q.qtype == 2){
                k = 0
                q.data.forEach(function(i){
                    console.log(i)
                    html+= '<input type="checkBox" value="' + i + '" id="i' + iid + 'q' + q.id + 'o' + k +'" name="i' + iid + 'q' + q.id + 'o'+ k++ +'"><label for="i' + iid + 'q' + q.id + '">' + i + '</label>' + '<br>'; 
                   
                });
            }
        }
    }
    return html;

}

function getItems()
{
    html = ""
    $.ajax({
         url: "./api/all",

        }).done(function(items){

        items = JSON.parse(items)
        console.log(items);
        console.log(typeof items);

        items.forEach(function(item){
            html+= '<div id="item' + item.id + '"><form action="./api/" method=post id="reply_form'+ item.id + '">' ;
            html+= '<input type="hidden" name="item_id" value="' + item.id + '">'
            html+= '<h1 class="item_title">' + item.name + '</h1><hr>';
            html+= '<img src="' + item.image_link + '"><br>';
            html+= '<p>'+ item.description + '</p><hr>';
            item.question.forEach(function(q){

                html += prepQuestion(q, item.id)
                html+="<hr>"

            });

        html += '<input type="submit" name="sub" class="login loginmodal-submit" value="Vote"></form></div>';

        });

        $("#main_content").html(html);

        items.forEach(function(item){
            console.log("#reply_form" + item.id);
            $("#replyform" + item.id).submit(function(e){
                e.preventDefault();
                submit_form($(this));
            });
        })

    });
}




function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    var user = getCookie("username");
    if (user != "") {
        alert("Welcome again " + user);
    } else {
        user = prompt("Please enter your name:", "");
        if (user != "" && user != null) {
            setCookie("username", user, 365);
        }
    }
}




$(document).ready(function(){

    getItems();/*
    $("form").submit(function(e){
        e.preventDefault();
        submit_form($(this));
    });
*/
    $(document).on("submit", "form", function(e){
        e.preventDefault();
        submit_form($(this))
    })
})