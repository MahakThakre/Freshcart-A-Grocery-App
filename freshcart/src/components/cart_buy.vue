<template>
  <div class="cart-container">
    <h2 style="text-align: center">Your Cart</h2>
    <div v-for="item in cartItems" :key="item.id" class="cart-item">
      <ul>
        <li>
          <div style="justify-content: space-between">
            <p>
              <strong>Product Name: {{ item.product_name }}</strong>
            </p>
            <p>Price: {{ item.product_price }}</p>
            <p>Quantity: {{ item.product_count }}</p>
            <button
              @click="removeFromCart(item.product_id)"
              class="remove-button"
            >
              Remove
            </button>
            <button
              @click="editProductCount(item.product_id, item.newProductCount)"
              class="edit-button"
            >
              Edit
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="cartItems.length !== 0">
      <button @click="promptBeforeBuy" class="buy-button">Buy All</button>
      <p><strong>Total Amount:</strong> {{ total_amount }}</p>
    </div>
    <div v-else>Your Cart is empty.</div>
    <router-link :to="'/user_dashboard/' + currentUserEmail" class="back-button"
      >Back to Dashboard</router-link
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      cartItems: [],
      total_amount: null,
      product: {
        stock: null,
      },
    };
  },
  async mounted() {
    try {
      const response = await fetch("http://localhost:5000/api/cart", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      });
      const data = await response.json();
      console.log(data);

      if (response.ok) {
        this.cartItems = data.cart;
        this.total_amount = data.cart_price;
      }
    } catch (error) {
      console.error("Error fetching cart items:", error);
      alert("Failed to fetch cart items. Please try again later.");
      this.$router.push("/");
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
  methods: {
    async removeFromCart(productId) {
      try {
        const shouldRemove = window.confirm(
          "Are you sure you want to remove this item from your cart?"
        );
        if (!shouldRemove) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/cart/${productId}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();

        if (response.ok) {
          this.cartItems = this.cartItems.filter(
            (item) => item.product_id !== productId
          );
          this.total_amount =
            data.new_total_amount !== null ? data.new_total_amount : 0;

          alert("Item removed from the cart");
          this.$router.push(`/user_dashboard/${this.currentUserEmail}`);
        } else {
          alert("Failed to remove item from the cart");
        }
      } catch (error) {
        console.error("Error removing item from cart:", error);
        alert("Item removed from the cart");
      }
    },

    async buyAll() {
      try {
        const response = await fetch("http://localhost:5000/api/buyCart", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          alert("Items successfully bought!");
          this.cartItems = [];
          this.total_amount = 0;
          this.$router.push(`/user_dashboard/${this.currentUserEmail}`);
        } else {
          alert("Failed to buy items. Please check your cart.");
        }
      } catch (error) {
        console.error("Error buying items:", error);
        alert("Failed to buy items. Please try again later.");
      }
    },

    promptBeforeBuy() {
      const shouldBuy = window.confirm(
        "Are you sure you want to buy all items?"
      );
      if (shouldBuy) {
        this.buyAll();
      }
    },

    async editProductCount(productId, currentProductCount) {
      try {
        const newProductCount = window.prompt(
          "Enter the new quantity:",
          currentProductCount
        );

        if (newProductCount !== null && !isNaN(newProductCount)) {
          const response = await fetch(
            `http://localhost:5000/api/cart/${productId}`,
            {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth-token"),
              },
              body: JSON.stringify({
                product_count: parseInt(newProductCount),
              }),
            }
          );

          const data = await response.json();
          console.log(data);

          if (data.message === "Product count updated successfully") {
            const updatedItem = this.cartItems.find(
              (item) => item.product_id === productId
            );
            if (updatedItem) {
              updatedItem.product_count = parseInt(newProductCount);
            }
            alert("Product count updated successfully");
          } else {
            alert(`Failed to update product count: ${data.message}`);
          }
        } else {
          alert("Invalid input. Please enter a valid number.");
        }
      } catch (error) {
        console.error("Error editing product count:", error);
        alert("Failed to edit product count. Please try again later.");
      }
    },
  },
};
</script>

<style scoped>
.cart-container {
  width: 40%;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

h2 {
  color: #333;
}

.cart-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.remove-button {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.edit-button {
  background-color: #35dc4b;
  color: white;
  padding: 5px 10px;
  border: none;
  margin-left: 5px;
  border-radius: 4px;
  cursor: pointer;
}

.buy-button {
  background-color: #28a745;
  color: white;
  margin-right: 10px;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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
