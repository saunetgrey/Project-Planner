const editShowDialog = document.getElementById('edit-show-dialog');

if (editShowDialog) {
  editShowDialog.showModal();

  // Escape returns to the list just like the visible Cancel link.
  editShowDialog.addEventListener('cancel', event => {
    event.preventDefault();
    window.location.assign(editShowDialog.dataset.cancelUrl);
  });

  editShowDialog.addEventListener('click', event => {
    const bounds = editShowDialog.getBoundingClientRect();
    if (event.target === editShowDialog &&
        (event.clientX < bounds.left || event.clientX > bounds.right ||
         event.clientY < bounds.top || event.clientY > bounds.bottom)) {
      window.location.assign(editShowDialog.dataset.cancelUrl);
    }
  });
}
