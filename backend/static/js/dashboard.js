const ctx = document.getElementById('assetActivityChart'); 
// get elemnt by id where this id is there take that element

 new Chart(ctx, { //new chart on ctx variable i.e canvas
    type: 'line',

    data: {
        labels: ['March', 'April', 'May', 'June', 'July', 'August'], // things taht are to be placed at the bottom of the chart

        datasets: [ //The actual numbers that belong to our labels.
            {
                label: 'Assets Added',
                data: [18, 24, 20, 32, 27, 35],
                tension: 0.4, // makes the line curved/smoother.
                borderColor: '#087443',
                pointBackgroundColor: '#087443',
            pointBorderColor: '#FAFAFA',
            pointRadius: 4
            },
         {
            label: 'Assets Assigned',
             data: [12, 19, 17, 25, 23, 29],
             tension: 0.4,
            borderColor: '#18A66A'
         },
        {
            label: 'Assets Returned',
           data: [5, 8, 6, 10, 7, 9],
          tension: 0.4,
        borderColor: '#74C69D'
         }
         ]
    },

    options: { //HOW should the chart behave
        responsive: true, //Make the chart adjust to the available space.

        maintainAspectRatio: false, //Don't force your own preferred width-to-height ratio. Let my CSS control the chart's height

        plugins: {
            legend: {
                position: 'top' //Put the legend at the top
            }
        },

        scales: {
            y: {
                beginAtZero: true,
                 //Start the Y-axis at zero
                grid: {
                    color: '#E5EDE8'
                        }
            
            },
             x: {
                grid: {
                    display: false //no vertical lines
                }
            }
        }
        }
});
