document.addEventListener('DOMContentLoaded', () => {
  const mobileMenuButton = document.getElementById('mobile-menu-button')
  const mobileMenu = document.getElementById('mobile-menu')
  const header = document.querySelector('header') // To add/remove the 'menu-open' class

  if (mobileMenuButton && mobileMenu && header) {
    mobileMenuButton.addEventListener('click', () => {
      const isHidden = mobileMenu.classList.contains('hidden')
      if (isHidden) {
        mobileMenu.classList.remove('hidden')
        header.classList.add('menu-open') // Add class to header for icon toggling
      } else {
        mobileMenu.classList.add('hidden')
        header.classList.remove('menu-open') // Remove class from header
      }
    })

    // Close mobile menu when a link is clicked (optional)
    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden')
        header.classList.remove('menu-open')
      })
    })
  } else {
    console.warn('Mobile menu elements not found in DOM.')
  }
})
