<template>
  <div class="search-container">
    <button>
      <router-link
        :to="'/user_dashboard/' + currentUserEmail"
        class="back-button"
      >
        Back
      </router-link>
    </button>
    <h2 class="page-title">Product Search</h2>
    <form @submit.prevent="searchProducts" class="search-form">
      <div class="filter-section">
        <div class="filter-item">
          <label for="category_name" class="filter-label">Category:</label>
          <select v-model="searchParams.category" class="filter-select">
            <option value="All">All</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="filter-item">
          <label for="product_name" class="filter-label">Product Name:</label>
          <input
            type="text"
            v-model="searchParams.product_name"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label for="manufacture_date" class="filter-label"
            >Manufacture Date:</label
          >
          <input
            type="date"
            v-model="searchParams.manufacture_date"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label for="expiry_date" class="filter-label">Expiry Date:</label>
          <input
            type="date"
            v-model="searchParams.expiry_date"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label for="min_price" class="filter-label">Min Price:</label>
          <input
            type="number"
            v-model="searchParams.min_price"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label for="max_price" class="filter-label">Max Price:</label>
          <input
            type="number"
            v-model="searchParams.max_price"
            class="filter-input"
          />
        </div>
      </div>

      <div class="form-group">
        <button type="submit" class="search-button">Search</button>
      </div>
    </form>

    <div v-if="products.length > 0" class="search-results">
      <h3 class="result-title">Search Results:</h3>
      <ul>
        <li v-for="product in products" :key="product.id" class="result-item">
          <p class="product-name">{{ product.name }}</p>
          <p v-if="product.manufacture_date">
            Manufacture Date: {{ product.manufacture_date }}
          </p>

          <p v-else>Manufacturer: Not Available</p>
          <p v-if="product.expiry_date">
            Expiry Date: {{ product.expiry_date }}
          </p>
          <p v-else>Expiry Date: Not Available</p>
          <p class="stock-status">
            Stock Availability:
            {{ product.stock > 0 ? "In Stock" : "Out of Stock" }}
          </p>
          <p>Category: {{ product.category.name }}</p>
          <p class="product-price">Price: {{ product.price }}</p>
        </li>
      </ul>
    </div>
    <div v-else class="no-results">No products Found</div>
  </div>
</template>

<script>
export default {
  name: "searchProduct",
  data() {
    return {
      searchParams: {
        stock: false,
        category: null,
        product_name: "",
        manufacture_date: "",
        expiry_date: "",
        min_price: null,
        max_price: null,
      },
      products: [],
      categories: [],
      errorMessage: "",
    };
  },
  computed: {
    currentUserEmail() {
      return this.$store.state.currentUserEmail;
    },
    isProductOwner() {
      return this.$store.state.currentUserId == this.product.user_id;
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
  mounted() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await fetch("http://localhost:5000/api/getCategory");
        const data = await response.json();
        this.categories = data;
        if (!this.isProductOwner) {
          alert("You are not authorized to view this page");
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch categories:", error);
      }
    },
    async searchProducts() {
      try {
        const formData = new FormData();
        Object.entries(this.searchParams).forEach(([key, value]) => {
          if (value !== null && value !== undefined && value !== "") {
            formData.append(key, value);
          }
        });
        formData.append("stock", this.searchParams.stock);

        const response = await fetch("http://localhost:5000/api/search", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || "Failed to fetch products");
        }

        const responseData = await response.json();
        this.products = responseData;
        this.errorMessage = "";
      } catch (error) {
        this.products = [];
        console.log("Error:", error);
        this.errorMessage = error.message || "Failed to fetch products";
      }
    },
  },
};
</script>

<style scoped>
.search-container {
  margin: 20px;
  background: linear-gradient(to right, #4cd06b, #0db8e8);
  padding: 20px;
}

button {
  background-color: #1ec646;
  color: white;
  padding: 8px 16px;
  border: none;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
}

.page-title {
  color: #333;
  text-decoration: underline;
  text-align: center;
}

.search-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}

.filter-section {
  display: flex;
  flex-wrap: wrap;
}

.filter-item {
  width: calc(33.33% - 20px);
  margin: 10px;
}

.filter-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #333;
}

.filter-select,
.filter-input,
.search-button {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 5px;
}

.search-results {
  margin-top: 20px;
}

.result-title {
  color: #333;
}

.result-item {
  background-color: #fff;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.product-name {
  font-weight: bold;
}

.stock-status {
  color: #28a745;
}
.back-button {
  background-color: black;
  color: white;
  padding: 8px 16px;
  border: none;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
}
.search-button {
  width: 80px;
  margin-left: 600px;
}
.product-price {
  color: #24b7e0;
}

.no-results {
  color: black;
  margin-top: 20px;
}
</style>
