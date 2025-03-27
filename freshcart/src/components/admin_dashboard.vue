<template>
  <div id="app">
    <nav class="navbar">
      <h1 class="dashboard-title">Admin Dashboard</h1>
      <router-link
        to="/"
        @click="logout"
        class="logout-link bi bi-box-arrow-in-right"
      ></router-link>
    </nav>

    <section class="dashboard-section">
      <div class="request-section">
        <h3>Manager Requests</h3>
        <div v-if="requests.length !== 0">
          <ol class="category-list">
            <li v-for="request in requests" :key="request.request_id">
              <span>
                <strong>Requester's Username:</strong>
                {{ request.requesters_name }}</span
              >
              <div>
                <button
                  class="edit"
                  @click="approveRequest(request.request_id)"
                >
                  Approve
                </button>
                <button
                  class="delete"
                  @click="declineRequest(request.request_id)"
                >
                  Decline
                </button>
              </div>
            </li>
            <br />
          </ol>
        </div>
        <div v-else>
          <p>No requests available.</p>
        </div>
      </div>

      <div class="request-section">
        <h3>Category Requests</h3>
        <div v-if="cat_requests.length !== 0">
          <ul>
            <li v-for="request in cat_requests" :key="request.req_id">
              <span
                ><strong>Requester's Username:</strong>
                {{ request.requesters_name }}
                <br />
                <strong>Requested Category:</strong>
                {{ request.category_name }}</span
              >
              <div>
                <button class="edit" @click="approveCatRequest(request.req_id)">
                  Approve
                </button>
                <button
                  class="delete"
                  @click="declineCatRequest(request.req_id)"
                >
                  Decline
                </button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No requests available.</p>
        </div>
      </div>

      <div class="request-section">
        <h3>Category Update Requests</h3>
        <div v-if="cat_update_requests.length !== 0">
          <ul>
            <li
              v-for="request in cat_update_requests"
              :key="request.category_id"
            >
              <span
                ><strong>Requester's Username:</strong>
                {{ request.requesters_name }} <br /><strong
                  >Requested Category name:</strong
                >
                {{ request.category_name }}<br /><strong
                  >Requested Category to Edit:</strong
                >
                {{ request.category_old_name }}</span
              >
              <div>
                <button
                  class="edit"
                  @click="approveCatUpdateRequest(request.category_id)"
                >
                  Approve
                </button>
                <button
                  class="delete"
                  @click="declineCatUpdateRequest(request.category_id)"
                >
                  Decline
                </button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p class="no-requests">No requests available.</p>
        </div>
      </div>

      <div class="request-section">
        <h3>Category Delete Requests</h3>
        <div v-if="cat_delete_requests.length !== 0">
          <ul>
            <li
              v-for="request in cat_delete_requests"
              :key="request.category_id"
            >
              <span
                ><strong>Requester's Username:</strong>
                {{ request.requesters_name }} <br />
                <strong>Requested Category:</strong> {{ request.category_name }}
              </span>
              <div>
                <button
                  class="edit"
                  @click="approveCatDeleteRequest(request.category_id)"
                >
                  Approve
                </button>
                <button
                  class="delete"
                  @click="declineCatDeleteRequest(request.category_id)"
                >
                  Decline
                </button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No requests available.</p>
        </div>
      </div>

      <div class="category-section">
        <h3>Add categrory</h3>
        <button @click="showAddCategoryForm">Add New Category</button>

        <div v-if="showCategoryForm" class="category-form">
          <form>
            <label for="category_name">Category Name:</label>
            <input type="text" v-model="formData.category_name" required />
            <button @click.prevent="addCategory">Add Category</button>
          </form>
        </div>
      </div>
      <div class="category-section">
        <h3>Category</h3>
        <ul v-if="categories.length !== 0">
          <li v-for="category in categories" :key="category.id">
            {{ category.name }}
            <div>
              <label for="category_name">Category Name:</label>
              <input
                type="text"
                v-model="categoryNames[category.id]"
                required
              />
              <button class="edit" @click.prevent="editcategory(category.id)">
                Edit
              </button>
            </div>
            <button class="delete" @click="deleteCategory(category.id)">
              Delete
            </button>
            <button class="edit" @click="viewProducts(category.id)">
              View Products
            </button>
          </li>
        </ul>
        <p v-else>No category available.</p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      account: {
        username: "",
        email: "",
        id: null,
        roles: [],
      },
      requests: [],
      cat_requests: [],
      cat_update_requests: [],
      cat_delete_requests: [],
      categories: [],
      showCategoryForm: false,
      showeditCategoryForm: false,
      formData: {
        category_name: "",
      },
      fta: {
        category_name: "",
      },
      categoryNames: {},
      error: "Something Went Wrong",
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
    const response = await fetch(
      `http://localhost:5000/api/admin_dashboard/${email}`,
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
      this.requests = Array.isArray(data) ? data : [];
    } else {
      this.error = data.message;
      alert(this.error);
      this.$router.push("/");
    }

    const cr_response = await fetch(
      "http://localhost:5000/api/categoryRequests",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      }
    );
    const cat_data = await cr_response.json();
    console.log(cat_data);
    if (cr_response.ok) {
      this.cat_requests = Array.isArray(cat_data) ? cat_data : [];
    }

    const cur_response = await fetch(
      "http://localhost:5000/api/categoryUpdateRequests",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      }
    );
    const cat_update_data = await cur_response.json();
    console.log(cat_update_data);
    if (cur_response.ok) {
      this.cat_update_requests = Array.isArray(cat_update_data)
        ? cat_update_data
        : [];
    }

    const cdr_response = await fetch(
      "http://localhost:5000/api/categoryDeleteRequests",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      }
    );
    const cat_delete_data = await cdr_response.json();
    console.log(cat_delete_data);
    if (cdr_response.ok) {
      this.cat_delete_requests = Array.isArray(cat_delete_data)
        ? cat_delete_data
        : [];
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
    if (c_response.ok) {
      this.categories = Array.isArray(c_data) ? c_data : [];
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
    isProductOwner() {
      return this.$store.state.currentUserId == this.product.user_id;
    },
    isUser() {
      return this.account.roles.includes("<Role 2>");
    },
  },

  methods: {
    viewProducts(categoryId) {
      this.$router.push(`/getProductsPage/${categoryId}`);
    },
    async declineCatRequest(requestId) {
      try {
        const shouldDecline = window.confirm(
          "Are you sure you want to decline the category request?"
        );

        if (!shouldDecline) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/declineCatRequest/${requestId}`,
          {
            method: "delete",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.cat_requests = data.requests;
          alert("Successfully Deleted Request");
        } else {
          alert("Something went wrong");
        }
      } catch {
        alert("Something went wrong");
      }
    },
    async declineCatDeleteRequest(categoryId) {
      try {
        const shouldDecline = window.confirm(
          "Are you sure you want to decline the deletion request for this category?"
        );

        if (!shouldDecline) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/declineCatDeleteRequest/${categoryId}`,
          {
            method: "delete",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.cat_delete_requests = data.requests;
          alert("Successfully Deleted Request");
        } else {
          alert("Something went wrong");
        }
      } catch {
        alert("Something went wrong");
      }
    },
    async declineRequest(requestId) {
      try {
        const shouldDecline = window.confirm(
          "Are you sure you want to decline the request?"
        );

        if (!shouldDecline) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/declineRequest/${requestId}`,
          {
            method: "delete",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.requests = data;
          alert("Successfully Deleted Request");
        } else {
          alert("Something went wrong");
        }
      } catch {
        alert("Something went wrong");
      }
    },
    async approveCatRequest(requestId) {
      try {
        const shouldApprove = window.confirm(
          "Are you sure you want to approve the category request?"
        );

        if (!shouldApprove) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/approveCatRequest/${requestId}`,
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.cat_requests = data.requests;
          this.categories = data.categories;
        } else {
          alert("Category Already Exists");
        }
      } catch {
        alert("Soomething went wrong");
      }
    },
    async declineCatUpdateRequest(categoryId) {
      try {
        const shouldDecline = window.confirm(
          "Are you sure you want to decline the update request for this category?"
        );

        if (!shouldDecline) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/declineCatUpdateRequest/${categoryId}`,
          {
            method: "delete",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.cat_update_requests = data.requests;
          alert("Successfully Deleted Request");
        } else {
          alert("Something went wrong");
        }
      } catch {
        alert("Something went wrong");
      }
    },

    async approveRequest(requestId) {
      try {
        const shouldApprove = window.confirm(
          "Are you sure you want to approve the request?"
        );

        if (!shouldApprove) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/approveRequest/${requestId}`,
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.requests = data;
        } else {
          alert("Something went wrong");
        }
      } catch {
        alert("Soomething went wrong");
      }
    },

    async approveCatDeleteRequest(categoryId) {
      try {
        const shouldApprove = window.confirm(
          "Are you sure you want to approve the deletion request for this category?"
        );

        if (!shouldApprove) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/approveCatDeleteRequest/${categoryId}`,
          {
            method: "delete",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.cat_delete_requests = data.requests;
          this.categories = data.categories;
        } else {
          alert(data.error);
        }
      } catch {
        alert("Something went wrong");
      }
    },
    async approveCatUpdateRequest(categoryId) {
      try {
        const shouldApprove = window.confirm(
          "Are you sure you want to approve the update request for this category?"
        );

        if (!shouldApprove) {
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/approveCatUpdateRequest/${categoryId}`,
          {
            method: "put",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          this.cat_update_requests = data.requests;
          this.categories = data.categories;
        } else {
          alert("Category Already Exists");
        }
      } catch {
        alert("Soomething went wrong");
      }
    },

    showAddCategoryForm() {
      this.showCategoryForm = !this.showCategoryForm;
    },
    showEditCategoryForm() {
      this.showeditCategoryForm = !this.showeditCategoryForm;
    },
    async addCategory() {
      try {
        if (!this.formData.category_name.trim()) {
          alert("Please enter a category name before adding.");
          return;
        }

        const shouldAdd = window.confirm(
          "Are you sure you want to add this category?"
        );

        if (!shouldAdd) {
          return; // If user cancels, do nothing
        }

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
          this.categories = data.categories;
          this.formData.category_name = "";
          this.showCategoryForm = false;
        } else {
          alert("Category Already Exists");
        }
      } catch {
        alert("Soomething went wrong");
      }
    },

    async editcategory(c_id) {
      try {
        const categoryInput = this.categoryNames[c_id];

        if (!categoryInput) {
          alert("Please enter a category name before editing.");
          return;
        }

        const categoryName = categoryInput.trim();

        if (!categoryName) {
          alert("Please enter a non-empty category name before editing.");
          return;
        }

        const shouldEdit = window.confirm(
          "Are you sure you want to edit this category?"
        );

        if (!shouldEdit) {
          return;
        }

        const formdata = new FormData();
        formdata.append("category_name", categoryName);

        const response = await fetch(
          `http://localhost:5000/api/editCategory/${c_id}`,
          {
            method: "PUT",
            headers: {
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
            body: formdata,
          }
        );

        const data = await response.json();
        console.log(data);

        if (response.ok) {
          alert("Category updated successfully!");
          this.categoryNames[c_id] = "";
          this.categories = data.categories;
        } else {
          alert("category Already Exists");
        }
      } catch {
        alert("Soomething went wrong");
      }
    },
    async checkCategoryExists(categoryName) {
      try {
        const response = await fetch(
          `http://localhost:5000/api/checkCategoryExists?category_name=${categoryName}`,
          {
            method: "get",
            headers: {
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );

        const data = await response.json();
        return data.exists;
      } catch {
        return false;
      }
    },
    async deleteCategory(c_id) {
      try {
        const shouldDelete = window.confirm(
          "Are you sure you want to delete this category?"
        );

        if (!shouldDelete) {
          return;
        }

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

        if (response.ok) {
          const data = await response.json();
          this.categories = data.categories;
        } else {
          const data = await response.json();
          alert(data.error);
        }
      } catch {
        alert("Failed to delete");
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
span {
  color: #0b7939;
}
strong {
  color: black;
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

.dashboard-section {
  margin: 20px;
}

.request-section,
.category-section {
  margin-bottom: 30px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: whitesmoke;
}

.category-section button,
.category-section input {
  margin-top: 10px;
}

.request-section h3,
.category-section h3 {
  color: black;
}

li {
  margin: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.request-section button.edit {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 4px;
  cursor: pointer;
}

.request-section button.delete {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 4px;
  cursor: pointer;
}
.category-section input {
  margin-right: 10px;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.category-section button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 5px;
}

.category-list li {
  list-style-type: circle;
  margin: 5px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-section button.edit {
  background-color: #2ecc71;
}

.category-section li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-section div {
  display: flex;
  align-items: center;
}

.category-section button.delete {
  background-color: #e74c3c;
  margin-left: 10px;
}

.category-section p {
  color: #888;
  margin-top: 10px;
}
</style>
