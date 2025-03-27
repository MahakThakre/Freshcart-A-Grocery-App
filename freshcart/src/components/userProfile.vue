<!-- UserProfile.vue -->
<template>
  <div class="user-profile-container">
    <h2>User Profile</h2>
    <div class="profile-details">
      <p><strong>Email:</strong> {{ account.email }}</p>
      <p><strong>Username:</strong> {{ account.username }}</p>
    </div>
    <router-link to="/boughtProducts" class="logout-link">Orders</router-link>
  </div>
</template>

<style scoped>
.user-profile-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: linear-gradient(to right, #a9f160, #87cefa);
}

h2 {
  text-align: center;
  color: #333;
}

.profile-details {
  margin-bottom: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
}

p {
  margin: 8px 0;
}

.logout-link {
  display: inline-block;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.logout-link:hover {
  background-color: #0056b3;
}
</style>

<script>
export default {
  name: "UserProfile",
  data() {
    return {
      account: {
        email: "",
        username: "",
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
    try {
      const email = this.$store.state.currentUserEmail;
      const response = await fetch(
        `http://localhost:5000/api/getUserData/${email}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      const data = await response.json();
      if (response.ok) {
        this.account = data;
      } else {
        console.error("Failed to fetch user details");
      }
    } catch (error) {
      console.error("An error occurred while fetching user details", error);
      this.$router.push("/");
    }
  },
};
</script>
