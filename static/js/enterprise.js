  const toggleSidebar = document.getElementById('toggleSidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // Open Sidebar
    toggleSidebar.addEventListener('click', () => {
      sidebar.classList.add('show');
      overlay.classList.add('show');
    });

    // Close Sidebar
    closeSidebar.addEventListener('click', () => {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });

    // Close Sidebar by clicking on the overlay
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });

    // Toggle Mini Sidebar (collapsed state)
    sidebar.addEventListener('transitionend', () => {
      if (!sidebar.classList.contains('show') && !sidebar.classList.contains('mini')) {
        sidebar.classList.add('mini');
      } else if (sidebar.classList.contains('show')) {
        sidebar.classList.remove('mini');
      }
    });