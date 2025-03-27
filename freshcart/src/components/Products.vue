<template>
  <div class="product-list">
    <router-link
      :to="'/admin_dashboard/' + currentUserEmail"
      class="back-button"
      >Back
    </router-link>
    <h2>Category Products</h2>
    <div v-if="products.length > 0">
      <ul class="product-ul">
        <li v-for="product in products" :key="product.id" class="product-item">
          <strong class="product-label">Product Name:</strong>
          <span class="product-info">{{ product.name }}</span
          ><br />

          <strong class="product-label">Manager Name:</strong>
          <span class="product-info">{{ product.manager_name }}</span
          ><br />

          <strong class="product-label">Price:</strong>
          <span class="product-info">{{ product.price }}</span
          ><br />
        </li>
      </ul>
    </div>
    <div v-else>
      <p class="no-products">No products available for this category.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ViewProducts",
  data() {
    return {
      approvedCategories: [],
      formData: {
        category_name: "",
      },
      fta: {
        category_name: "",
      },
      products: [],
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
      return this.account.roles.includes("<Role 1>");
    },
  },
  async mounted() {
    const c_id = this.$route.params.category_id;
    const response = await fetch(
      `http://localhost:5000/api/getProducts/${c_id}`,
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
      this.products = Array.isArray(data) ? data : [];
    } else {
      alert("No Products Available");
    }
  },
};
</script>
<style scoped>
.product-list {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

.product-ul {
  list-style: none;
  padding: 0;
}

.product-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.product-label {
  font-weight: bold;
  margin-right: 5px;
}

.no-products {
  font-style: italic;
  color: #777;
}
.back-button {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 16px;
  text-decoration: none;
  background-color: #333;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
</style>
