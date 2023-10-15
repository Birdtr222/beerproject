<!--페이지네이션 -->
        $(document).ready(function () {
          $("div a").click(function () {
            var t = $(this).html();
          })
          $(".pagination > a").on("click", function () {
            $(".pagination").find("a").removeClass("active");
            $(this).addClass("active")
          })
        })

      function boardlist(page_num) {
          $('#container').empty()
          $.ajax({
              type: "GET",
              url: `/pagelist?page=${page_num}`,
              data: {},
              success: function (response) {
                  let beers = response['all_beers']

                  for (let i = 0; i < beers.length; i++) {
                      let country_sub = beers[i]['국가 소분류']
                      let name = beers[i]['맥주 이름']
                      let degree = beers[i]['도수']
                      let image = beers[i]['이미지']
                      let count = beers[i]['좋아요']

                      let temp_html = `<div class="section-contents">
                                  <img class="section-contents-img" src="${image}" alt="">
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
                  }
              }
          })
      }
