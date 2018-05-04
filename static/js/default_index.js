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

  function get_tracks_url(start_idx, end_idx) {
    var pp = {
      start_idx: start_idx,
      end_idx: end_idx
    };
    return "/InstaFab/default/get_posts" + "?" + $.param(pp);
  }



  self.get_posts = function() {
    $.getJSON(get_tracks_url(0, 15), function(data) {
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
      posts: [],
      logged_in: false,
      has_more: false,
      user: null
    },
    methods: {}

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
