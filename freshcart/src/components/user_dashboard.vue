<template>
  <div id="app">
    <nav class="navbar">
      <h1 class="dashboard-title">{{ currentUserName }} Dashboard</h1>
      <div class="search-section">
        <label for="search" class="form-label">Search:</label>
        <router-link to="/searchProducts"
          ><input type="text" class="form-input"
        /></router-link>
      </div>
      <router-link to="/cart-buy" class="logout-link bi bi-cart4">
      </router-link>

      <router-link to="/profile" class="logout-link bi bi-person-circle">
      </router-link>
      <router-link to="/" class="logout-link" @click="logout">
        Logout
      </router-link>
    </nav>

    <div class="category-section">
      <h2 style="text-align: center; text-decoration: underline">
        Welcome To Freshcart
      </h2>
      <h3 style="text-align: center; text-decoration: underline">
        Happy Shopping
      </h3>
      <div v-if="Categories.length !== 0" class="category-list">
        <div
          v-for="category in Categories"
          :key="category.id"
          class="category-item"
        >
          <h1 style="text-decoration: underline">{{ category.name }}</h1>
          <div v-if="category.products.length !== 0" class="card-container">
            <div
              v-for="product in category.products"
              :key="product.id"
              class="card"
            >
              <div class="card-header">
                <h3 class="prod-name">{{ product.name }}</h3>
              </div>
              <div class="card-body">
                <p>
                  <strong>Manufacture Date:</strong>
                  {{
                    product.manufacture_date
                      ? product.manufacture_date
                      : "Not Available"
                  }}
                </p>
                <p>
                  <strong> Expiry Date:</strong>
                  {{
                    product.expiry_date ? product.expiry_date : "Not Available"
                  }}
                </p>
                <p><strong>Price:</strong> {{ product.price }}</p>
                <p>
                  <strong>Rate per Unit:</strong> {{ product.rate_per_unit }}
                </p>
                <p><strong>Manager Name:</strong> {{ product.manager_name }}</p>

                <router-link
                  v-if="product.stock > 0"
                  :to="{
                    name: 'cart',
                    params: {
                      category_id: category.id,
                      product_id: product.id,
                    },
                  }"
                  class="btn-success"
                >
                  Add to Cart
                </router-link>
                <router-link
                  v-if="product.stock > 0"
                  :to="{
                    name: 'buy_product',
                    params: {
                      category_id: category.id,
                      product_id: product.id,
                    },
                  }"
                  class="btn-success"
                >
                  Buy Now
                </router-link>
                <p v-else class="out-of-stock">Out of Stock</p>
              </div>
            </div>
          </div>
          <p v-else class="no-products">
            No products available inside this category.
          </p>
        </div>
      </div>
      <p v-else class="no-categories">No products available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserDashboard",
  data() {
    return {
      account: {
        username: "",
        email: "",
        id: null,
        roles: [],
      },
      Categories: [],
      searchQuery: "",
    };
  },
  async mounted() {
    try {
      const email = this.$route.params.email;
      const resaccount = await fetch(
        `http://localhost:5000/api/getUserData/${email}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      const dataaccount = await resaccount.json();
      console.log(dataaccount);
      if (resaccount.ok) {
        this.account = dataaccount;
        this.$store.commit("setCurrentUser", {
          id: dataaccount.id,
          username: dataaccount.username,
          email: dataaccount.email,
          roles: dataaccount.roles,
        });
        console.log("setting done!");
      } else if (resaccount.status == 401) {
        this.success = false;
        this.error = dataaccount.response.error;
      } else {
        this.success = false;
        this.error = dataaccount.message;
        alert("something went wrong");
        this.$router.push("/");
        localStorage.clear();
      }
      const response = await fetch(`http://localhost:5000/api/userDashboard`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      });
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        this.Categories = Array.isArray(data) ? data : [];
      }
    } catch {
      alert("Login Again");
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
#app {
  margin: 10px;
  padding: 20px;
}

.dashboard-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: white;
}

.navbar {
  display: flex;
  align-items: center;
  background-color: #4caf50;
  color: white;
  padding: 10px;
}

.search-section {
  display: flex;
  align-items: center;
  margin-right: 50px;
  margin-left: 500px;
}

.form-label {
  margin-right: 10px;
}

.form-input {
  padding: 5px;
  border: 1px solid #ccc;
}

.logout-link {
  color: white;
  text-decoration: none;
  padding: 5px;
  background-color: #333;
  margin-left: 10px;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 5px;
}

.category-section {
  margin: 20px;
}

.category-item {
  margin-bottom: 20px;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

.card-container {
  display: flex;
  flex-wrap: wrap;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 10px;
  background-color: whitesmoke;
  overflow: hidden;
}

.card-header {
  background-color: #c8c4c4;
  padding: 10px;
}

.card-body {
  padding: 15px;
}

.prod-name {
  margin: 0;
}

.btn-success {
  padding: 8px;
  margin: 10px;
  display: inline-block;
  text-decoration: none;
  color: #fff;
  background-color: #28a745;
  cursor: pointer;
}

.out-of-stock {
  color: red;
  margin: 0;
}
</style>
