var currentItem = '2770'
var timeframe = 'All'

async function fetch_price_data(item_id=currentItem, start=null, end=null) {

    let url = `http://localhost:8000/data?item_id=${item_id}`
    if (start && end) {
        url += `&start=${start}&end=${end}`
    }

    const response = await fetch(url)
    const data = await response.json()
    const stats = await get_stats(currentItem)
    console.log(data)

    const dates = data.data.map(entry => new Date(entry.t))
    const prices = data.data.map(entry => entry.price)
    
    const item_name = await get_item_name(item_id)
    const recent_price = prices[prices.length - 1]
    const percentage_change_24h = stats.percentage_change
    const gsc_recent_price = copperToGSC(recent_price)
    
    document.getElementById("tickerAssetName").innerHTML = item_name.name
    document.getElementById("tickerCurrentPriceGSC").innerHTML = gsc_recent_price
    document.getElementById("tickerCurrentPrice").innerHTML = recent_price
    document.getElementById("tickerChange").innerHTML = percentage_change_24h
    document.getElementById("change_24h").innerHTML = percentage_change_24h


    document.getElementById("tickerChange").style.color = percentage_change_24h >= 0 ? '#16c281' : '#e43943';
    document.getElementById("change_24h").style.color = percentage_change_24h >= 0 ? '#16c281' : '#e43943';

    var ma_ts = null
    var ma_prices = null

    if (timeframe === "1M" && data.ma_data && data.ma_data.length > 0 && data.ma_data[0].ma_price.length > 0) {
        ma_ts = data.ma_data[0].ma_t.map(t => new Date(t));
        ma_prices = data.ma_data[0].ma_price;
    }

    render_chart(dates, prices, item_name, ma_ts, ma_prices)
}

function render_chart(dates, prices, item_name, ma_ts, ma_prices) {

    const trace = []

    var price = {
        x:dates,
        y:prices,
        type: 'scatter',
        mode: 'lines',
        line: {
            color: '#16c281',
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: '#0e423a96',
        hovertemplate:
            '<b>%{x|%b %d, %Y %H:%M}</b><br>' +
            'Price: %{y:$,.0f}' +
            '<extra></extra>'
    }

    trace.push(price)

    if (ma_ts && ma_prices) {
        var ma = {
            x:ma_ts,
            y:ma_prices,
            type: 'scatter',
            mode: 'lines',
            line: {
                color: '#e43943',
                shape: 'spline'
            },
            fill: 'tozeroy',
            fillcolor: '#401d2967',
            hovertemplate:
                '<b>%{x|%b %d, %Y %H:%M}</b><br>' +
                'Price: %{y:$,.0f}' +
                '<extra></extra>'
        }
        trace.push(ma)
    }

    var layout = {
        autosize: true,
        margin: {
            l: 30,
            r: 30,
            t: 20,
            b: 50
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            color: '#848e9c',
            size: 11
        },
        xaxis: {
            gridcolor: '#3b424c',
            zerolinecolor: '#3b424c',
            tickfont: { size: 11, color: '#848e9c' },
            showgrid: true,
            showline: true,
            linecolor: '#3b424c',
            mirror: true
        },
        yaxis: {
            gridcolor: '#3b424c',
            zerolinecolor: '#3b424c',
            side: 'right',
            tickfont: { size: 11, color: '#848e9c' },
            showgrid: true,
            showline: true,
            linecolor: '#3b424c',
            mirror: true
        },
        hovermode: 'x unified',
        showlegend: false,
        }

    Plotly.newPlot('priceChart', trace, layout, {scrollZoom: true})
}

async function get_item_name(item_id) {

    const url = `http://localhost:8000/name/${item_id}`
    const response = await fetch(url)
    const name = await response.json()

    return name
}

async function get_item_id(item_name) {

    const url = `http://localhost:8000/item_id/${item_name}`
    const response = await fetch(url)
    const item_id = await response.json()

    return item_id
}

async function get_stats(item_id) {

    const url = `http://localhost:8000/stats/${item_id}`
    const response = await fetch(url)
    const data = await response.json()

    var all_time_high = data.all_time_high
    var all_time_low = data.all_time_low
    var daily_high = data.daily_high
    var daily_low = data.daily_low
    var percentage_change = data.percentage_change
    var stability_score = data.stability_score
    var stability_label = data.stability_label
    var total_volume = data.total_volume
    var trend_slope = data.trend_slope
    var volatility = data.volatility
    var volume_24h = data.volume_24h

    console.log(stability_label)

    document.getElementById("all_time_high").innerHTML = all_time_high
    document.getElementById("all_time_low").innerHTML = all_time_low
    document.getElementById("daily_high").innerHTML = daily_high
    document.getElementById("daily_low").innerHTML = daily_low
    document.getElementById("percentage_change").innerHTML = percentage_change
    document.getElementById("stability_score").innerHTML = stability_score
    document.getElementById("stability_label").innerHTML = stability_label
    document.getElementById("total_volume").innerHTML = total_volume
    document.getElementById("trend_slope").innerHTML = trend_slope
    document.getElementById("volatility").innerHTML = volatility
    document.getElementById("volume_24h").innerHTML = volume_24h

    document.getElementById("percentage_change").style.color = percentage_change >= 0 ? '#16c281' : '#e43943';
    document.getElementById("stability_score").style.color = getStabilityColor(stability_score)
    document.getElementById("stability_label").style.color = getStabilityColor(stability_score)

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
        buttons.forEach(function (b) {b.classList.remove("active");});
        this.classList.add("active");
        var range = button.dataset.range
        timeframe = range
        timeframe_date = get_timeframe(range)
        var start = timeframe_date.start
        var end = timeframe_date.end

        fetch_price_data(currentItem, start, end)
    })
})

const searchBar = document.getElementById('itemSearch')
searchBar.addEventListener('keyup', async (e) => {
    if (e.key === "Enter") {
        const searchString = e.target.value.toLowerCase()
        if (!searchString) return

        const item_id = await get_item_id(searchString)
        currentItem = item_id

        fetch_price_data(currentItem)
    }
})

function copperToGSC(copper) {
    const COPPER_PER_SILVER = 100;
    const COPPER_PER_GOLD = 10000;

    const gold = Math.floor(copper / COPPER_PER_GOLD);
    copper %= COPPER_PER_GOLD;

    const silver = Math.floor(copper / COPPER_PER_SILVER);
    copper %= COPPER_PER_SILVER;

    return `${gold}g ${silver}s ${copper}c`;
}

function getStabilityColor(score) {
    if (score === null || score === undefined || !isFinite(score)) {
        return '#3b424c'
    }

    if (score >= 40) return '#16c281'
    if (score >= 20) return '#dac617ff'
    if (score >= 10) return '#d39014ff'
    if (score >= 5)  return '#e43943'
    return '#991b1b'
}

window.onload = function () {
    fetch_price_data(currentItem)
}