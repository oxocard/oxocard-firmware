//
// Place any custom JS here
//

document.querySelectorAll('input[name="type"]').forEach((radio) => {
  radio.addEventListener('change', () => {
    const button = document.querySelector('esp-web-install-button')
    button.manifest = `manifest_${radio.value}.json`
    button.classList.remove('invisible')
    console.log('button', button)
  })
})
