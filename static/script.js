async function fetch_price_data() {

    const item_id = "2770"

    const url = `http://localhost:8000/data?item_id=${item_id}`
    const response = await fetch(url)
    const data = await response.json();

    const dates = data.data.map(entry => new Date(entry.t));
    const prices = data.data.map(entry => entry.price);
    
    console.log(dates)

    const item_name = await get_item_name(item_id)

    render_chart(dates, prices, item_name)
}

function render_chart(dates, prices, item_name) {
    var trace1 = {
        x:dates,
        y:prices,
        type: 'scatter'
    }

    var trace = [trace1];

    var layout = {
        title: {
            text: `${item_name.name}`
        },
        showlegend: false
    }

    Plotly.newPlot('priceChart', trace, layout, {scrollZoom: true});
}

async function get_item_name(item_id) {

    const url = `http://localhost:8000/name/${item_id}`
    const response = await fetch(url)
    const name = await response.json();

    return name
}

window.onload = function () {
    fetch_price_data();
};