//
// Place any custom JS here
//

document.querySelectorAll('input[name="type"]').forEach((radio) => {
  console.log('radio', radio.value)
  radio.addEventListener('change', () => {
    const button = document.querySelector('esp-web-install-button')
    console.log('button', button)
    button.manifest = `./manifest/${radio.value}.json`
    button.classList.remove('invisible')
    console.log('button', button)
  })
})
