
$('.donationButton').on('click', (event) => {
  event.preventDefault();
  let currentItemReq = event.target.parentNode
  let currentButton = event.target
  let itemRequestId = (event.target.id).split('-')[1]
  $.ajax({
    url: '/post_donate/',
    method: 'GET',
    data: {item_request_id: itemRequestId},
    success: (res) => {
      currentButton.remove()
      document.getElementsByClassName('needsFulfilledList')[0].prepend(currentItemReq)
    },
    error: () => {
      console.log(' error doing donation')
    }
  })
})

$('.deleteButton').on('click', (event) => {
  event.preventDefault();
  console.log('delete button was clicked!')
  let currentItemReq = event.target.parentNode
  let itemRequestId = (event.target.id).split('-')[1]
  $.ajax({
    url: '/remove_item_request/',
    method: 'GET',
    data: {item_request_id: itemRequestId},
    success: (res) => {
      currentItemReq.remove()
    },
    error: () => {
      console.log('error deleting item request')
    }
  })
})

$('.editItemReqButton').on('click', (event) => {
  event.preventDefault();
  event.target.parentNode.childNodes[9].style.display = null;
  event.target.style.display = 'none';
  let currentItemReq = event.target.parentNode.parentNode
  let updateForm = currentItemReq.childNodes[3]
  updateForm.style.display = null;
  updateForm.style.border = '2px solid green';
  updateForm.style.width = '300px';
  updateForm.style.padding = '5px';
})

$('.cancelEditItemReqButton').on('click', (event) => {
  event.preventDefault();
  let currentName = event.target.parentNode.getElementsByClassName('itemName')[0];
  let currentDesc = event.target.parentNode.getElementsByClassName('itemDesc')[0];
  let editButton = event.target.parentNode.getElementsByClassName('editItemReqButton')[0];
  let nameInputBox = event.target.parentNode.parentNode.getElementsByClassName('id_name')[0];
  let descInputBox = event.target.parentNode.parentNode.getElementsByClassName('id_desc')[0];
  nameInputBox.value = currentName.innerHTML;
  descInputBox.value = currentDesc.innerHTML;
  let updateForm = event.target.parentNode.parentNode.childNodes[3];
  updateForm.style.display = 'none';
  updateForm.style.border = null;
  updateForm.style.width = null;
  updateForm.style.padding = null;
  event.target.style.display = 'none';
  editButton.style.display = null;
})
