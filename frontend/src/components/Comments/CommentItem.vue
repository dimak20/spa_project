<template>
  <div class="comment-item">
    <div class="comment-header">
      <div v-if="avatarUrl">
        <img :src="avatarUrl" alt="User Avatar" class="avatar"/>
      </div>
      <p>
        <strong>{{ comment.user.username }}</strong>
        <span class="comment-date">{{ formattedDate }}</span>
      </p>
    </div>

    <p class="comment-text" v-html="safeHtml"></p>

    <div v-if="comment.attached_image">
      <img
          :src="comment.attached_image"
          alt="Attached photo"
          class="attached-photo"
          @click="openImage(comment.attached_image)"
      />
    </div>
    <div v-if="comment.attached_file">
      <a :href="comment.attached_file" target="_blank">Download attached file</a>
    </div>
    <span v-if="comment.home_page">
      <a :href="comment.home_page" target="_blank">{{ comment.home_page }}</a>
    </span>

    <button @click="toggleReplyForm" :class="{ 'cancel-button': showReplyForm }">
      {{ showReplyForm ? 'Cancel' : 'Reply' }}
    </button>

    <div v-if="showReplyForm" class="reply-form">
      <!-- Tag toolbar -->
      <div class="tags-toolbar">
        <button class="tag-button" @click="insertTag('<a href=\'\' title=\'\'>', '</a>')">A</button>
        <button class="tag-button" @click="insertTag('<code>', '</code>')">Code</button>
        <button class="tag-button" @click="insertTag('<i>', '</i>')">Italic</button>
        <button class="tag-button" @click="insertTag('<strong>', '</strong>')">Bold</button>
      </div>

      <textarea
          ref="replyTextarea"
          v-model="replyText"
          placeholder="Write your reply"
          required
      ></textarea>

      <!-- CAPTCHA placeholder -->
      <div v-if="showRecaptcha">
        <div class="g-recaptcha" :data-sitekey="siteKey" ref="recaptcha"></div>
      </div>

      <button
          v-if="!showRecaptcha"
          @click="renderRecaptcha"
          :disabled="!replyText.trim()"
      >
        Submit Reply
      </button>

      <button
          v-else
          @click="submitReply"
          :disabled="!captchaVerified || !replyText.trim()"
      >
        Confirm Submission
      </button>
    </div>

    <div class="replies" v-if="comment.replies && comment.replies.length">
      <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          @new-reply="handleNewReply"
      />
    </div>

    <div v-if="isViewerVisible" class="image-viewer" @click="closeImage">
      <img :src="currentImage" alt="Full-size image"/>
    </div>
  </div>
</template>

<script>
import DOMPurify from "dompurify";
import defaultAvatar from "@/assets/images/default_avatar.jpg";

export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },
  computed: {
avatarUrl() {
  const apiUrl = import.meta.env.VITE_APP_API_URL;
  const profileImage = this.comment.user.profile_image;

  if (!profileImage || profileImage.trim() === '' || profileImage === 'null') {
    return defaultAvatar;
  }

  // Если profileImage уже содержит абсолютный URL, возвращаем его как есть
  if (profileImage.startsWith('http://') || profileImage.startsWith('https://')) {
    return profileImage;
  }

  // Иначе обрабатываем как относительный путь
  const sanitizedProfileImage = profileImage.startsWith('/')
    ? profileImage.slice(1)
    : profileImage;

  const sanitizedApiUrl = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;

  return `${sanitizedApiUrl}/${sanitizedProfileImage}`;
},
    safeHtml() {
      return DOMPurify.sanitize(this.comment.text);
    },
    formattedDate() {
      const date = new Date(this.comment.created_at);
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return date.toLocaleDateString("en-US", options);
    },
  },
  mounted() {
    this.siteKey = import.meta.env.VITE_SITE_KEY || '';
  },
  data() {
    return {
      showReplyForm: false,
      replyText: "",
      isViewerVisible: false,
      currentImage: null,
      captchaVerified: false,
      captchaResponse: null,
      showRecaptcha: false,
      siteKey: "",
    };
  },
  methods: {
    toggleReplyForm() {
      this.showReplyForm = !this.showReplyForm;
      this.captchaVerified = false; //
      this.showRecaptcha = false;  //
    },
    renderRecaptcha() {
      this.showRecaptcha = true;

      this.$nextTick(() => {
        if (window.grecaptcha) {
          window.grecaptcha.render(this.$refs.recaptcha, {
            sitekey: this.siteKey,
            callback: this.onCaptchaVerified,
          });
        } else {
          this.loadRecaptchaScript(() => {
            window.grecaptcha.render(this.$refs.recaptcha, {
              sitekey: this.siteKey,
              callback: this.onCaptchaVerified,
            });
          });
        }
      });
    },
    loadRecaptchaScript(callback) {
      const script = document.createElement("script");
      script.src = `https://www.google.com/recaptcha/api.js?render=explicit`;
      script.async = true;
      script.onload = callback;
      document.head.appendChild(script);
    },
    onCaptchaVerified(response) {
      this.captchaVerified = !!response; //
      this.captchaResponse = response;  //
    },
    async submitReply() {
      if (!this.replyText.trim() || !this.captchaVerified) return;

      try {
        const response = await fetch(
            `${import.meta.env.VITE_APP_API_URL}api/v1/comments/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
              },
              body: JSON.stringify({
                text: this.replyText,
                parent: this.comment.id,
                captcha: this.captchaResponse,
              }),
            }
        );
        if (response.ok) {
          const newReply = await response.json();
          this.replyText = "";
          this.showReplyForm = false;
          this.showRecaptcha = false;

          this.$parent.fetchComments(this.$parent.currentPage);

        } else {
          console.error("Failed to submit reply");
        }
      } catch (error) {
        console.error("Error submitting reply:", error);
      }
    },
    handleNewReply(newReply) {
      if (!this.comment.replies) {
        this.$set(this.comment, "replies", []);
      }
      this.comment.replies.push(newReply);
    },
    openImage(imageUrl) {
      this.currentImage = imageUrl;
      this.isViewerVisible = true;
    },
    closeImage() {
      this.currentImage = null;
      this.isViewerVisible = false;
    },
    insertTag(openTag, closeTag) {
      const textarea = this.$refs.replyTextarea;
      if (!textarea) {
        console.error("Textarea ref not found");
        return;
      }
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;

      const textBefore = this.replyText.substring(0, start);
      const textAfter = this.replyText.substring(end);

      const selectedText = this.replyText.substring(start, end);
      const newText = `${textBefore}${openTag}${selectedText}${closeTag}${textAfter}`;

      this.replyText = newText;

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
.comment-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.comment-header {
  display: flex;
  align-items: center;
}

.comment-header .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-header .comment-date {
  margin-left: 10px;
  font-size: 0.9rem;
  color: #555;
}

.comment-text {
  margin-top: 5px;
}

.reply-form {
  margin-top: 10px;
}

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

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.attached-photo {
  max-width: 100px;
  margin-top: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.attached-photo:hover {
  transform: scale(1.1);
}

.replies {
  margin-top: 10px;
  padding-left: 20px;
  border-left: 2px solid #ddd;
}

.image-viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.image-viewer img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 8px;
}

.tags-toolbar {
  display: flex;
  gap: 5px;
}

.tag-button {
  background-color: #ddd;
  border: none;
  padding: 5px;
  cursor: pointer;
}

.tag-button:hover {
  background-color: #bbb;
}
</style>
