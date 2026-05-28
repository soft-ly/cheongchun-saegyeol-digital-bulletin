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

  /* ==========================================================================
     3. New Family Registration Form with Validation
     ========================================================================== */
  const connectForm = document.getElementById('connect-form');
  const successOverlay = document.getElementById('form-success-overlay');
  const successCloseBtn = document.getElementById('success-close-btn');

  // Input Formatting helper for Korean Mobile Phone Format (010-XXXX-XXXX)
  const phoneInput = document.getElementById('reg-phone');
  if (phoneInput) {
    phoneInput.addEventListener('input', (e) => {
      let value = e.target.value.replace(/[^0-9]/g, '');
      let formattedValue = '';
      
      if (value.length < 4) {
        formattedValue = value;
      } else if (value.length < 7) {
        formattedValue = `${value.substr(0, 3)}-${value.substr(3)}`;
      } else if (value.length < 11) {
        formattedValue = `${value.substr(0, 3)}-${value.substr(3, 3)}-${value.substr(6)}`;
      } else {
        formattedValue = `${value.substr(0, 3)}-${value.substr(3, 4)}-${value.substr(7, 4)}`;
      }
      
      e.target.value = formattedValue;
    });
  }

  // Form field validator
  function validateField(input, errorElement, validationFn, errorMessage) {
    const value = input.value.trim();
    const isValid = validationFn(value);

    if (!isValid) {
      input.classList.add('is-invalid');
      errorElement.textContent = errorMessage;
      errorElement.classList.add('visible');
      return false;
    } else {
      input.classList.remove('is-invalid');
      errorElement.classList.remove('visible');
      return true;
    }
  }

  if (connectForm) {
    connectForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const nameInput = document.getElementById('reg-name');
      const nameError = document.getElementById('error-name');
      const phoneInput = document.getElementById('reg-phone');
      const phoneError = document.getElementById('error-phone');
      const emailInput = document.getElementById('reg-email');
      const emailError = document.getElementById('error-email');

      // Validation logic
      const isNameValid = validateField(
        nameInput,
        nameError,
        (val) => val.length >= 2,
        '이름은 2자 이상 입력해주세요.'
      );

      const phoneRegex = /^01[016789]-\d{3,4}-\d{4}$/;
      const isPhoneValid = validateField(
        phoneInput,
        phoneError,
        (val) => phoneRegex.test(val),
        '연락처 형식(010-0000-0000)을 확인해주세요.'
      );

      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      const isEmailValid = validateField(
        emailInput,
        emailError,
        (val) => val === '' || emailRegex.test(val),
        '올바른 이메일 주소를 입력해주세요.'
      );

      // Submit only if all fields pass
      if (isNameValid && isPhoneValid && isEmailValid) {
        // Form is valid! Show success state overlay
        successOverlay.classList.add('active');
        
        // Reset form inputs after successfully animation finishes
        setTimeout(() => {
          connectForm.reset();
          document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
          document.querySelectorAll('.form-error').forEach(el => el.classList.remove('visible'));
        }, 300);
      }
    });
  }

  // Close the New Family Registration Success Overlay
  if (successCloseBtn) {
    successCloseBtn.addEventListener('click', () => {
      successOverlay.classList.remove('active');
    });
  }

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
