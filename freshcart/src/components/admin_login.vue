<template>
  <div id="app">
    <h2 class="login-title bi bi-person-fill">Admin Login</h2>
    <form class="login-form">
      <label for="email" class="form-label">Email:</label>
      <input
        type="email"
        v-model="formData.email"
        class="form-input"
        required
      />

      <label for="password" class="form-label">Password:</label>
      <input
        type="password"
        v-model="formData.password"
        class="form-input"
        required
      />

      <button @click.prevent="adminLogin" class="login-button">Login</button>
      <router-link
        to="/"
        class="logout-link"
        @click="logout"
        id="bottom-back-link"
      >
        Back
      </router-link>
    </form>
  </div>
</template>

<script>
export default {
  name: "AdminLogin",
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
    };
  },
  methods: {
    async adminLogin() {
      const response = await fetch(
        "http://localhost:5000/login?include_auth_token",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.formData),
        }
      );
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        localStorage.setItem(
          "auth-token",
          data.response.user.authentication_token
        );
        this.$router.push(`/admin_dashboard/${this.formData.email}`);
      } else {
        alert("Wrong Password or Email");
      }
    },
  },
};
</script>
<style scoped>
#app {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 10px 10px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  background: linear-gradient(to right, #a9f160, #87cefa);
  margin-top: 100px;
  text-align: center;
}

h2,
h3 {
  text-decoration: underline;
}

.login-title {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 8px;
  color: #555;
}

.form-input {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  align-content: center;
}

.login-button {
  background-color: #4caf50;
  color: #fff;
  border: none;
  padding: 10px;
  width: 60px;
  margin-left: 170px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #45a049;
}

#bottom-back-link {
  margin-top: 20px;
  display: block;
  cursor: pointer;
  padding: 5px;
  width: 60px;
  background-color: black;
  text-decoration: none;
  color: rgb(250, 247, 247);
}
</style>
