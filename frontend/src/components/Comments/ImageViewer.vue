<template>
  <div v-if="visible" class="image-viewer" @click.self="closeViewer">
    <img :src="imageSrc" alt="Full-size Image" />
    <button @click="closeViewer" class="close-btn">×</button>
  </div>
</template>

<script>
export default {
  props: {
    imageSrc: {
      type: String,
      required: true,
    },
    visible: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    closeViewer() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.image-viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.image-viewer img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 5px;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  color: white;
  font-size: 30px;
  cursor: pointer;
}
</style>
