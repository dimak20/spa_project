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
      <input type="file" ref="imageInput" @change="handlePhotoUpload" accept="image/*"/>
    </label>

    <!-- Field for uploading a text file -->
    <label>
      Upload Text File:
      <input type="file" ref="fileInput" @change="handleFileUpload" accept=".txt"/>
    </label>

    <!-- reCAPTCHA -->
    <div
        v-if="showRecaptcha"
        ref="recaptcha"
        id="recaptcha-container"
        class="g-recaptcha">
    </div>

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
      text: "",
      home_page: "",
      attached_image: null,
      attached_file: null,
      errorMessage: "",
      recaptchaToken: "", // Token reCAPTCHA
      siteKey: "", // reCAPTCHA site key
      showRecaptcha: false, // Flag to control the display of reCAPTCHA
    };
  },
  mounted() {
    this.siteKey = import.meta.env.VITE_SITE_KEY || "";

    // Ensure reCAPTCHA script is loaded
    const script = document.createElement("script");
    script.src = "https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit";
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    // Define global callback
    window.onloadCallback = () => {
      console.log("reCAPTCHA script loaded");
    };
  },
  methods: {
    handlePhotoUpload(event) {
      this.attached_image = event.target.files[0];
    },
    handleFileUpload(event) {
      this.attached_file = event.target.files[0];
    },
    renderRecaptcha() {
      if (window.grecaptcha && this.$refs.recaptcha) {
        window.grecaptcha.render(this.$refs.recaptcha, {
          sitekey: this.siteKey,
          callback: this.onRecaptchaSuccess,
        });
        console.log("reCAPTCHA rendered");
      } else {
        console.error("reCAPTCHA placeholder not available or grecaptcha not loaded");
      }
    },
    onRecaptchaSuccess(token) {
      this.recaptchaToken = token;
      console.log("reCAPTCHA verified");
      this.finalizeSubmission();
    },
    async submitComment() {
      this.errorMessage = "";

      if (!this.recaptchaToken) {
        this.showRecaptcha = true;
        this.$nextTick(() => {
          this.renderRecaptcha();
        });
        return;
      }

      this.finalizeSubmission();
    },
    async finalizeSubmission() {
      const formData = new FormData();
      formData.append("text", this.text);
      if (this.home_page) {
        formData.append("home_page", this.home_page);
      }
      if (this.attached_image) {
        formData.append("attached_image", this.attached_image);
      }
      if (this.attached_file) {
        formData.append("attached_file", this.attached_file);
      }
      formData.append("captcha", this.recaptchaToken);

      try {
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}api/v1/comments/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: formData,
        });

        if (response.ok) {
          this.resetForm();
          this.$emit("new-comment");
        } else {
          this.handleError(response);
        }
      } catch (error) {
        console.error("Network error:", error);
        this.errorMessage = "Network error: Unable to connect to the server.";
      }
    },
    resetForm() {
      this.text = "";
      this.home_page = "";
      this.attached_image = null;
      this.attached_file = null;
      this.recaptchaToken = "";
      this.showRecaptcha = false;
      this.errorMessage = "";

      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = "";
      }
      if (this.$refs.imageInput) {
        this.$refs.imageInput.value = "";
      }
    },
    async handleError(response) {
      try {
        const errorResponse = await response.json();

        if (response.status === 400) {
          if (errorResponse.errors || errorResponse) {
            const validationErrors = Object.entries(errorResponse)
                .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
                .join("; ");
            this.errorMessage = `Validation errors: ${validationErrors}`;
          } else if (errorResponse.detail) {
            this.errorMessage = errorResponse.detail;
          } else {
            this.errorMessage = "Bad request: Please check your input.";
          }
        } else if (response.status === 401) {
          this.errorMessage = "Unauthorized: Please log in to post a comment.";
        } else {
          this.errorMessage = `Unexpected error: ${response.status} - ${response.statusText}`;
        }
      } catch (jsonError) {
        const errorText = await response.text();
        this.errorMessage = errorText || `Unexpected error: ${response.status}`;
      }
      console.error(`Error ${response.status}:`, this.errorMessage);
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
