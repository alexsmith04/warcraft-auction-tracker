
async function get_market_overview() {
    const url = `http://127.0.0.1:8000/market`
    const response = await fetch(url)
    const data = await response.json()
    const list = document.getElementById("market-list")

    data.slice(0, 99).forEach(function (item) {
        const link = document.createElement("a")
        link.href = `/pricechart?item_id=${item.item_id}`
        link.className = "market-link"

        const box = document.createElement("div")
        box.className = "market-box"
        box.innerHTML = `<div class="market-name">${item.name}</div>`

        link.appendChild(box)
        list.appendChild(link)
    })
}

const searchBar = document.getElementById('itemSearch')
searchBar.addEventListener('keyup', async (e) => {
    if (e.key === "Enter") {
        const searchString = e.target.value.toLowerCase()
        if (!searchString) return

        const item_id = await get_item_id(searchString)
        
        window.location.href = `/pricechart?item_id=${item_id}`
    }
})

async function get_item_id(item_name) {
    const url = `http://localhost:8000/item_id/${item_name}`
    const response = await fetch(url)
    const item_id = await response.json()

    return item_id
}

window.onload = function () {
    get_market_overview()
}