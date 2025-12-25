
async function get_market_overview() {
    const url = `http://127.0.0.1:8000/market`
    const response = await fetch(url)
    const data = await response.json()
    const list = document.getElementById("market-list")

    data.slice(0, 99).forEach(function (item) {
        const link = document.createElement("a")
        link.href = `/static/pricechart.html?item_id=${item.item_id}`
        link.className = "market-link"

        const box = document.createElement("div")
        box.className = "market-box"
        box.innerHTML = `<div class="market-name">${item.name}</div>`

        link.appendChild(box)
        list.appendChild(link)
    })
}

window.onload = function () {
    get_market_overview()
}