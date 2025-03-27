<template>
  <div id="app" class="welcome-container">
    <h2 class="welcome-title">Welcome to FreshCart</h2>
    <div class="row">
      <div class="col-md-6">
        <router-link to="/admin_login" class="welcome-link"
          >Admin Login</router-link
        >
      </div>
      <div class="col-md-6">
        <router-link to="/user_login" class="welcome-link"
          >User Login</router-link
        >
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <router-link to="/manager_login" class="welcome-link"
          >Manager Login</router-link
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  text-align: center;
}

.welcome-title {
  font-size: 36px;
  margin-bottom: 20px;
  color: #0c0101;
  text-decoration: underline;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.col-md-6 {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
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
.col-md-6:hover {
  transform: scale(1.05);
}

h3 {
  color: #333;
}

.welcome-link {
  font-size: 18px;
  text-decoration: none;
  color: #007bff;
  transition: color 0.3s ease;
}

.welcome-link:hover {
  color: #0056b3;
}
</style>

<script>
export default {
  name: "WelCome",
};
</script>
