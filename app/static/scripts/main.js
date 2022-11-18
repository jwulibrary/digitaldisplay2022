// Databases are currently hidden


function adjustCallNumber() {
  var h1 = document.getElementById('book-description').offsetHeight;
  var h2 = document.getElementById('book').offsetHeight;
  var h3 = document.getElementById('book-image').offsetHeight;
  // $('#call-number').css('margin-top', String( (h3- h1) /2)+ 'px')
  var pxToChange = String((h3 - h1) / 2) + 'px';
  document.getElementById('call-number').setAttribute('style', 'margin-top:' + pxToChange)
}
function setDateTime() {
  var d = new Date();
  datestring = d.toLocaleDateString('en-us')
  // $('#datetime').text(datestring)
  document.getElementById('datetime').textContent = datestring;
};
// Get messages from google sheets
var messageList;
function getMessages(libraryName) {
  $.get('/messages/' + libraryName, function(data) {
    window.messageList = data.messages;
  })
};
function selectMessage() {
  curMessage = _.sample(messageList);
  $('#message').fadeOut(2000, function() {
    $(this).text(curMessage).fadeIn(2000);
  })
};
// change slides
function changeSlides() {
  $('.rotating').removeClass('visible').fadeOut('fast');
  $('.rotating').addClass('hidden');
  var selected = $($('.rotating')[_.sample(_.range($('.rotating').length))]);
  selected.fadeIn('slow').addClass('visible').removeClass('hidden');
  _.delay(function() {
    if (document.querySelector('.visible').getAttribute('id') == 'book') {
      adjustCallNumber()
    }
  },
    500)
  };
  function refreshBooks() {
    //endpoints
    var bookData;
    $.get('/books', function(data) {
      bookData = data
    });
    _.delay(function() {
      $('#book-title').text(bookData['title']);
      $('#call-number').text(bookData['call_number']);
      $('#book-description').text(bookData['description']);
      $('#book-image').attr('src', bookData['image']);
       adjustCallNumber();

    }, 1000)
  };
  function refreshDatabases() {
    //endpoints
    var databaseData;
    $.get('/databases', function(data) {
      databaseData = data
    });
    _.delay(function() {
      $('#database-title').text(databaseData['title'])
      $('#database-description').text(databaseData['description'])
      $('#database-image').attr('src', databaseData['image'])
    }, 1000)
  };
  function refreshPosters() {
    //endpoints
    var posterData;
    $.get('/posters', function(data) {
      console.log(data)
      posterData = data
    });
    _.delay(function() {
      $('#poster-img').remove();
      newImg = document.createElement('img');
      newImg.setAttribute('id', 'poster-img')
      newImg.setAttribute('src', posterData)
      $('#poster').append(newImg)
    }, 3000)
  };
  function refreshPosters2() {
    //endpoints
    var posterData;
    $.get('/posters2', function(data) {
      console.log(data)
      posterData = data
    });
    _.delay(function() {
      $('#poster-img2').remove();
      newImg = document.createElement('img');
      newImg.setAttribute('id', 'poster-img2')
      newImg.setAttribute('src', posterData)
      $('#poster2').append(newImg)
    }, 3000)
  };
  function refreshContent() {
    refreshBooks();
    // refreshDatabases();
    refreshPosters();
        refreshPosters2();
  };
  // Init function
  $(document).ready(function() {
    // Run on load
    setDateTime();
    changeSlides();
    getMessages();
    _.delay(function() {
      selectMessage()
    }, 1000);
    // Set regular run
    setInterval(function() {
      changeSlides();
    }, 120000);
    setInterval(function() {
      refreshContent()
    }, 300000);
    setInterval(function() {
      selectMessage();
    }, 30000);
    setInterval(function() {
      setDateTime();
    }, 600000);
  });
