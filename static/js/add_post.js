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
      imageData: null,
      myCrop: null,
      message: null,
      tag: null,

    },
    methods: {
      previewImage: function(event) {
        // Reference to the DOM input element
        var input = event.target;
        var $uploadCrop;
        // Ensure that you have a file before attempting to read it
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          reader.onload = function(e) {
            $uploadCrop.croppie('bind', {
              url: e.target.result
            }).then(function() {
              console.log('jQuery bind complete');
              $uploadCrop.croppie('rotate', 90);
              $uploadCrop.croppie('result', {
                type: 'base64',
                size: 'viewport'
              }).then(function(base64) {
                console.log(base64)
                  //this.imageData = blob;
              });

            });
          }
          reader.readAsDataURL(input.files[0]);
        } else {
          swal(
            "Sorry - you're browser doesn't support the FileReader API"
          );
        }
        $uploadCrop = $('#crop').croppie({
          viewport: {
            width: 200,
            height: 200,
          },
          enableResize: true,
          enableOrientation: true
        });

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
