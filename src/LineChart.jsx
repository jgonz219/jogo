import { SolidApexCharts } from 'solid-apexcharts';

export function LineChart(props) {
  const series = [
    {
      name: 'Muscle Mass',
      type: 'line',
      data: [132.85, 130.80, 131.13, 129.56, 135.09]
    },
    {
      name: 'Fat Mass',
      type: 'line',
      data: [91.86, 93.98, 92.74, 92.26, 86.00]
    },
    {
      name: 'Bone Mass',
      type: 'line',
      data: [7.18, 7.14, 7.14, 7.09, 7.25]
    },
  ];

  const options = {
    labels: ['2024-9-11', '2024-9-12', '2024-9-13', '2024-9-14', '2024-9-15'],
    xaxis: {
      type: 'datetime'
    },
    colors: ['#00735c', '#c1d9b7', '#e5a298'],
    stroke: {
      curve: 'smooth',
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
