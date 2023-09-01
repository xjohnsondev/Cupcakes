const BASE_URL = "http://127.0.0.1:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-button">X</button>
        </li>
        <img class="cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>
    `;
}

async function showCupcakes() {
    const res = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcake of res.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcake));
        $('#list').append(newCupcake);
    }
}

$('#list').on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(this).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)
    $cupcake.remove();
})


showCupcakes();