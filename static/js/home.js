// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function(name) {
            let ajax_options = {
                type: 'GET',
                url: '/api/anime?anime_name=' + name,
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'post': function(main_name, recomm_name, rating) {
            let ajax_options = {
                type: 'POST',
                url: '/api/anime',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'main_anime_name': main_name,
                    'recomm_anime_name': recomm_name,
                    'rating': rating
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_add_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $anime_name = $('#AnimeName');

    // return the API
    return {
        reset: function() {
            $anime_name.val('').focus();
        },
        update_editor: function(name) {
            $anime_name.val(name).focus();
        },
        build_sections: function(recommended_anime) {
            let rows = '';
            let anime_list = [];
            let alter = 0;

            //document.getElementById("anime_content").style.display = "block";

            // clear the table
            $('.rows').empty();

            // get the output
            anime_list = recommended_anime['output']['animes']

            // did we get a people array?
            if (anime_list) {
                for (let i=0, l=anime_list.length; i < l; i++) {
                    let genres = '';

                    let g = anime_list[i].genre.split(',');

                    for (let j = 0, gl = g.length; j < gl; j++) {
                        genres += `<span class = "genre">${g[j]}</span>`
                    }

                    if (alter == 0) {
                        rows += `
                                <!-- Section -->
                                    <section class="wrapper style1">
                                        <div class="inner">
                                            <!-- 2 Columns -->
                                                <div class="flex flex-2">
                                                    <div class="col col1">
                                                        <div class="image fit">
                                                            <img src="${anime_list[i].img_url}" alt="" />
                                                        </div>
                                                    </div>
                                                    <div class="col col2">
                                                        <h3>${anime_list[i].name}</h3>
                                                        <p class = "synopsis">${anime_list[i].synopsis}</p>
                                                        <p class = "genres">
                                                            ${genres}
                                                        </p>
                                                    </div>
                                                </div>
                                        </div>
                                    </section>
                                `
                        alter = 1;
                    }
                    else {
                        rows += `
                                <!-- Section -->
                                    <section class="wrapper style2">
                                        <div class="inner">
                                            <div class="flex flex-2">
                                                <div class="col col2">
                                                        <h3>${anime_list[i].name}</h3>
                                                        <p class = "synopsis">${anime_list[i].synopsis}</p>
                                                        <p class = "genres">
                                                            ${genres}
                                                        </p>
                                                </div>
                                                <div class="col col1 first">
                                                    <div class="image fit">
                                                        <img src="${anime_list[i].img_url}" alt="" />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </section>
                                `
                        alter = 0;
                    }

                }
                $('.rows').append(rows);
                //document.getElementsByClassName('row')[0].style.display = "block";
                document.getElementById('main').scrollIntoView();
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        },
        events_: function(func_1, func_2) {
            var like_btns = document.querySelectorAll('#like-btn')
            for (var i = 0; i < like_btns.length; i++) {
                var lbtn_ = like_btns[i];
                lbtn_.onclick = func_1;
            }

            var dislike_btns = document.querySelectorAll('#dislike-btn')
            for (var i = 0; i < dislike_btns.length; i++) {
                var dlbtn_ = dislike_btns[i];
                dlbtn_.onclick = func_2;
            }
        },
        response_: function() {

        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $anime_name = $('#AnimeName');

    /*
    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)
    */

    // Validate input
    function validate(name) {
        return name !== "";
    }

    function validate_rating(name_1, name_2, rating) {
        return name_1 !== "" && name_2 !== "" && rating !== "";
    }

    // Create our event handlers
    $('#getSimilar').click(function(e) {
        let anime_name = $anime_name.val();

        e.preventDefault();

        if (validate(anime_name)) {
            model.read(anime_name)
        } else {
            alert('Problem with input data');
        }
    });

    function like_rating() {
        let anime_name = $anime_name.val(),
            recomm_name = $(this).parent().parent().parent()[0].childNodes[1].innerHTML,
            rating = 1;

        recomm_name = recomm_name.substring(13);

        if (validate_rating(anime_name, recomm_name, rating)) {
            model.post(anime_name, recomm_name, rating)
            //console.log(anime_name + recomm_name + rating);
        } else {
            alert('Problem with input data');
        }
    };

    function dislike_rating() {
        let anime_name = $anime_name.val(),
            recomm_name = $(this).parent().parent().parent()[0].childNodes[1].innerHTML,
            rating = 0;

        recomm_name = recomm_name.substring(13);

        if (validate_rating(anime_name, recomm_name, rating)) {
            model.post(anime_name, recomm_name, rating)
            //console.log(anime_name + recomm_name + rating);
        } else {
            alert('Problem with input data');
        }
    };

    /*
    function sample() {
        var name = $(this).parent().parent().parent()[0].childNodes[1].innerHTML;
        name = name.substring(13);

        console.log(name);
    }
    */

    $('#reset').click(function() {
        view.reset();
    });

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target), name;

        name = $target
            .parent()
            .find('td.name')
            .text();

        view.update_editor(name);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_sections(data);
        view.events_(like_rating, dislike_rating);
    });
    $event_pump.on('model_add_success', function(e, data) {
        //console.log(data + " added to the rating dataframe.");
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        window.open("/404", "_self");
    })
}(ns.model, ns.view));
