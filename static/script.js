const verifyButton = document.querySelectorAll(".verify");

async function toggleButton(event, element) {
    event.preventDefault();
    const request = await fetch(event.target.action, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            bila: event.target.dataset.bila //  <button data-bila="alba">Bila alba</button>
        })
        //  if request.method == "POST":
        //      bila = request.json.get("bila")
    });
    if (request.ok) {
        const response = await request.json();

        element.querySelector("button i").classList.toggle("bi-app");
        element.querySelector("button i").classList.toggle("bi-check2-square");
    }
}

verifyButton.forEach(function (element) {
    element.addEventListener("submit", async (event) => {
        await toggleButton(event, element);
    });
});
