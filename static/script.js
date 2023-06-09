const verifyButton = document.querySelectorAll(".verify")

async function toggleButton(event, element) {
    event.preventDefault()
    const request = await fetch(event.target.action);
    if (request.ok) {
        const response = await request.json()
        
        element.querySelector("button i").classList.toggle("bi-app");
        element.querySelector("button i").classList.toggle("bi-check2-square");
    }
}

verifyButton.forEach(function (element) {
    element.addEventListener("submit", async (event) => {
        await toggleButton(event, element)
    })
})


