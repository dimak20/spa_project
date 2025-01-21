<template>
  <div class="register-page">
    <h2>Register</h2>
    <form @submit.prevent="registerUser" enctype="multipart/form-data">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="first_name">First name:</label>
        <input type="text" id="first_name" v-model="first_name" />
      </div>
      <div>
        <label for="last_name">Last name:</label>
        <input type="text" id="last_name" v-model="last_name" />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
      </div>
      <div>
        <label for="profile_image">Profile Picture:</label>
        <input type="file" id="profile_image" @change="handleFileUpload" />
      </div>
      <button type="submit">Register</button>
    </form>

    <!-- Error display -->
    <div v-if="errorMessages.length" class="error-message">
      <ul>
        <li v-for="(message, index) in errorMessages" :key="index">{{ message }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      confirmPassword: '',
      profile_image: null,  // We store the avatar file
      errorMessages: [], // Array for storing error messages
    };
  },
  methods: {
    handleFileUpload(event) {
      // Getting the selected file
      this.profile_image = event.target.files[0];
    },
    async registerUser() {
      if (this.password !== this.confirmPassword) {
        this.errorMessages = ['Passwords do not match'];
        return;
      }

      // We create FormData to send data with a file
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('first_name', this.first_name);
      formData.append('last_name', this.last_name);
      formData.append('email', this.email);
      formData.append('password', this.password);
      if (this.profile_image) {
        formData.append('profile_image', this.profile_image);
      }

      try {
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}api/v1/accounts/register/`, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          this.$router.push('/login'); // Redirect to login page after successful registration
        } else if (response.status === 400) {
          // Error handling if the server returned status 400 (invalid data)
          const data = await response.json();

          // Retrieving all error messages
          this.errorMessages = [];
          for (const [field, messages] of Object.entries(data)) {
            messages.forEach(message => {
              this.errorMessages.push(`${field}: ${message}`);
            });
          }
        } else {
          this.errorMessages = ['An error occurred. Please try again.']; // Common error for other codes
        }
      } catch (error) {
        this.errorMessages = ['An error occurred. Please try again.']; // Handling an error when sending
      }
    },
  },
};
</script>

<style scoped>
.register-page {
  max-width: 400px;
  margin: 0 auto;
}

form {
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 10px;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.error-message ul {
  list-style-type: none;
  padding: 0;
}
</style>
