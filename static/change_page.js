const pageButtons = document.querySelectorAll(".page-button")

function changePage(i){
    const pages = document.querySelectorAll('.page')
    for (const page of pages){
        page.style.display = 'none'
    }
    document.querySelector(`#page${i}`).style.display = ''
}