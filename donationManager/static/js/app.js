
$('.donationButton').on('click', (event) => {
  event.preventDefault();
  let authorizeDonationBox = event.target.parentNode.parentNode.getElementsByClassName('authorizeDonation')[0]
  let cancelDonationButton = event.target.parentNode.parentNode.getElementsByClassName('cancelDonationButton')[0]
  event.target.style.display = "none";
  cancelDonationButton.style.display = null;
  authorizeDonationBox.style.display = null;
  console.log(authorizeDonationBox)
  // let currentItemReq = event.target.parentNode
  // let currentButton = event.target
  // let itemRequestId = (event.target.id).split('-')[1]
  // $.ajax({
  //   url: '/post_donate/',
  //   method: 'GET',
  //   data: {item_request_id: itemRequestId},
  //   success: (res) => {
  //     currentButton.remove()
  //     document.getElementsByClassName('needsFulfilledList')[0].prepend(currentItemReq)
  //     location.reload()
  //   },
  //   error: () => {
  //     console.log(' error doing donation')
  //   }
  // })
})

$('.cancelDonationButton').on('click', (event) => {
  event.preventDefault()
  let donationButton = event.target.parentNode.parentNode.getElementsByClassName('donationButton')[0]
  let authorizeDonationBox = event.target.parentNode.parentNode.getElementsByClassName('authorizeDonation')[0]
  event.target.style.display = "none";
  authorizeDonationBox.style.display = "none";
  donationButton.style.display = null;
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

$('.editReliefEffortDetailsButton').on('click', (event) => {
  // make cancel edit button visible and hide edit button
  event.target.parentNode.childNodes[9].style.display = null;
  event.target.style.display = "none";
  // make edit form appear on page
  let updateForm = event.target.parentNode.childNodes[11]
  updateForm.style.display = null;
  console.log(event.target.parentNode.childNodes)
})

$('.cancelEditReliefEffortDetailsButton').on('click', (event) => {
  console.log(event.target.parentNode.childNodes)
  let currentName = event.target.parentNode.getElementsByClassName('reliefEffortName')[0];
  let currentDesc = event.target.parentNode.getElementsByClassName('reliefEffortDesc')[0];
  let currentLocation = event.target.parentNode.getElementsByClassName('reliefEffortLocation')[0];
  let editButton = event.target.parentNode.getElementsByClassName('editReliefEffortDetailsButton')[0];
  let nameInputBox = event.target.parentNode.getElementsByClassName('id_name')[0];
  let descInputBox = event.target.parentNode.getElementsByClassName('id_desc')[0];
  let locationInputBox = event.target.parentNode.getElementsByClassName('id_location')[0];
  nameInputBox.value = currentName.innerHTML;
  descInputBox.value = currentDesc.innerHTML;
  locationInputBox.value = currentLocation.innerHTML;
  let updateForm = event.target.parentNode.childNodes[11]
  event.target.parentNode.childNodes[7].style.display = null;
  event.target.style.display = 'none';
  updateForm.style.display = 'none';
})
