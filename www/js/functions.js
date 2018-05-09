
document.question_count = 1


$("#q1_type").change(function(){

    if($(this).val() != "text")
    {
        nr = parseInt(prompt("Number of options: "));
        $(this).parent().children().last().html("");
        html_data = "";
        for(i=1; i<=nr; i++)
        {
            html_data += '<label for="qdata_' + i + '_name" class="form_label">Option ' + i +':</label>';
            html_data += '<input type="text" name="qdata' + i + '" placeholder="option ' + i + '" id="qdata' + i + '">';
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
            html_data = "";
            for(i=1; i<=nr; i++)
            {
                html_data += '<label for="qdata_' + i + '_name" class="form_label">Option ' + i +':</label>';
                html_data += '<input type="text" name="qdata' + i + '" placeholder="option ' + i + '" id="qdata' + i + '">';
                html_data += '<br />';
            }
    
            $(this).parent().children().last().html(html_data);
        }
        else{
            $(this).parent().children().last().html("");
    
        }
    
    });

});