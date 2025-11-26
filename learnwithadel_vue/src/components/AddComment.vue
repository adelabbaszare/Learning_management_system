<template>
  <form @submit.prevent="submitComment">
    <div class="field">
      <label class="label">Name</label>
      <div class="control">
        <input
          type="text"
          class="input"
          v-model="comment.name"
          :disabled="isAuthenticated" 
          :placeholder="isAuthenticated ? fullName : 'Enter your name'"
        />
      </div>
    </div>

    <div class="field">
      <label class="label">Content</label>
      <div class="control">
        <textarea class="textarea" v-model="comment.content"></textarea>
      </div>
    </div>

    <div class="field">
      <div class="control">
        <button type="submit" class="button is-link">Submit</button>
      </div>
    </div>
  </form>
</template>


<script>
import axios from 'axios'

export default {
  props: [
    'course', 
    'activeLesson',
    'currentUser', 
    'isAuthenticated'
  ],
  data() {
    return {
      comment: {
        name: '',
        content: '',
      },
      errors: []
    }
  },
  computed: {
    fullName() {
      if (this.currentUser && this.currentUser.first_name) {
        return `${this.currentUser.first_name} ${this.currentUser.last_name || ''}`.trim()
      }
      if (this.currentUser && this.currentUser.username) {
        return this.currentUser.username
      }
      return ''
    }
  },
  watch: {
    isAuthenticated: {
        immediate: true,
        handler(newVal) {
            this.setCommentName(newVal);
        }
    },
    currentUser: {
        deep: true,
        handler(newVal) {
            this.setCommentName(this.isAuthenticated);
        }
    }
  },
  methods: {
    setCommentName(isAuthenticated) {
        if (isAuthenticated && this.fullName) {
            this.comment.name = this.fullName
        } else if (!isAuthenticated) {
            this.comment.name = ''
        }
    },

    async submitComment() {
      console.log('submitComment called', { comment: this.comment, activeLesson: this.activeLesson, course: this.course })

      if (!this.course || !this.course.slug) {
        alert('Course not loaded correctly.')
        return
      }
      if (!this.activeLesson || !this.activeLesson.slug) {
        alert('Please select a lesson first.')
        return
      }
      if (!this.comment.content) {
          alert('Please fill the content field.')
          return
      }
      if (!this.isAuthenticated && !this.comment.name) {
          alert('Please enter your name.')
          return
      }

      const url = `courses/${this.$route.params.slug}/lessons/${this.activeLesson.slug}/comments/`
      console.log('POST URL:', url)

      const token = localStorage.getItem('token')
      const headers = { 'Content-Type': 'application/json' }
      if (token) headers['Authorization'] = 'Token ' + token

      try {
        const resp = await axios.post(url, this.comment, { headers })
        console.log('comment created:', resp.data)

        // reset form
        this.comment.name = this.isAuthenticated ? this.fullName : ''
        this.comment.content = ''

        this.$emit('submitComment', resp.data)

        alert('The comment was added!')

      } catch (err) {
        console.error('Failed to submit comment:', err, err?.response?.data)
        if (err.response) {
          alert('Server error: ' + JSON.stringify(err.response.data))
        } else {
          alert('Network error while submitting comment.')
        }
      }
    }
  }
}
</script>