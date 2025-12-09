async function fetch_price_data(item_id="2770", start=null, end=null) {

    let url = `http://localhost:8000/data?item_id=${item_id}`
    if (start && end) {
        url += `&start=${start}&end=${end}`
    }

    console.log("Fetching:", url);
    const response = await fetch(url)
    const data = await response.json()

    const dates = data.data.map(entry => new Date(entry.t))
    const prices = data.data.map(entry => entry.price)
    
    console.log(dates)

    const item_name = await get_item_name(item_id)

    render_chart(dates, prices, item_name)
}

function render_chart(dates, prices, item_name) {
    var trace1 = {
        x:dates,
        y:prices,
        type: 'scatter',
        mode: 'lines',
        line: {
            color: 'rgb(0, 123, 255)'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(0, 123, 255, 0.1)'
    }

    var trace = [trace1]

    var layout = {
        title: {
            text: `${item_name.name}`
        },
        showlegend: false
    }

    Plotly.newPlot('priceChart', trace, layout, {scrollZoom: true})
}

async function get_item_name(item_id) {

    const url = `http://localhost:8000/name/${item_id}`
    const response = await fetch(url)
    const name = await response.json()

    return name
}

function get_timeframe(range) {
    const now = new Date()
    let start

    switch (range) {
        case "24h":
            start = new Date(now.getTime() - (24 * 60 * 60 * 1000))
            break
        case "1W":
            start = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
            break
        case "1M":
            start = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000))
            break
        case "1Y":
            start = new Date(now.getTime() - (365 * 24 * 60 * 60 * 1000))
            break
        case "All":
            start = null
            break
        default:
            start = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
    }

    if (start != null) {
        start = start.toISOString()
    }
    end = now.toISOString()

    return { start, end };
}

var buttons = document.querySelectorAll(".timeframe-button")
buttons.forEach(function(button) {
    button.addEventListener("click", function() {
        var range = button.dataset.range
        var timeframe = get_timeframe(range)
        var start = timeframe.start
        var end = timeframe.end

        fetch_price_data("2770", start, end)
    })
})

window.onload = function () {
    fetch_price_data()
}