function getSortedItems(items, sortField, sortDirection) {
    if (sortDirection === "asc") {
        const firstItem = items.shift();
        if (firstItem) {
            items.push(firstItem);
        }
    } else {
        const lastItem = items.pop();
        if (lastItem) {
            items.push(lastItem);
        }
    }

    return items;
}

function getFilteredItems(items, filterValue) {
    let result = [];
    for (let i = 0; i < items.length; i++) {
        if (
            (filterValue.startsWith("!Description:") &&
                !items[i].Description.includes(
                    filterValue.substring("!Description:".length)
                )) ||
            (filterValue.startsWith("Description:") &&
                items[i].Description.includes(
                    filterValue.substring("Description:".length)
                )) ||
            (filterValue.startsWith("Title:") &&
                items[i].Title.includes(
                    filterValue.substring("Title:".length)
                )) ||
            (filterValue.startsWith("!Title:") &&
                !items[i].Title.includes(
                    filterValue.substring("!Title:".length)
                ))
        ) {
            result.push(items[i]);
        }
    }
    return result;
}

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
}
document.querySelector("#theme-button").addEventListener("click", toggleTheme);

function increaseFont() {}

function decreaseFont() {}
