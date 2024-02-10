import { SolidApexCharts } from 'solid-apexcharts';

export function LineBarChart(props) {
  const series = [
    {
      name: 'Weight',
      type: 'line',
      data: [231.99, 231.95, 231.05, 228.96,228.37]
    },
    {
      name: 'Calories Defecit',
      type: 'column',
      data: [1425, 1464, 1705, 1079, 1068]
    },
    {
      name: 'Calories Defecit Goal',
      type: 'line',
      data: [1000, 1000, 1000, 1000, 1000]
    },
  ];

  const options = {
    labels: ['2024-9-11', '2024-9-12', '2024-9-13', '2024-9-14', '2024-9-15'],
    xaxis: {
      type: 'datetime'
    },
    yaxis: [
      {
        axisTicks: {
          show: true
        },
        title: {
          text: "Weight",
        }        
      },
      {
        opposite: true,
        axisTicks: {
          show: true
        },
        title: {
          text: "Calories",
        },
        min: 0,
        max: 1800,
      },
      {
        show: false,
        opposite: true,
        axisTicks: {
          show: true
        },
        title: {
          text: "Calories",
        },
        min: 0,
        max: 1800,    
      }
  ],
    colors: ['#00735c', '#c1d9b7', '#111'],
    stroke: {
      curve: 'smooth',
      dashArray: [0, 0 ,10],
    },
    title: {
      text: props.title,
    }
  }

  return (
    <>
      <SolidApexCharts type='line' height='300' width='500' options={options} series={series}/>
    </>
  )
}
