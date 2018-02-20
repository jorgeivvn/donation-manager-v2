console.log('js is working!')

$('button').on('click', (event) => {
  event.preventDefault();
  let element = $(this);
  let itemRequestId = (event.target.id).split('-')[1]
  let $currentButton = $('#' + event.target.id)
  $.ajax({
    url: '/post_donate/',
    method: 'GET',
    data: {item_request_id: itemRequestId},
    success: (res) => {
      $currentButton.html(res)
    },
    error: () => {
      console.log(' error doing donation')
    }
  })
})
