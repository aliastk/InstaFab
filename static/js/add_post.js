var app = function() {

  var self = {};
  var tag = null;
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
      imageData: "",
      message: null,
      tag: null,

    },
    methods: {
      previewImage: function(event) {
        // Reference to the DOM input element
        var input = event.target;
        // Ensure that you have a file before attempting to read it
        if (input.files && input.files[0]) {
          // create a new FileReader to read this image and convert to base64 format
          var reader = new FileReader();
          // Define a callback function to run, when FileReader finishes its job
          reader.onload = (e) => {
              // Note: arrow function used here, so that "this.imageData" refers to the imageData of Vue component
              // Read image as base64 and set to imageData
              this.imageData = e.target.result;
            }
            // Start the reader job - read file as a data url (base64 format)
          reader.readAsDataURL(input.files[0]);
        }
      }
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
