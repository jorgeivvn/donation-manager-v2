
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
  let itemRequestDomId = event.target.id
  let currentItemReq = event.target.parentNode
  // Grab text of name and desc and their span nodes and set them to variables:
  let currentName = event.target.parentNode.getElementsByClassName('itemName')[0]
  let currentDesc = event.target.parentNode.getElementsByClassName('itemDesc')[0]
  let currentNameText = currentName.innerHTML
  let currentDescText = currentDesc.innerHTML
  // Create new input field for name:
  let editNameField = document.createElement("input");
  editNameField.type = "text";
  editNameField.className = "itemNameInput"
  editNameField.value = currentNameText
  // Create new input field for desc:
  let editDescField = document.createElement("input")
  editDescField.type = "text";
  editDescField.className = "itemDescInput"
  editDescField.value = currentDescText
  // Replace text fields with input fields:
  currentItemReq.replaceChild(editNameField, currentName)
  currentItemReq.replaceChild(editDescField, currentDesc)
  //Replace edit button with save button:
  let currentButton = event.target
  let saveButton = document.createElement("button")
  saveButton.innerHTML = "Save Changes"
  saveButton.className = "saveItemReqButton"
  saveButton.id = itemRequestDomId
  currentItemReq.replaceChild(saveButton, currentButton)
  // add event listener to new save button
  $('#' + itemRequestDomId).on('click', (event) => {
    event.preventDefault();
    let itemRequestId = (event.target.id).split('-')[1]
    let itemRequestDomId = event.target.id
    let currentItemReq = event.target.parentNode
    let updatedNameInput = event.target.parentNode.getElementsByClassName('itemNameInput')[0]
    let updatedDescInput = event.target.parentNode.getElementsByClassName('itemDescInput')[0]
    let updatedNameText = updatedNameInput.value
    let updatedDescText = updatedDescInput.value
    let saveButton = event.target
    console.log(updatedNameText)
    console.log(updatedDescText)
    $.ajax({
      url: '/update_item_request/',
      method: 'GET',
      data: {
        item_request_id: itemRequestId,
        updatedName: updatedNameText,
        updatedDesc: updatedDescText
      },
      success: (res) => {
        let updatedNameSpan = document.createElement("span")
        updatedNameSpan.innerHTML = res.name
        updatedNameSpan.className = "itemName"
        let updatedDescSpan = document.createElement("span")
        updatedDescSpan.innerHTML = res.Name
        updatedNameSpan.className = "itemDesc"
        currentItemReq.replaceChild(updatedNameSpan, updatedNameInput)
        currentItemReq.replaceChild(updatedDescSpan, updatedDescInput)
        let editButton = document.createElement("button")
        editButton.innerHTML = "Edit Item"
        editButton.className = "editItemReqButton"
        editButton.id = itemRequestDomId
        currentItemReq.replaceChild(editButton, saveButton)
      },
      error: () => {
        console.log(' error doing update')
      }
    })
  })
})
