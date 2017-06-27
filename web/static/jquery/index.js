$(function () {

  Highcharts.setOptions({
    colors: ['#f47961', '#60be7b', '#4b5d69', '#9fdbea']
  });

  $('#areaChart').highcharts({
    chart: {
      type: 'areaspline',
      zoomType: 'x'
    },
    title: { text: null },
    legend: { enabled: false },

    xAxis: {
      type: 'datetime',
      categories: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'
      ],
      min: 0.5,
      max: 11,
      plotLines: [{
        color: 'red',
        dashStyle: 'solid',
        value: '3',
        width: '1'
      }]
    },

    yAxis: {
      title: {
        text: null
      }
    },

    tooltip: {
      shared: true
    },

    credits: {
      enabled: false
    },

    plotOptions: {
      areaspline: {
        fillOpacity: 0.8
      },
      series: {
        marker: { enabled: false },
        lineWidth: 0
      }
    },

    series: [{
      name: 'Failing',
      data: [1,2,3,4,5]
    }, {
      name: 'Unknown',
      data: [1,2,3,4,5,6]
    }, {
      name: 'Passing',
      data: [1,2,3,4,5,20000]
    }]
  });
});

// $(function () {
//     Highcharts.setOptions({
//         colors: ['#f47961', '#60be7b', '#4b5d69', '#9fdbea']
//     });
//     $('#areaChart').highcharts({
//         chart: {
//             type: 'areaspline',
//             zoomType: 'x'
//         },
//         title: {text: null},
//         legend: {enabled: false},
//
//         xAxis: {
//             type: 'datetime',
//             categories: [1, 2, 3, 4, 5],
//             min: 0.5,
//             max: 11,
//             plotLines: [{
//                 color: 'red',
//                 dashStyle: 'solid',
//                 value: '3',
//                 width: '1'
//             }]
//         },
//
//         yAxis: {
//             title: {
//                 text: null
//             }
//         },
//
//         tooltip: {
//             shared: true
//         },
//
//         credits: {
//             enabled: false
//         },
//
//         plotOptions: {
//             areaspline: {
//                 fillOpacity: 0.8
//             },
//             series: {
//                 marker: {enabled: false},
//                 lineWidth: 0
//             }
//         },
//
//         series: [{
//             name: 'Failing',
//             data: hms
//         }, {
//             name: 'Unknown',
//             data: epg
//         }, {
//             name: 'Passing',
//             data: ll
//         }]
//     });
// })