async function fetch_price_data(item_id="2770", start=null, end=null) {

    let url = `http://localhost:8000/data?item_id=${item_id}`
    if (start && end) {
        url += `&start=${start}&end=${end}`
    }

    const response = await fetch(url)
    const data = await response.json()

    console.log(data)

    const dates = data.data.map(entry => new Date(entry.t))
    const prices = data.data.map(entry => entry.price)

    const item_name = await get_item_name(item_id)

    const ma_ts = data.ma_data.map(entry => new Date(entry.ma_t))
    const ma_prices = data.data.map(entry => entry.ma_prices)

    render_chart(dates, prices, item_name, ma_ts, ma_prices)
}

function render_chart(dates, prices, item_name, ma_ts, ma_prices) {
    var price = {
        x:dates,
        y:prices,
        type: 'scatter',
        mode: 'lines',
        line: {
            color: 'rgb(0, 123, 255)',
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(0, 123, 255, 0.1)',
        hovertemplate:
            '<b>%{x|%b %d, %Y %H:%M}</b><br>' +
            'Price: %{y:$,.0f}' +
            '<extra></extra>'
    }

    var ma = {
        x:ma_ts,
        y:ma_prices,
        type: 'scatter',
        mode: 'lines',
        line: {
            color: 'rgba(247, 58, 33, 1)',
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(255, 85, 85, 0.1)',
        hovertemplate:
            '<b>%{x|%b %d, %Y %H:%M}</b><br>' +
            'Price: %{y:$,.0f}' +
            '<extra></extra>'
    }

    var trace = [price, ma]

    var layout = {
        title: {
            text: `${item_name.name}`
        },
        showlegend: false,
        hovermode: 'x',
    }

    Plotly.newPlot('priceChart', trace, layout, {scrollZoom: true})
}

async function get_item_name(item_id) {

    const url = `http://localhost:8000/name/${item_id}`
    const response = await fetch(url)
    const name = await response.json()

    return name
}

async function get_stats(item_id) {

    const url = `http://localhost:8000/stats/${item_id}`
    const response = await fetch(url)
    const data = await response.json()

    console.log(data)

    return data

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
    get_stats(2770)
}