spoonacularAPI = "https://api.spoonacular.com/recipes/complexSearch?"
// async function processForm(evt) {
//     evt.preventDefault()
//     let max_protein = $('#max-protein').val();
//     let max_carbs = $('#max-carbs').val();
//     let max_fat = $('#max-fat').val();
//     let cuisine = $('#cuisine').val();
//     let diet = $('#diet').val();
//     let intolerance = $('#intolerance').val();
//     let query = $('#search').val();

//     let resp = await axios.post("/api/get-recipe-results", {
//         max_protein, max_carbs, max_fat, cuisine, diet, intolerance, query
//     })

//     handleResponse(resp)
// }

async function gatherFavData(evt) {
    evt.preventDefault()
    console.log(evt.target)
    if (evt.target.classList.contains("like")){
    if (evt.target.classList.contains("fa-heart-o")){
        evt.target.classList.remove("fa-heart-o")
        evt.target.classList.add("fa-heart")

        const id = evt.target.getAttribute("data-id")
        const title = evt.target.getAttribute("data-title")
        const img_url = evt.target.getAttribute("data-img")
        console.log(id, title, img_url)
        let resp = await axios.post("/api/recipe/favs", {
        id, title, img_url
        })
        console.log(resp)
    }
    else if(evt.target.classList.contains("fa-heart")){
        evt.target.classList.remove("fa-heart")
        evt.target.classList.add("fa-heart-o")

        const id = evt.target.getAttribute("data-id")
        console.log(id)
        let resp = await axios.post("/api/recipe/remove_favs", {
        id
        })
        console.log(resp)
    }
    

    // handleFavResponse(resp)
    }
 
}
async function gatherDelData(evt) {
    evt.preventDefault()
    console.log(evt.target)
    if (evt.target.classList.contains("like")){
        if(evt.target.classList.contains("fa-trash")){

        const id = evt.target.getAttribute("data-id")
        console.log(id)
        let resp = await axios.post("/api/recipe/remove", {
        id
        })
        console.log(resp)
    }
    }
 
}

/** handleResponse: deal with response from the spoonaculare API. */
// make an api call and when retrieve it at the app.py then you

// function handleResponse(resp) {
//     console.log(resp)
//     $("#recipe-results").empty()
//     for (const result of resp.data.results){
//         $("#new-recipe-results").append(`
//         <div class="entry one-fourth">
//         <figure>
//             <img src="${result.image}" alt="" />
//             <figcaption><a href="recipe.html"><i class="icon icon-themeenergy_eye2"></i> <span>View recipe</span></a></figcaption>
//         </figure>
//         <div class="container">
//             <h2><a href="/api/recipe/${result.id}">${result.title}</a></h2> 
//             <div class="actions">
//                 <div>
//                     <div class="difficulty"><i class="ico i-medium"></i><a href="#">medium</a></div>
//                     <div class="likes"><i class="fa fa-heart like" data-id="${result.id}" data-title="${result.title}" data-img="${result.image}></i></div>
//                 </div>
//             </div>
//         </div>
//         </div>`)
//     }
    
// }

// function handleFavResponse(resp) {
//     $()
// }


// $(".cuisine-form").on("submit", processForm);
// $(".search-form").on("submit", processForm);
$(".recipe-results").click(gatherFavData)
$(".actions").click(gatherDelData)
// document.getElementById('#recipe-results').addEventListener("click", gatherFavData);


