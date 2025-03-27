<template>
  <div id="app">
    <div style="margin-left: 550px; margin-top: -10px">
      <router-link to="/" class="logout-link" @click="logout">
        Logout </router-link
      >&nbsp;&nbsp;
      <router-link :to="'/category_products/' + category_id" class="btn-dark"
        >Back</router-link
      >
    </div>
    <div class="edit-product">
      <h3 class="title">Product Details</h3>

      <div class="product-details">
        <div class="detail-item"><strong>Name:</strong> {{ product.name }}</div>
        <div class="detail-item">
          <strong>Manufacture Date:</strong>
          {{
            product.manufacture_date
              ? product.manufacture_date
              : "Not Available"
          }}
        </div>
        <div class="detail-item">
          <strong>Expiry Date:</strong>
          {{ product.expiry_date ? product.expiry_date : "Not Available" }}
        </div>

        <div class="detail-item">
          <strong>Price:</strong> {{ product.price }}
        </div>
        <div class="detail-item">
          <strong>Rate per Unit:</strong> {{ product.rate_per_unit }}
        </div>
        <div class="detail-item">
          <strong>Stock:</strong> {{ product.stock }}
        </div>
        <div class="detail-item">
          <strong>Category:</strong> {{ product.category.name }}
        </div>
        <div>
          <button
            v-if="isProductOwner"
            class="delete"
            @click="confirmDeleteProduct(product.id)"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    <div v-if="isProductOwner" class="edit-product">
      <h3 class="title">Edit Product</h3>
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
            required
            class="form-input"
          />
        </div>
      </div>
      <div class="form-group">
        <div class="form-column">
          <label for="rate_per_unit" class="form-label">Rate per Unit:</label>
          <select v-model="formData.rate_per_unit" class="form-select">
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
      <button @click.prevent="editProduct(product.id)" class="create-button">
        Edit Product
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "SingleProduct",
  data() {
    return {
      product: {
        id: 0,
        user_id: 0,
        name: "",
        manufacture_date: "",
        expiry_date: "",
        price: 0,
        rate_per_unit: "",
        stock: 0,
        category: {
          name: "",
          id: 0,
        },
      },
      formData: {
        product_name: "",
        manufacture_date: "",
        expiry_date: "",
        price: 0,
        rate_per_unit: "",
        stock: 0,
      },
    };
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
      this.formData.product_name = data.name;
      this.formData.manufacture_date = data.manufacture_date;
      this.formData.expiry_date = data.expiry_date;
      this.formData.price = data.price;
      this.formData.rate_per_unit = data.rate_per_unit;
      this.formData.stock = data.stock;
    } else {
      alert("Failed to display");
    }
  },
  computed: {
    category_id() {
      return this.$route.params.category_id;
    },
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
  methods: {
    async deleteProduct(p_id) {
      const category_id = this.$route.params.category_id;
      const response = await fetch(
        `http://localhost:5000/api/deleteProduct/${p_id}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        this.$router.push(`/category_products/${category_id}`);
      }
    },

    confirmDeleteProduct(p_id) {
      const isConfirmed = window.confirm(
        "Are you sure you want to delete this product?"
      );
      if (isConfirmed) {
        this.deleteProduct(p_id);
      }
    },
    async editProduct(p_id) {
      const isConfirmed = window.confirm(
        "Are you sure you want to edit this product?"
      );
      if (!isConfirmed) {
        return;
      }
      if (!this.formData.manufacture_date) {
        this.formData.manufacture_date = "Not Available";
      }

      if (!this.formData.expiry_date) {
        this.formData.expiry_date = "Not Available";
      }
      const formdata = new FormData();
      formdata.append("product_name", this.formData.product_name);
      formdata.append("manufacture_date", this.formData.manufacture_date);
      formdata.append("expiry_date", this.formData.expiry_date);
      formdata.append("price", this.formData.price);
      formdata.append("rate_per_unit", this.formData.rate_per_unit);
      formdata.append("stock", this.formData.stock);
      const _response = await fetch(
        `http://localhost:5000/api/editProduct/${p_id}`,
        {
          method: "PUT",
          headers: {
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: formdata,
        }
      );
      const data = await _response.json();
      console.log(data);
      if (_response.ok) {
        this.product = data;
      } else {
        alert("You are not authorized to edit Product");
      }
    },
    logout() {
      this.$router.push("/");
    },
  },
};
</script>
<style scoped>
#app {
  max-width: 800px;
  margin: 0 auto;
  font-size: 18px;
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

.product-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}
.title {
  font-size: 30px;
  text-decoration: underline;
  margin-bottom: 30px;
  text-align: center;
}

.product-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  text-align: left;
  margin-top: 20px;
}

.detail-item {
  padding: 10px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.detail-item strong {
  margin-right: 8px;
}

.logout-link,
.btn-dark {
  text-decoration: none;
  background-color: black;
  color: #fff;
  padding: 8px;
  border-radius: 4px;
  display: inline-block;
  margin-top: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-link:hover {
  background-color: #0056b3;
}

.new-product,
.edit-product {
  margin-top: 20px;
  border: 1px solid #ddd;
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

.form-input,
.form-select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.create-button,
.delete {
  background-color: #28a745;
  color: #fff;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px;
  margin-top: 10px;
}

.create-button:hover,
.edit-button:hover {
  background-color: #218838;
}
</style>
