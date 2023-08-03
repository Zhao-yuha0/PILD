void function () {
  console.clear();
  document.getElementsByClassName('sidebar__menu--item')[0].
  classList.add('is-active');
}();

const menuItems = Array.from(document.querySelectorAll('.sidebar__menu--item'));
menuItems.forEach(item => {
  item.addEventListener('click', e => {
    menuItems.forEach(item => {
      item.classList.remove('is-active');
    });
    e.currentTarget.classList.add('is-active');
  });
});
