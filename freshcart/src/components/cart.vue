<template>
  <div id="app">
    <div style="display: flex; margin-left: 400px">
      <router-link
        :to="'/user_dashboard/' + currentUserEmail"
        class="logout-link"
      >
        Back
      </router-link>
    </div>
    <div id="applog">
      <h2>{{ product.name }}</h2>
      <br />
      Enter Quantity:
      <input
        name="product_count"
        v-model="formData.product_count"
        type="number"
        required
      />
      <br />
      <button @click="AddToCart">Add to cart</button>
      <p class="total-amount">Total Amount: ₹ {{ total_amount }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "cartProduct",
  data() {
    return {
      product: {
        name: "",
        price: "",
        id: "",
      },
      formData: {
        product_count: 0,
      },
    };
  },

  computed: {
    currentUserEmail() {
      return this.$store.state.currentUserEmail;
    },
    currentUserId() {
      return this.$store.state.currentUserId;
    },
    currentUserName() {
      return this.$store.state.currentUsername;
    },
    isUser() {
      return this.account.roles.includes("<Role 2>");
    },

    total_amount() {
      const count = parseInt(this.formData.product_count);
      const price = parseInt(this.product.price);
      return count * price;
    },
  },
  async mounted() {
    const product_id = this.$route.params.product_id;
    const category_id = this.$route.params.category_id;
    const response = await fetch(
      `http://localhost:5000/api/getProduct/${category_id}/${product_id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      }
    );
    const data = await response.json();
    console.log(data);
    if (response.ok) {
      this.product = data;
    }
  },
  methods: {
    async AddToCart() {
      try {
        if (
          this.product.stock !== null &&
          this.formData.product_count > this.product.stock
        ) {
          alert(
            "Please enter less amount of products. Not enough Stock available"
          );
          return;
        }
        const formdata = new FormData();
        formdata.append("product_count", this.formData.product_count);
        const prod_id = this.$route.params.product_id;
        const response = await fetch(
          `http://localhost:5000/api/cartProduct/${prod_id}`,
          {
            method: "POST",
            headers: {
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
            body: formdata,
          }
        );
        const data = await response.json();
        console.log(data.message);
        if (response.ok) {
          alert(data.message);
          this.$router.push(`/user_dashboard/${this.currentUserEmail}`);
        } else {
          alert("Something went wrong");
        }
      } catch {
        alert("Something Went Wrong. Please Login");
      }
    },
  },
};
</script>
<style scoped>
#app {
  width: 40%;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}
#applog {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h2 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

input {
  width: 50%;
  padding: 10px;
  margin-bottom: 20px;

  box-sizing: border-box;
}

button {
  padding: 10px;
  background-color: #4caf50;
  margin-left: 30px;
  color: #fff;
  border: none;
  cursor: pointer;
  width: 20%;
  box-sizing: border-box;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

p {
  text-align: center;
  margin-top: 20px;
  font-weight: bold;
  color: #333;
}

.logout-link {
  text-align: center;
  margin: 15px;
  color: #ffffff;
  text-decoration: none;
  padding: 10px;
  width: 30%;
  background-color: #000000;
  border-radius: 5px;
}

.logout-link:hover {
  background-color: #ddd;
}
</style>
