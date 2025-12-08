async function fetch_price_data() {

    const url = "http://localhost:8000/data?item_id=2770"
    const response = await fetch(url)
    const data = await response.json();

    console.log(data)

    const timestamps = data.data.map(entry => entry.t);
    const dates = timestamps.map(t => new Date(t));
    const prices = data.data.map(entry => entry.price);
    
    console.log(dates)

    var trace1 = {
        x:timestamps,
        y:prices,
        type: 'scatter'
    };

    var trace = [trace1];

    var layout = {
        title: {
            text: 'Scroll and Zoom'
        },
        showlegend: false
    };

    Plotly.newPlot('priceChart', trace, layout, {scrollZoom: true});
}