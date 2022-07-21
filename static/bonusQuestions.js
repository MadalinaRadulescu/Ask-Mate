// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    // console.log(items)
    // console.log(sortField)
    // console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    // console.log(items)
    // console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table

    let result = []
    for (let i=0; i<items.length; i++) {
        if (filterValue.startsWith("!Description:")) {
            if (!items[i].Description.includes(filterValue.substring("!Description:".length))) {
                result.push(items[i])
            }
        } else if (filterValue.startsWith("Description:")){
            if (items[i].Description.includes(filterValue.substring("Description:".length))) {
                result.push(items[i])
            }
        } else if (filterValue[0] === "!") {
            if (!items[i].Title.includes(filterValue.slice(1))) {
                result.push(items[i])
            }
        } else if (items[i].Title.includes(filterValue)) {
            result.push(items[i])
        }
    }
    return result
}

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    // console.log("toggle theme")
}
document.querySelector("#theme-button").addEventListener("click", toggleTheme)


function increaseFont() {
    // console.log("increaseFont")
}

function decreaseFont() {
    // console.log("decreaseFont")
}