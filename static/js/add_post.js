var app = function() {

  var self = {};
  //var message = null;
  //var pic = null;
  Vue.config.silent = false; // show all warnings

  // Extends an array
  self.extend = function(a, b) {
    for (var i = 0; i < b.length; i++) {
      a.push(b[i]);
    }
  };

  // Enumerates an array.
  var enumerate = function(v) {
    var k = 0;
    return v.map(function(e) {
      e._idx = k++;
    });
  };

  self.submit = function() {
    // The submit button to add a track has been added.
    $.post(add_track_url, {
        MyMessage: self.vue.form_message,
        Picture: self.vue.form_pic,
      },
      function(data) {
        $.web2py.enableElement($("#add_track_submit"));
        self.vue.tracks.unshift(data.track);
        enumerate(self.vue.tracks);
      });
  };

  self.vue = new Vue({
    el: "#add-div",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
      pic: null,
      message: null
    },
    methods: {

    }

  });

  $("#add-div").show();

  return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function() {
  APP = app();
});
