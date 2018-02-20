console.log('js is working!')

$('button').on('click', (event) => {
  event.preventDefault();
  let currentItemReq = event.target.parentNode
  let currentButton = event.target
  let itemRequestId = (event.target.id).split('-')[1]
  // let $currentButton = $('#' + event.target.id)
  $.ajax({
    url: '/post_donate/',
    method: 'GET',
    data: {item_request_id: itemRequestId},
    success: (res) => {
      // $currentButton.html(res)
      // $('.needsFulfilledList').append(element.parentNode)
      currentButton.remove()
      document.getElementsByClassName('needsFulfilledList')[0].prepend(currentItemReq)
    },
    error: () => {
      console.log(' error doing donation')
    }
  })
})
