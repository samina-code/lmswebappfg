// Toggle Functions
function toggleNotifications() {
  const popup = document.getElementById('notificationsPopup');
  popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
}

function toggleProfileMenu() {
  const menu = document.getElementById('profileMenu');
  menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

function markAsRead(elem) {
  elem.style.textDecoration = "line-through";
}

function toggleDarkMode() {
  document.body.classList.toggle("dark");
}
