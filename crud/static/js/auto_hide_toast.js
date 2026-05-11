setTimeout(() => {
    const toastMessages = document.querySelectorAll('[id^="toast-"]')

    toastMessages.forEach(toast => {
        toast.style.display = 'none'
    })

}, 3000)