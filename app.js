/**
 * app.js
 * Client-side interactive script for Cheongchun Saegyeol Church Digital Bulletin
 */

document.addEventListener('DOMContentLoaded', () => {
  
  /* ==========================================================================
     1. Navigation and Tab Switching (Synchronized between Desktop and Mobile)
     ========================================================================== */
  const mobileNavItems = document.querySelectorAll('.mobile-nav .nav-item');
  const desktopNavTabs = document.querySelectorAll('.desktop-nav .nav-tab');
  const tabContents = document.querySelectorAll('.tab-content');

  function switchTab(tabId) {
    // Scroll to top of window smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Sync mobile navigation items
    mobileNavItems.forEach(item => {
      if (item.getAttribute('data-tab') === tabId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Sync desktop navigation tabs
    desktopNavTabs.forEach(tab => {
      if (tab.getAttribute('data-tab') === tabId) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });

    // Switch tab contents with subtle transition
    tabContents.forEach(content => {
      const contentId = content.id.replace('tab-', '');
      if (contentId === tabId) {
        content.style.display = 'block';
        // Delay adding active class slightly to trigger CSS transition
        setTimeout(() => {
          content.classList.add('active');
        }, 50);
      } else {
        content.classList.remove('active');
        content.style.display = 'none';
      }
    });

    // Recalculate header styling immediately on tab switch
    setTimeout(() => {
      handleHeaderScroll();
    }, 60);
  }

  // Mobile nav click handler
  mobileNavItems.forEach(item => {
    item.addEventListener('click', () => {
      const tabId = item.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // Desktop nav click handler
  desktopNavTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const tabId = tab.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  /* ==========================================================================
     2. Offering Account Number Copy to Clipboard
     ========================================================================== */
  const copyButtons = document.querySelectorAll('.copy-btn');
  const toast = document.getElementById('toast');
  let toastTimeout;

  function showToast(message) {
    if (toast) {
      toast.querySelector('.toast-body').textContent = message;
      toast.classList.add('show');
      
      clearTimeout(toastTimeout);
      toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
      }, 2000);
    }
  }

  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const textToCopy = document.getElementById(targetId).textContent;

      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          showToast('계좌번호가 클립보드에 복사되었습니다.');
        })
        .catch(err => {
          console.error('Failed to copy account number: ', err);
          showToast('계좌번호 복사에 실패했습니다.');
        });
    });
  });

  /* Form logic removed as it has been replaced by the open chat and map */

  /* ==========================================================================
     4. Scroll State and Sticky Header transition
     ========================================================================== */
  const header = document.querySelector('.app-header');

  function handleHeaderScroll() {
    if (!header) return;

    const scrollY = window.scrollY;
    const isMobile = window.innerWidth < 768;
    
    // Find active tab
    const activeTabEl = document.querySelector('.mobile-nav .nav-item.active, .desktop-nav .nav-tab.active');
    const activeTab = activeTabEl ? activeTabEl.getAttribute('data-tab') : 'worship';
    
    if (isMobile) {
      if (scrollY > 20) {
        // Scrolled down state (solid background, compact header)
        header.classList.add('header-scrolled');
        header.classList.remove('header-large', 'header-transparent-dark');
      } else {
        // Top of screen (transparent background, large centered header)
        header.classList.add('header-large');
        header.classList.remove('header-scrolled');
        
        if (activeTab === 'worship') {
          // On Worship tab at scroll position 0, text is white to contrast with banner
          header.classList.add('header-transparent-dark');
        } else {
          // On other tabs at scroll position 0, text is primary sage green
          header.classList.remove('header-transparent-dark');
        }
      }
    } else {
      // Desktop overrides handled in CSS media queries
      header.classList.remove('header-scrolled', 'header-transparent-dark', 'header-large');
    }
  }

  // Bind scroll and resize events
  window.addEventListener('scroll', handleHeaderScroll);
  window.addEventListener('resize', handleHeaderScroll);

  // Run initial state calculation
  handleHeaderScroll();

});
