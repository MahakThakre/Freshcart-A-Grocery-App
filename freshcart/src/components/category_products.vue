<template>
  <div id="app" class="product-container">
    <div style="margin-left: 600px; margin-top: -10px">
      <router-link to="/" class="logout-link" @click="logout">
        Logout </router-link
      >&nbsp;&nbsp;
      <router-link
        :to="'/manager_dashboard/' + currentUserEmail"
        class="btn-dark"
        >Back</router-link
      >
    </div>
    <div class="edit-category">
      <h3 class="title">Edit Category</h3>

      <div class="form-group">
        <label for="category_name" class="form-label">Category Name:</label>
        <input
          type="text"
          v-model="fta.category_name"
          required
          class="form-cat-input"
        />
      </div>
      <button @click="editcategory" class="edit-button">
        Edit Category Request
      </button>
    </div>
    <div class="new-product">
      <h3 class="title">Products</h3>

      <ul v-if="products.length !== 0" class="product-list">
        <li v-for="product in products" :key="product.id" class="product-item">
          <router-link
            :to="{
              name: 'single_product',
              params: {
                category_id: product.category.id,
                product_id: product.id,
              },
            }"
            class="product-link"
          >
            {{ product.name }}
          </router-link>
        </li>
      </ul>
      <p v-else class="no-products">No products available.</p>
    </div>
    <div class="new-product">
      <h3 class="title">Create New Product</h3>
      <div class="form-group">
        <div class="form-column">
          <label for="product_name" class="form-label">Product Name:</label>
          <input
            type="text"
            v-model="formData.product_name"
            required
            class="form-input"
          />
        </div>

        <div class="form-column">
          <label for="manufacture_date" class="form-label"
            >Manufacture Date:</label
          >
          <input
            type="date"
            v-model="formData.manufacture_date"
            class="form-input"
          />
        </div>
      </div>

      <div class="form-group">
        <div class="form-column">
          <label for="expiry_date" class="form-label">Expiry Date:</label>
          <input
            type="date"
            v-model="formData.expiry_date"
            class="form-input"
          />
        </div>

        <div class="form-column">
          <label for="price" class="form-label">Product Price:</label>
          <input
            type="number"
            v-model="formData.price"
            class="form-input"
            required
          />
        </div>
      </div>

      <div class="form-group">
        <div class="form-column">
          <label for="rate_per_unit" class="form-label">Rate per Unit:</label>
          <select v-model="formData.rate_per_unit" required class="form-select">
            <option value="kg">Rs/kg</option>
            <option value="lit">Rs/lit</option>
            <option value="pack">Rs/pack</option>
            <option value="piece">Rs/piece</option>
          </select>
        </div>

        <div class="form-column">
          <label for="stock" class="form-label">Product Stock:</label>
          <input
            type="number"
            v-model="formData.stock"
            required
            class="form-input"
          />
        </div>
      </div>

      <button @click.prevent="createProduct" class="create-button">
        Create Product
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "CategoryProducts",
  data() {
    return {
      products: [],
      formData: {
        product_name: "",
        manufacture_date: "",
        expiry_date: "",
        price: 0,
        rate_per_unit: "",
        stock: 0,
      },
      fta: {
        category_name: "",
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
  methods: {
    async createProduct() {
      if (
        !this.formData.product_name ||
        !this.formData.price ||
        !this.formData.rate_per_unit ||
        !this.formData.stock
      ) {
        alert("Please fill in all required fields.");
        return;
      }
      const isConfirmed = window.confirm(
        "Are you sure you want to create this product?"
      );
      if (!isConfirmed) {
        return;
      }

      const formdata = new FormData();
      formdata.append("product_name", this.formData.product_name);
      formdata.append("manufacture_date", this.formData.manufacture_date);
      formdata.append("expiry_date", this.formData.expiry_date);
      formdata.append("price", this.formData.price);
      formdata.append("rate_per_unit", this.formData.rate_per_unit);
      formdata.append("stock", this.formData.stock);

      const cat_id = this.$route.params.category_id;
      const _response = await fetch(
        `http://localhost:5000/api/addProduct/${cat_id}`,
        {
          method: "POST",
          headers: {
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: formdata,
        }
      );

      const data = await _response.json();
      console.log(data);

      if (_response.ok) {
        this.products = data;
        this.clearForm();
      } else {
        alert("Error in creating product");
      }
    },

    clearForm() {
      this.formData = {
        product_name: "",
        manufacture_date: "",
        expiry_date: "",
        price: 0,
        rate_per_unit: "",
        stock: 0,
      };
    },

    async editcategory() {
      const isConfirmed = window.confirm(
        "Are you sure you want to send the category updation request?"
      );
      if (!isConfirmed) {
        return;
      }
      const c_id = this.$route.params.category_id;
      const formdata = new FormData();
      formdata.append("category_name", this.fta.category_name);
      const response = await fetch(
        `http://localhost:5000/api/editCategory/${c_id}`,
        {
          method: "put",
          headers: {
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: formdata,
        }
      );

      const data = await response.json();
      console.log(data);

      if (response.ok) {
        alert("Category updation request sent successfully!");
        this.formData.category_name = "";
      } else {
        alert(
          "Failed to send category updation request, Category Already Exists"
        );
      }
    },
  },
};
</script>
<style scoped>
#app {
  max-width: 800px;
  margin: 0 auto;
  font-size: 18px;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

.title {
  font-size: 30px;
  text-decoration: underline;
  margin-bottom: 30px;
  text-align: center;
}

.logout-link,
.btn-dark {
  text-align: center;
  text-decoration: none;
  color: #fff;
  background-color: #343a40;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px; /* Adjust the font size */
}

.logout-link:hover,
.btn-dark:hover {
  background-color: #23272b;
}

.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  margin-bottom: 10px;
}

.product-link {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

.product-link:hover {
  text-decoration: underline;
}

.no-products {
  font-style: italic;
  color: #888;
  font-size: 17px;
}

.new-product,
.edit-category {
  margin-top: 20px;
  border: 1px solid white;
  padding: 15px;
  border-radius: 5px;
  background-color: white;
}

.form-group {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
}

.form-column {
  flex: 1;
  margin-right: 10px;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.form-cat-input {
  height: 30px;
  width: 50%;
  margin-right: 30px;
}
.form-input,
.form-select,
.form-input-half {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.create-button,
.edit-button {
  background-color: #28a745;
  color: #fff;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px; /* Adjust the font size */
}

.create-button:hover,
.edit-button:hover {
  background-color: #218838;
}
</style>
