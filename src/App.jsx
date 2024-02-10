import { RadialBar } from "./RadialBar";
import { LineChart } from "./LineChart";
import { LineBarChart } from "./LineBarChart";
import { FoodLog } from "./FoodLog";

function App() {
  return (
    <div>
      <RadialBar title='Gym Sessions'></RadialBar>
      <LineChart title='Body Composition'></LineChart>
      <LineBarChart title='Weight and Calorie Intake'></LineBarChart>
      <FoodLog></FoodLog>
    </div>
  );
}

export default App;
