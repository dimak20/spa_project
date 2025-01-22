<template>
  <form @submit.prevent="submitComment">
    <!-- Error message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Tag button panel -->
    <div class="tags-toolbar">
      <button type="button" @click="insertTag('<a href=\'\' title=\'\'>', '</a>')">A</button>
      <button type="button" @click="insertTag('<code>', '</code>')">Code</button>
      <button type="button" @click="insertTag('<i>', '</i>')">Italic</button>
      <button type="button" @click="insertTag('<strong>', '</strong>')">Bold</button>
    </div>

    <!-- Comment text field -->
    <textarea ref="commentTextarea" v-model="text" placeholder="Add your comment" required></textarea>

    <!-- Home_page input field -->
    <label>
      Your Homepage (optional):
      <input type="url" v-model="home_page" placeholder="https://example.com"/>
    </label>

    <!-- Photo upload field -->
    <label>
      Upload Photo:
      <input type="file" @change="handlePhotoUpload" accept="image/*"/>
    </label>

    <!-- Field for uploading a text file -->
    <label>
      Upload Text File:
      <input type="file" @change="handleFileUpload" accept=".txt"/>
    </label>

    <!-- reCAPTCHA (appears only before submitting) -->
    <div v-if="showRecaptcha" class="g-recaptcha" :data-sitekey="siteKey" ref="recaptcha"></div>

    <!-- Button wrapper -->
    <div>
      <button type="submit">Submit</button>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return {
      text: '',
      home_page: '',
      attached_image: null,
      attached_file: null,
      errorMessage: '',
      recaptchaToken: '', // Token reCAPTCHA
      siteKey: "",
      showRecaptcha: false, // Flag that controls the display of reCAPTCHA
    };
  },
  mounted() {
    this.siteKey = import.meta.env.VITE_SITE_KEY || '';
  },
  methods: {
    handlePhotoUpload(event) {
      this.attached_image = event.target.files[0];
    },
    handleFileUpload(event) {
      this.attached_file = event.target.files[0];
    },
    onRecaptchaChange(token) {
      this.recaptchaToken = token;
    },
    async submitComment() {
      this.errorMessage = '';

      // Show reCAPTCHA before sending
      this.showRecaptcha = true;

      // We initialize reCAPTCHA only before sending
      if (window.grecaptcha && !this.recaptchaToken) {
        grecaptcha.render(this.$refs.recaptcha, {
          sitekey: this.siteKey,
          callback: this.onRecaptchaChange,
        });
      }

      // reCAPTCHA token verification
      if (!this.recaptchaToken) {
        this.errorMessage = 'Please complete the CAPTCHA verification.';
        return;
      }

      const formData = new FormData();
      formData.append('text', this.text);
      if (this.home_page) {
        formData.append('home_page', this.home_page);
      }
      if (this.attached_image) {
        formData.append('attached_image', this.attached_image);
      }
      if (this.attached_file) {
        formData.append('attached_file', this.attached_file);
      }
      formData.append('captcha', this.recaptchaToken); //

      try {
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}api/v1/comments/`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: formData,
        });

        if (response.ok) {
          this.$emit('new-comment');
          this.text = '';
          this.home_page = '';
          this.attached_image = null;
          this.attached_file = null;
          this.recaptchaToken = '';
          this.showRecaptcha = false;
          this.errorMessage = '';
        } else {
          let errorDetails = '';
          try {
            const errorResponse = await response.json();
            if (errorResponse.detail) {
              errorDetails = errorResponse.detail;
            } else if (errorResponse.errors) {
              errorDetails = `Validation errors: ${JSON.stringify(errorResponse.errors)}`;
            }
          } catch (jsonError) {
            errorDetails = await response.text();
          }

          if (response.status === 401) {
            this.errorMessage = errorDetails || 'Unauthorized: Please log in to post a comment.';
          } else if (response.status === 400) {
            this.errorMessage = errorDetails || 'Bad request: Please check your input.';
          } else {
            this.errorMessage = errorDetails || `Unexpected error: ${response.status} - ${response.statusText}`;
          }

          console.error(`Server responded with error: ${response.status} - ${response.statusText}`, errorDetails);
        }
      } catch (error) {
        console.error('Network error:', error);
        this.errorMessage = 'Network error: Unable to connect to the server.';
      }
    },
    insertTag(openTag, closeTag) {
      const textarea = this.$refs.commentTextarea;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;

      const textBefore = this.text.substring(0, start);
      const textAfter = this.text.substring(end);

      const selectedText = this.text.substring(start, end);
      const newText = `${textBefore}${openTag}${selectedText}${closeTag}${textAfter}`;

      this.text = newText;

      this.$nextTick(() => {
        textarea.focus();
        const newPos = start + openTag.length;
        textarea.setSelectionRange(newPos, newPos + selectedText.length);
      });
    },
  },
};
</script>

<style scoped>
textarea {
  width: 100%;
  min-height: 50px;
  margin-bottom: 10px;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
}

button[type="submit"] {
  display: block;
  margin-top: 10px;
}

.error-message {
  color: red;
  margin-bottom: 10px;
  font-weight: bold;
}

/* Tag button panel */
.tags-toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.tags-toolbar button {
  padding: 5px 10px;
  background-color: #ddd;
  cursor: pointer;
}

.tags-toolbar button:hover {
  background-color: #bbb;
}
</style>
