const verifyButton = document.querySelectorAll(".verify")

async function toggleButton(event, element) {
    event.preventDefault()
    const request = await fetch(event.target.action);
    // const request = await fetch(`/api/question/${question_id}/${answer_id}`);
    if (request.ok) {
        const response = await request.json()
        console.log(response)
        element.querySelector("button i").classList.toggle("bi-check-square");
        element.querySelector("button i").classList.toggle("bi-check-square-fill");
    }
}

verifyButton.forEach(function (element) {
    element.addEventListener("submit", async (event) => {
        await toggleButton(event, element)
    })
})


