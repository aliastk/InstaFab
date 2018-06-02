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
    var file = new File([data], "image.png", {
      'type': 'image/png'
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
          contentType: "image/png",
          processData: false,
          success: self.upload_complete(data.image_path)
        });
      });
  };

  self.upload_complete = function(key) {
    // Hides the uploader div.
    $.getJSON(download, {
      image_path: key
    }, function(data) {
      console.log(data);
      $.getJSON(add, {
        picture: data.get_url,
        MyMessage: self.vue.message,
        Tags: self.vue.tag
      })
    })
    console.log('The file was uploaded; it is now available at ');
  }

  self.rotate = function(degrees) {
    if (!self.vue.cropping) {
      return;
    }
    self.vue.$uploadCrop.rotate(degrees);
  }

  self.save = function() {
    if (!self.vue.cropping) {
      return;
    }
    self.vue.$uploadCrop.getCroppedCanvas().toBlob(self.cleanup,
      "image/png");
    /*.then(
      function(blob) {
        //self.upload_file(blob);
        self.vue.imageData = blob;
        console.log(blob);
        var reader2 = new FileReader();
        reader2.onload = function(f) {
          self.vue.imageUrl = f.target.result;
          console.log(f.target.result);
          self.vue.cropping = false;
          self.vue.$uploadCrop.destroy();
        }
        reader2.readAsDataURL(blob);
        //this.imageData = blob;
      });*/

    return;
  }

  self.cleanup = function(blob) {
    self.vue.imageData = blob;
    console.log(blob);
    var reader2 = new FileReader();
    reader2.onload = function(f) {
      self.vue.imageUrl = f.target.result;
      console.log(f.target.result);
      self.vue.cropping = false;
      self.vue.$uploadCrop.destroy();
    }
    reader2.readAsDataURL(blob);
  }

  self.submit = function() {

    self.upload_file(self.vue.imageData);


  }

  self.edit = function() {
    //https://stackoverflow.com/questions/4069982/document-getelementbyid-vs-jquery
    var image = document.getElementsByTagName('IMG');
    console.log(image[0]);
    self.vue.$uploadCrop = new Cropper(
      image[0], {
        guides: false,
        ready: function() {
          self.vue.cropping = true;
          console.log("attached")
        }
      });
  }

  self.refresh = function() {
    var reader = new FileReader();
    reader.onload = function(e) {
      self.vue.imageUrl = e.target.result;
      self.vue.imageData = self.vue.original;
      self.vue.$uploadCrop.destroy();
      self.vue.cropping = false;
      event.target.value = null;
    }
    reader.readAsDataURL(self.vue.original);
  }

  self.vue = new Vue({
    el: "#add-div",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
      imageData: null,
      original: null,
      myCrop: null,
      message: null,
      tag: null,
      imageUrl: null,
      cropping: false,
      $uploadCrop: null
    },
    methods: {
      previewImage: function(event) {
        // Reference to the DOM input element
        console.log(event);
        var input = event.target;
        // Ensure that you have a file before attempting to read it
        if (input.files && input.files[0]) {
          console.log(input.files[0]);
          var reader = new FileReader();
          if (self.vue.cropping) {
            self.vue.$uploadCrop.destroy();
            self.vue.imageUrl = null;
          }
          reader.onload = function(e) {
            self.vue.imageUrl = e.target.result;
            self.vue.imageData = input.files[0];
            self.vue.cropping = false;
            event.target.value = null;
          }
          reader.readAsDataURL(input.files[0]);
          self.vue.original = input.files[0];
        }
      },
      save: self.save,
      rotate: self.rotate,
      submit: self.submit,
      edit: self.edit,
      refresh: self.refresh
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
