/* 검색 관련 자바스크립트*/
        function search_client() {
          let search_name_give = $('#search_name').val()

          $.ajax({
            type: "GET",
            url: "/api/search",
            data: {search_name_give :search_name_give},
            success: function (response) {
              let searched_beer = response['beer_search']
              console.log(searched_beer)
              console.log(searched_beer.length)

              $('#container').empty()

              for(let i = 0; i < searched_beer.length; i++) {
                let searched_country_sub = searched_beer[i]['국가 소분류']
                let searched_name = searched_beer[i]['맥주 이름']
                let searched_degree = searched_beer[i]['도수']
                let searched_img = searched_beer[i]['이미지']
                let count = searched_beer[i]['좋아요']

                let temp_html = `<div class="section-contents">
                                  <img class="section-contents-img" src="${searched_img}" alt="">
                                  <div class="section-contents-country"><p>${searched_country_sub}</p></div>
                                  <div class="section-contents-name"><p>${searched_name}</p></div>
                                  <div class="section-contents-ABV"><p>${searched_degree}</p></div>
                                  <div class="section-contents-count"><p>${count}</p></div>
                                  <div class="section-contents-like">
                                    <label>
                                        <img class="like" src="static/img/like.png" alt="" width="30px">
                                        <img class="like_hover" src="static/img/like_hover.png" alt="" width="30px">
                                        <button class="section-contents-likeBtn" type="button" onclick="likebeer('${searched_name}')"></button>
                                    </label>
                                  </div>                               
                                 </div>`
                $('#container').append(temp_html)
                $(".pagination").hide();
              }
            }
          })
        }
/* 검색 엔터키 이벤트*/
function enterkey(){
  return search_client();
}

/*검색창 동작 이벤트*/
// function searchToggle(obj, evt){
//     var container = $(obj).closest('.search-wrapper');
//         if(!container.hasClass('active')){
//             container.addClass('active');
//             evt.preventDefault();
//         }
//         else if(container.hasClass('active') && $(obj).closest('.input-holder').length == 0){
//             container.removeClass('active');
//             // clear input
//             container.find('.search-input').val('');
//         }
// }
