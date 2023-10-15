 function filtering(address_name, api_name) {
     $('#container').empty()
          $.ajax({
            type: "GET",
            url: address_name,
            data: {},
            success: function(response){

              value = response[api_name]
              for(let i = 0; i< value.length; i++) {
                let country_sub = value[i]['국가 소분류']
                let name = value[i]['맥주 이름']
                let degree = value[i]['도수']
                let image = value[i]['이미지']
                let count = value[i]['좋아요']
                  console.log(value.length)

                let temp_html = `<div class="section-contents">
                                  <img class="section-contents-img" src=${image} alt="">
                                  <div class="section-contents-country"><p>${country_sub}</p></div>
                                  <div class="section-contents-name"><p>${name}</p></div>
                                  <div class="section-contents-ABV"><p>${degree}</p></div>
                                  <div class="section-contents-count"><p>${count}</p></div>
                                  <div class="section-contents-like">
                                    <label>
                                        <img class="like" src="static/img/like.png" alt="" width="30px">
                                        <img class="like_hover" src="static/img/like_hover.png" alt="" width="30px">
                                        <button class="section-contents-likeBtn" type="button" onclick="likebeer('${name}')"></button>
                                    </label>
                                  </div>
                                 </div>`
                $('#container').append(temp_html)
                $(".pagination").hide();
              }
            }
          })
 }
