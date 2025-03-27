<template>
  <div class="app">
    <h2>Your Bought Items</h2>
    <div v-for="item in boughtItems" :key="item.id" class="container">
      <ul>
        <li>
          <strong>Product Name:</strong> {{ item.product_name }}<br />
          <strong>Category:</strong> {{ item.category_name }}<br />
          <strong>Quantity:</strong> {{ item.product_count }}<br />
          <strong>Manufacture Date:</strong>
          {{ item.manufacture_date ? item.manufacture_date : "Not Available"
          }}<br />
          <strong>Expiry Date:</strong>
          {{ item.expiry_date ? item.expiry_date : "Not Available" }}<br />
          <strong>Price:</strong> {{ item.amount }}<br />
          <strong>Ordered Date:</strong> {{ item.bought_date }}
        </li>
        <br />
      </ul>
    </div>
    <div style="display: flex; margin-left: 370px">
      <router-link
        :to="'/user_dashboard/' + currentUserEmail"
        class="logout-link"
      >
        Back to dashboard
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "boughtProducts",
  data() {
    return {
      boughtItems: [],
    };
  },
  async mounted() {
    const response = await fetch("http://localhost:5000/api/bought", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": localStorage.getItem("auth-token"),
      },
    });
    const data = await response.json();
    console.log(data);
    if (response.ok) {
      this.boughtItems = data.bucket;
    }
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
  },
};
</script>
<style scoped>
.app {
  width: 40%;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

.container {
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
.out-of-stock {
  padding: 10px;
  background-color: #4caf50;
  margin-left: 30px;
  color: #fff;
  border: none;
  cursor: pointer;
  width: 30%;
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
  width: 50%;
  background-color: #000000;
  border-radius: 5px;
}

.logout-link:hover {
  background-color: #ddd;
}
</style>
