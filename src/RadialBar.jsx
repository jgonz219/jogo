import { SolidApexCharts } from 'solid-apexcharts';
import { createSignal } from 'solid-js';

export function RadialBar(props) {
  const series = [(5/50 * 100)];

  const options = {
    stroke: {
      lineCap: 'round',
    },

    labels: [''],

    title: {
      text: props.title,
      align: 'center',
      style: {}
    },

    colors: ['#00e091'],

    // fill: {
    //   type: 'gradient',
    //   gradient: {
    //     type: 'vertical',
    //     gradientToColors: ['#00735c'],
    //     stops: [0, 100]
    //   }
    // },

    plotOptions: {
      radialBar: {
        hollow: {
          margin: 15,
          size: '70%',
        },
       
        dataLabels: { // hidden
          show: true,
          name: {
            offsetY: -10,
            show: true,
            color: '#888',
            fontSize: '13px'
          },
          value: {
            offsetY: 0,
            color: '#111',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
            formatter: function (w) {
              return w + '%'
            }
          },
        }
      }
    },
  

  };



  return (
    <>
      <SolidApexCharts type='radialBar' width='300' options={options} series={series}/>
    </>
  )
}