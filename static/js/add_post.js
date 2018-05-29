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

  self.upload_file = function(data) {
    // Reads the file.
    var file = new File([data], "image.jpeg", {
      'type': 'image/jpeg'
    });
    console.log(file);
    // First, gets an upload URL.
    console.log("Trying to get the upload url");
    $.getJSON(
      upload,
      function(data) {
        // We now have upload (and download) URLs.
        var put_url = data['signed_url'];
        /*//var get_url = data['access_url'];
        console.log("Received upload url: " + put_url);
        // Uploads the file, using the low-level interface.
        var req = new XMLHttpRequest();
        req.addEventListener("load", self.upload_complete());
        // TODO: if you like, add a listener for "error" to detect failure.
        req.open("PUT", put_url, true);
        req.send(file);*/
        $.ajax({
          type: 'PUT',
          url: put_url,
          data: file,
          contentType: "image/jpeg",
          processData: false,
          success: self.upload_complete()
        });
      });
  };

  self.upload_complete = function() {
    // Hides the uploader div.
    console.log('The file was uploaded; it is now available at ');
  }

  self.vue = new Vue({
    el: "#add-div",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
      imageData: null,
      myCrop: null,
      message: null,
      tag: null,
      image_url: null
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
                type: 'blob',
                format: 'jpeg',
                size: 'viewport'
              }).then(function(blob) {
                self.upload_file(blob);
                console.log(blob);
                //this.imageData = blob;
              });

            });
          }
          reader.readAsDataURL(input.files[0]);
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
