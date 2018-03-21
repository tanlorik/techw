function changeContent () {
    var items=[
    {name:"Vivo", info:"Quality Burgers", category:"Location"},
    {name:"CHouse", info:"Italian Food", category:"Location"},
    {name:"Mercedesa ", info:"Cocalar in timpul liber", category:"Person"}
]
var content = document.getElementById("content");
var itemListHtml='';
for(var item of items){
    itemListHtml+=
    `
    
    <div class="item">&nbsp</div>
    <div class="info nomargintext">
        <h3>Name: ${item.name}</h3>
        <p>Info: ${item.info}</p>
        <p>Category: ${item.category}</p>
    </div>
    <div class="buttons">
        <div class ="col span_1_of_12">
            &nbsp
        </div>
        <div class ="col span_2_of_12">
            <button>feedback</button>
        </div>
        <div class ="col span_1_of_12">
            &nbsp
        </div>
        <div class ="col span_2_of_12">
            <button>rate</button>
        </div>
        <div class ="col span_3_of_12">
            &nbsp
        </div>
        <div class=" col span_2_of_12">
            <button>statistics</button>
        </div>
    </div>
    
    `
}
content.innerHTML= itemListHtml;
}

window.onload = changeContent ;


