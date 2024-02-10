import { For, createSignal } from "solid-js";

const initialFoods = [
  {date: '2024-02-09', name: 'Oatmeal', quatity: 1, time: 'breakfast', calories: 95, fat: 3, carbs: 27, protein: 5},
  {date: '2024-02-09', name: 'Coffee', quatity: 1, time: 'breakfast', calories: 0, fat: 0, carbs: 0, protein: 0},
  {date: '2024-02-09', name: 'Pizza Slice', quatity: 3, time: 'lunch', calories: 250, fat: 9, carbs: 32, protein: 11},
  {date: '2024-02-09', name: 'Ham Sandwich', quatity: 1, time: 'dinner', calories: 361, fat: 16, carbs: 32, protein: 19}
]

const date = new Date('2024-02-09')

export function FoodLog() {
  const [foods, setFoods] = createSignal(initialFoods)

  return (
    <>
      <h3>{date.toDateString()}</h3>
      <table class="table table-borderless">
        <thead>
          <tr>
            <th colspan='5'>Food Log</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th></th>
            <th>Calories</th>
            <th>Fat</th>
            <th>Carbs</th>
            <th>Protein</th>
          </tr>
          <tr>
            <th colspan='5'>Breakfast</th>
          </tr>
          <For each={foods()}>
            {(food) => {
              if (food.time == 'breakfast') {
                return (
                  <tr>
                    <td>{food.name}</td>
                    <td>{food.calories}</td>
                    <td>{food.fat}</td>
                    <td>{food.carbs}</td>
                    <td>{food.protein}</td>
                  </tr>
                )
              }
            }}
          </For>
          <tr>
            <th colspan='5'>Lunch</th>
          </tr>
          <For each={foods()}>
            {(food) => {
              if (food.time == 'lunch') {
                return (
                  <tr>
                    <td>{food.name}</td>
                    <td>{food.calories}</td>
                    <td>{food.fat}</td>
                    <td>{food.carbs}</td>
                    <td>{food.protein}</td>
                  </tr>
                )
              }
            }}
          </For>
          <tr>
            <th colspan='5'>Dinner</th>
          </tr>
          <For each={foods()}>
            {(food) => {
              if (food.time == 'dinner') {
                return (
                  <tr>
                    <td>{food.name}</td>
                    <td>{food.calories}</td>
                    <td>{food.fat}</td>
                    <td>{food.carbs}</td>
                    <td>{food.protein}</td>
                  </tr>
                )
              }
            }}
          </For>
        </tbody>
      </table>
    </>
  );
}