<template>
  <div id="app" class="manager-signup">
    <h2 class="signup-title bi bi-person-fill">Manager Signup</h2>
    <form class="signup-form">
      <label for="email" class="form-label">Email:</label>
      <input
        type="email"
        v-model="formData.email"
        class="form-input"
        required
      />

      <label for="username" class="form-label">Username:</label>
      <input
        type="text"
        v-model="formData.username"
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

      <label for="cpassword" class="form-label">Confirm Password:</label>
      <input
        type="password"
        v-model="formData.cpassword"
        class="form-input"
        required
      />

      <button @click.prevent="ManagerRegister" class="signup-button">
        Register
      </button>
      <router-link to="/manager_login" class="login-link">
        Already have an account? Login here.
      </router-link>

      <router-link to="/" id="bottom-back-link"> Back </router-link>
    </form>
  </div>
</template>

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

.manager-signup {
  text-align: center;
}

.signup-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
  text-decoration: underline;
}

.signup-form {
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
}

.signup-button {
  background-color: #4caf50;
  color: #fff;
  border: none;
  padding: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  width: 100px;
  margin-left: 170px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

.signup-button:hover {
  background-color: #00b3187a;
}

.login-link {
  text-decoration: none;
  color: black;
  cursor: pointer;
  margin: 10px;
}

#bottom-back-link {
  margin-top: 20px;
  display: block;
  cursor: pointer;
  padding: 5px;
  width: 60px;
  background-color: black;
  text-decoration: none;
  color: white;
}
</style>
<script>
export default {
  name: "ManagerSignup",
  data() {
    return {
      formData: {
        email: "",
        password: "",
        cpassword: "",
        username: "",
      },
    };
  },
  methods: {
    async ManagerRegister() {
      if (this.formData.password !== this.formData.cpassword) {
        console.log("Passwords do not match");
        return;
      }
      const res = await fetch("http://localhost:5000/api/manager_signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.formData),
      });
      const data = await res.json();
      if (res.ok) {
        alert(data.message);
        this.$router.push("/");
      } else {
        this.error = data.message;
        alert(this.error);
      }
    },
  },
};
</script>
