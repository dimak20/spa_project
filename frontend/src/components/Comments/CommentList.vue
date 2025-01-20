<template>
  <div>
    <!-- Comment form -->
    <CommentForm @new-comment="handleNewComment"/>
    <div>
      <!-- Drop-down list for selecting sorting -->
      <div>
        <label for="sort">Sort by:</label>
        <select v-model="sortField" @change="fetchComments(currentPage)">
          <option value="created_at">Date</option>
          <option value="user__username">Username</option>
          <option value="user__email">Email</option>
        </select>

        <label for="order">Order:</label>
        <select v-model="sortOrder" @change="fetchComments(currentPage)">
          <option value="">Ascending</option>
          <option value="-">Descending</option>
        </select>
      </div>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <div v-if="comments.length">
          <CommentItem
              v-for="comment in comments"
              :key="comment.id"
              :comment="comment"
          />
        </div>
        <div v-else>
          <p>No comments available.</p>
        </div>

        <!-- Pagination -->
        <div class="pagination">
          <button
              :disabled="!previousPage"
              @click="goToPage(currentPage - 1)"
          >
            Previous
          </button>
          <span>Page {{ currentPage }}</span>
          <button
              :disabled="!nextPage"
              @click="goToPage(currentPage + 1)"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommentForm from './CommentForm.vue';
import CommentItem from './CommentItem.vue';

export default {
  components: {CommentForm, CommentItem},
  data() {
    return {
      comments: [],
      loading: true,
      currentPage: 1,
      nextPage: null,
      previousPage: null,
      sortField: 'date',
      sortOrder: 'desc',
    };
  },
  methods: {
    // Function to update the list of comments after adding a new one
    handleNewComment() {
      this.fetchComments(this.currentPage); // Reload current page
    },
    // Comment function
    async fetchComments(page = 1) {
      this.loading = true;
      try {
        const url = `${import.meta.env.VITE_APP_API_URL}api/v1/comments/?page=${page}&ordering=${this.sortOrder}${this.sortField}`;
        const response = await fetch(url);
        const data = await response.json();

        // Logging data for debugging
        console.log('API Response:', data);

        // Update the status
        this.comments = data.results || [];
        this.nextPage = data.next ? page + 1 : null;
        this.previousPage = data.previous ? page - 1 : null;
        this.currentPage = page;
      } catch (error) {
        console.error('Error fetching comments:', error);
        this.comments = [];
      } finally {
        this.loading = false;
      }
    },
    // Page switch handler
    goToPage(page) {
      if (page < 1) return; // Protection against incorrect page

      // Updating the route (URL)
      this.$router.push({query: {page}});
      this.fetchComments(page); // Add a fetchComments call with the correct page
    },
  },
  watch: {
    // Monitoring the change in the "page" parameter in the URL
    '$route.query.page': {
      immediate: true,
      handler(newPage) {
        const page = Number(newPage) || 1; // Convert to a number, default 1
        this.fetchComments(page);
      },
    },
  },
};

</script>

<style scoped>
.pagination {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

button {
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

span {
  font-size: 14px;
}
</style>
