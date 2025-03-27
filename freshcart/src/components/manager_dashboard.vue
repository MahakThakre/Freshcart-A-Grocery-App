<template>
  <div id="app">
    <nav class="navbar">
      <h1 class="dashboard-title">Manager Dashboard</h1>
      <router-link to="/" class="logout-link" @click="logout">
        Logout
      </router-link>
    </nav>

    <div class="category-section">
      <h2>Create Categories</h2>
      <ul v-if="approvedCategories.length !== 0" class="category-list">
        <li
          v-for="category in approvedCategories"
          :key="category.id"
          class="category-item"
        >
          <router-link
            :to="{
              name: 'category_products',
              params: { category_id: category.id },
            }"
            class="category-link"
          >
            <strong> {{ category.name }}</strong>
          </router-link>
          <button @click.prevent="deleteCategory(category.id)" class="delete">
            Delete Category Request
          </button>
        </li>
      </ul>
      <p v-else class="no-categories">No approved categories available.</p>
    </div>

    <div class="category-section">
      <h2>Create New Category</h2>
      <label for="category_name" class="form-label">Category Name:</label>
      <input
        type="text"
        v-model="formData.category_name"
        required
        class="form-input"
      />
      <button @click.prevent="createCategory" class="add">
        Create Category Request
      </button>
    </div>

    <button @click="exportManagerCSV" class="export-csv">Export Csv</button>
  </div>
</template>

<script>
export default {
  name: "ManagerDashboard",
  data() {
    return {
      account: {
        username: "",
        email: "",
        id: null,
        roles: [],
      },
      approvedCategories: [],
      formData: {
        category_name: "",
      },
      fta: {
        category_name: "",
      },
    };
  },
  async mounted() {
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
    const c_response = await fetch("http://localhost:5000/api/getCategory", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": localStorage.getItem("auth-token"),
      },
    });
    const c_data = await c_response.json();
    console.log(c_data);
    if (c_response.ok && this.account.roles.includes("<Role 2>")) {
      this.approvedCategories = Array.isArray(c_data) ? c_data : [];
    } else {
      alert("Something went wrong");
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
    isManager() {
      return this.account.roles.includes("<Role 2>");
    },
  },
  methods: {
    async createCategory() {
      const shouldCreate = window.confirm(
        "Are you sure you want to create this category request?"
      );
      if (!shouldCreate) {
        return;
      }
      try {
        const formdata = new FormData();
        formdata.append("category_name", this.formData.category_name);
        const response = await fetch("http://localhost:5000/api/addCategory", {
          method: "post",
          headers: {
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: formdata,
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          alert("Category creation request sent successfully!");
          this.formData.category_name = "";
        } else {
          alert(
            "Failed to send category creation request, Category Already Exists"
          );
          this.formData.category_name = "";
        }
      } catch (error) {
        console.error("Error creating category:", error);
        alert("An error occurred while creating the category.");
      }
    },
    async deleteCategory(c_id) {
      const shouldDelete = window.confirm(
        "Are you sure you want to delete this category request?"
      );
      if (!shouldDelete) {
        return;
      }
      try {
        const response = await fetch(
          `http://localhost:5000/api/deleteCategory/${c_id}`,
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
          alert("Delete Request Sent Successfully");
          this.categories = data.categories;
        } else {
          alert("Unable to send delete request.Try again!");
        }
      } catch (error) {
        console.error(error);
        alert("Failed to send delete request. Try again!");
      }
    },

    async exportManagerCSV() {
      try {
        const user_id = this.$store.state.currentUserId;
        const response = await fetch(
          `http://localhost:5000/export_manager_csv/${user_id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
            responseType: "blob",
          }
        );
        if (response.ok) {
          const csvShop = await response.blob();
          const csvUrl = URL.createObjectURL(csvShop);
          const a = document.createElement("a");
          a.href = csvUrl;
          a.download = `${user_id}_data.csv`;
          a.click();
          alert("CSV export job started");
        } else {
          alert("Failed to start CSV export job");
        }
      } catch (error) {
        console.error(error);
        alert("Failed to start CSV export job");
      }
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
  justify-content: space-between;
  align-items: center;
  background-color: #4caf50;
  color: white;
  padding: 10px;
}

.logout-link {
  color: white;
  text-decoration: none;
  padding: 5px 10px;
  background-color: #333;
  border-radius: 5px;
}

.category-section {
  margin-bottom: 30px;
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: whitesmoke;
}

.category-list {
  list-style: none;
  padding: 0;
}

.category-item {
  margin: 5px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-link {
  text-decoration: none;
  color: #333;
}

.delete,
.add,
.export-csv {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 4px 2px;
  cursor: pointer;
}

.delete:hover,
.add:hover,
.export-csv:hover {
  background-color: #45a049;
}
.form-input {
  width: 300px;
  height: 30px;
  border: 1px solid black;
  border-radius: 4px;
}
</style>
