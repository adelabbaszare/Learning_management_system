<template>
  <article class="media box comment-box">
    <figure class="media-left">
      <p class="image is-64x64">
        <img 
          class="is-rounded" 
          :src="userImage" 
          :alt="comment.name"
        >
      </p>
    </figure>

    <div class="media-content">
      <div class="content">
        <div class="is-flex is-justify-content-space-between is-align-items-center mb-2">
          <div>
            <strong>{{ comment.name }}</strong>
            <span v-if="comment.role" class="tag is-info is-light ml-2 is-rounded is-small">
              {{ comment.role }}
            </span>
          </div>
          <small class="has-text-grey-light is-size-7">{{ formattedDate }}</small>
        </div>

        <p class="has-text-light">
          {{ comment.content }}
        </p>
      </div>

      <nav class="level is-mobile mt-3">
        <div class="level-left">
          <a class="level-item" aria-label="reply">
            <span class="icon is-small mr-1">
              <i class="fas fa-reply"></i> </span>
            <span class="is-size-7">پاسخ</span>
          </a>
          <a class="level-item" aria-label="like">
            <span class="icon is-small mr-1">
              <i class="far fa-heart"></i>
            </span>
            <span class="is-size-7">پسندیدن</span>
          </a>
        </div>
      </nav>
    </div>
  </article>
</template>

<script>
export default {
  name: 'CourseComment',
  props: {
    comment: {
      type: Object,
      required: true,
      validator: (obj) => 'name' in obj && 'content' in obj
    }
  },
  computed: {
    userImage() {
      if (this.comment.image) {
        return this.comment.image;
      }

      return `https://ui-avatars.com/api/?name=${encodeURIComponent(this.comment.name)}&background=random&color=fff`;
    },

    formattedDate() {
      if (!this.comment.created_at) return '';

      return new Date(this.comment.created_at).toLocaleDateString('fa-IR'); 
    }
  }
}
</script>

<style scoped>
.comment-box {
  transition: all 0.3s ease;
  border: 1px solid #f5f5f5;
}

.comment-box:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1); 
  border-color: transparent;
}

.is-rounded {
  object-fit: cover;
}
</style>