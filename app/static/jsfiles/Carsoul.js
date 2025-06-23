Items = document.getElementsByClassName("CarsoulItem")
Images = ["header1.jpg", "header2.jpg", "header3.jpg", "header4.jpg", "header5.jpg"]
container = document.getElementsByClassName("CarsoulContainer")[0]

function changeBackground(index) {
    container.style.opacity = 1;
    setTimeout(() => {
        container.style.opacity = 1;
        container.style.backgroundImage = `url(/static/assets/home/${Images[index]})`;
    }, 500);
}

const intervalId = setInterval(() => {
    for (let index = 0; index < Items.length; index++) {
        if (Items[index].classList.contains("active")) {
            console.log(index)
            if(!Items[index].classList.contains("Last")){
                Items[index].classList.remove("active")
                Items[index+1].classList.add("active")
                container.style.backgroundImage = changeBackground(index + 1)
            }else{
                Items[index].classList.remove("active")
                Items[0].classList.add("active")
                container.style.backgroundImage = changeBackground(0)
            }
            break
        }
    }
}, 3000);