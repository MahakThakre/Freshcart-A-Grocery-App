<template>
  <div id="app" class="user-signup">
    <h2 class="signup-title bi bi-person-fill">User Signup</h2>
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

      <button @click.prevent="UserRegister" class="signup-button">
        Register
      </button>
    </form>

    <div class="bottom-link-container">
      <router-link to="/user_login" class="bottom-link">
        Already have an account? Log in here.
      </router-link>
    </div>

    <router-link to="/" class="bottom-back-link">Back</router-link>
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

.signup-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
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
  margin-left: 170px;
  width: 100px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

.signup-button:hover {
  background-color: #00b3187a;
}

.bottom-link-container {
  margin: 10px;
}

.bottom-link {
  text-decoration: none;
  color: black;
  cursor: pointer;
}

.bottom-back-link {
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

<script>
export default {
  name: "UserSignup",
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
    async UserRegister() {
      if (this.formData.password !== this.formData.cpassword) {
        console.log("Passwords do not match");
        return;
      }
      const res = await fetch("http://localhost:5000/api/user_signup", {
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
