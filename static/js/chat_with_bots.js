document.querySelector('.chat[data-chat=person2]').classList.add('active-chat');
document.querySelector('.person[data-chat=person2]').classList.add('active');

let friends = {
    list: document.querySelector('ul.people'),
    all: document.querySelectorAll('.left .person'),
    name: '',
  },
  chat = {
    container: document.querySelector('.container .right'),
    current: null,
    person: null,
    name: document.querySelector('.container .right .top .name'),
  };

friends.all.forEach((f) => {
  f.addEventListener('mousedown', () => {
    f.classList.contains('active') || setAciveChat(f);
  });
});

function setAciveChat(f) {
  friends.list.querySelector('.active').classList.remove('active');
  f.classList.add('active');
  chat.current = chat.container.querySelector('.active-chat');
  chat.person = f.getAttribute('data-chat');
  chat.current.classList.remove('active-chat');
  chat.container
    .querySelector('[data-chat="' + chat.person + '"]')
    .classList.add('active-chat');
  friends.name = f.querySelector('.name').innerText;
  chat.name.innerHTML = friends.name;
}
$(document).ready(function () {
  var messageMLModel = document.getElementById('message-to-send-ML-model');
  var sendBtnMLModel = document.getElementById('button-send-ML-model');
  sendBtnMLModel.addEventListener('click', function (e) {
    e.preventDefault();
    var chat = $('#message-to-send-ML-model').val();
    $('<li><div class="bubble me">' + chat + '</div></li>').appendTo(
      $('.with_ML_model')
    );
    $('#message-to-send-ML-model').val('');
    $.post('/chat', {
      type: 'post',
      url: '/chat',
      contentType: 'application/json;charset=UTF-8',
      dataType: 'json',
      data: JSON.stringify({ content: chat, with_ML_model: 'true' }),
    }).done(function (q) {
      if (q.status) {
        var chat_res = q.chat_res;
        $('<li><div class="bubble you">' + chat_res + '</div></li>').appendTo(
          $('.with_ML_model')
        );
      }
    });
  });
  messageMLModel.addEventListener('keypress', function(event) {
    if (event.key == 'Enter') {
      event.preventDefault();
      sendBtnMLModel.click();
    }
  });

  var message_nonMLModel = document.getElementById('message-to-send-non-ML-model')
  var sendBtn_nonMLModel = document.getElementById('button-send-non-ML-model');
  sendBtn_nonMLModel.addEventListener('click', function (e) {
    e.preventDefault();
    var chat = $('#message-to-send-non-ML-model').val();
    $('<li><div class="bubble me">' + chat + '</div></li>').appendTo(
      $('.non_ML_model')
    );
    $('#message-to-send-non-ML-model').val('');
    $.post('/chat', {
      type: 'post',
      url: '/chat',
      contentType: 'application/json;charset=UTF-8',
      dataType: 'json',
      data: JSON.stringify({ content: chat, with_ML_model: 'false' }),
    }).done(function (q) {
      if (q.status) {
        var chat_res = q.chat_res;
        $('<li><div class="bubble you">' + chat_res + '</div></li>').appendTo(
          $('.non_ML_model')
        );
      }
    });
  });
  message_nonMLModel.addEventListener('keypress', function(event) {
    if (event.key == 'Enter') {
      event.preventDefault();
      sendBtn_nonMLModel.click();
    }
  });
});
