// This is the js for the default/index.html view.


var app = function() {

  var self = {};

  Vue.config.silent = false; // show all warnings

  // Extends an array
  self.extend = function(a, b) {
    for (var i = 0; i < b.length; i++) {
      a.push(b[i]);
    }
  };

  function get_tracks_url(start_idx, end_idx, search) {
    var pp = {
      start_idx: start_idx,
      end_idx: end_idx,
      search: search,
    };
    return "/InstaFab/default/get_posts" + "?" + $.param(pp);
  }



  self.get_posts = function() {
    $.getJSON(get_tracks_url(0, 15, self.vue.search), function(data) {
      self.vue.posts = data.posts;
      self.vue.has_more = data.has_more;
      self.vue.logged_in = data.logged_in;
      self.vue.user = data.user;
    })
  };

  // Complete as needed.
  self.vue = new Vue({
    el: "#vue-div",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
      search: "",
      posts: [],
      logged_in: false,
      has_more: false,
      user: null
    },
    methods: {

    },
    computed: {
      filteredPosts() {
        return this.posts.filter(post => {
          fields = post.Tags;
          tokens = this.search.split("#").filter(token => token !=
            "");
          if (tokens.length > 0) {
            recent = tokens[tokens.length - 1];
            console.log(tokens);
            prediction = false;
            fields.forEach(function(element) {
              if (element.includes(recent)) {
                prediction = true;

              }
            });
            console.log("prediction:" + prediction);
            if (tokens.length == 1) {
              return prediction || tokens.includes(post.PostedBy);
            } else {
              matches = 0;
              tokens.forEach(function(elem) {
                if (fields.includes(elem)) {
                  matches++;
                }
              });
              console.log(matches);
              console.log(tokens.length)
            }
            return (matches == tokens.length - 1 && prediction) ||
              (
                matches == tokens.length) || tokens.includes(post.PostedBy);

            //return fields.includes(tokens)
            //post.Tags.includes(tokens)
          } else {
            return true;
          }
        })
      }
    }

  });

  self.get_posts();
  $("#vue-div").show();
  return self;

};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function() {
  APP = app();
});
