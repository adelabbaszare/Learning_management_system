<template>
  <div
    class="card course-card"
    tabindex="0"
    @keydown.enter="goToCourse"
    @click="goToCourse"
    :aria-label="`Open course ${course.title}`"
  >
    <!-- image + overlays -->
    <div class="card-image">
      <figure class="image is-4by3 image-wrapper">
        <img :src="imageSrc" :alt="course.title" />

        <!-- duration badge (top-left) with FontAwesome clock -->
        <div class="duration-badge">
          <span class="tag is-small is-light duration-tag">
            <font-awesome-icon :icon="faClock" class="clock-icon" />
            <span class="duration-text">{{ activeDuration }}</span>
          </span>
        </div>

        <!-- category tags (top-right) -->
        <div class="category-tags" v-if="categoryTags.length">
          <span
            v-for="(tag, idx) in categoryTags"
            :key="`cat-${course.id || idx}-${idx}`"
            class="tag is-info is-light is-small category-tag"
          >
            {{ tag }}
          </span>
        </div>

        <!-- overlay actions on hover -->
        <div class="image-overlay">
          <div class="overlay-actions">
            <button class="button is-small is-primary" @click.stop="goToCourse">
              <span class="icon"><i class="fas fa-eye" aria-hidden="true"></i></span>
              <span>View</span>
            </button>
            <button class="button is-small is-info" @click.stop="enroll">
              <span class="icon"><i class="fas fa-book-open" aria-hidden="true"></i></span>
              <span>Enroll</span>
            </button>
          </div>
        </div>
      </figure>
    </div>

    <!-- card content (Bulma card body) -->
    <div class="card-content">
      <div class="media">
        <!-- media-left: circular image placeholder for author (Bulma pattern) -->
        <div class="media-left">
          <figure class="image is-48x48 author-image-figure">
            <img :src="authorImageSrc" :alt="authorTitle" />
          </figure>
        </div>

        <div class="media-content">
          <p class="title is-5">{{ course.title }}</p>
          <p class="subtitle is-6 has-text-grey">{{ authorTitle }}</p>
        </div>
      </div>

      <div class="content">
        <p class="desc">{{ truncatedDescription }}</p>

        <div class="meta is-flex is-justify-content-space-between is-align-items-center mt-3">
          <div class="meta-left">
            <div class="rating">
              <span v-for="n in 5" :key="n" class="star">
                <i
                  class="fas"
                  :class="n <= Math.round(activeRating) ? 'fa-star' : 'fa-star-o'"
                  aria-hidden="true"
                ></i>
              </span>
              <small class="has-text-grey">{{ activeRating.toFixed(1) }}</small>
            </div>
          </div>
        </div>

        <div class="card-footer mt-3">
          <router-link
            class="card-footer-item"
            :to="{ name: 'Course', params: { slug: course.slug } }"
            @click.stop
          >
            Details
          </router-link>
          <a class="card-footer-item" @click.stop.prevent="enroll">Enroll</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// اگر قبلاً FontAwesome را گلوبال نصب نکردی، اینجا اضافه کن:
import { library } from '@fortawesome/fontawesome-svg-core'
import { faClock } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faClock)

export default {
  name: "CourseItem",
  components: {
    FontAwesomeIcon
  },
  props: {
    course: { type: Object, required: true },
    fallbackImage: { type: String, default: "https://bulma.io/assets/images/placeholders/1280x960.png" },
    authorPlaceholder: { type: String, default: "https://bulma.io/assets/images/placeholders/96x96.png" }
  },
  data() {
    return {
      randomRating: 0,
      randomDuration: "",
      faClock // expose icon to template
    };
  },
  created() {
    this.randomRating = +(3 + Math.random() * 2).toFixed(1);
    const minutes = Math.floor(20 + Math.random() * 160);
    if (minutes < 60) this.randomDuration = `${minutes}m`;
    else {
      const h = Math.floor(minutes / 60);
      const m = minutes % 60;
      this.randomDuration = m ? `${h}h ${m}m` : `${h}h`;
    }
  },
  computed: {
    imageSrc() {
      return this.course.get_image || this.course.image || this.fallbackImage;
    },
    truncatedDescription() {
      const text = this.course.short_description || this.course.long_description || "";
      const max = 120;
      if (text.length <= max) return text;
      return text.slice(0, max).trim() + "...";
    },
    activeRating() {
      const r = this.course.rating;
      if (r === 0 || r === null || typeof r === "undefined" || isNaN(Number(r))) return this.randomRating;
      return Number(r);
    },
    activeDuration() {
      // اگر بک‌اند فیلد duration را نداد، از مقدار تصادفی استفاده کن
      return this.course.duration || this.randomDuration;
    },
    // categories as array of strings (titles). fallback: "Category #id" when only ids present.
    categoryTags() {
      const cats = this.course.categories;
      if (!cats) return [];
      if (Array.isArray(cats) && cats.length > 0) {
        return cats.map(c => {
          if (typeof c === "object") return c.title || c.name || `Category #${c.id || ''}`;
          if (/^\d+$/.test(String(c))) return `Category #${c}`;
          return String(c);
        });
      }
      if (typeof cats === "object") return [cats.title || cats.name || `Category #${cats.id || ''}`];
      if (/^\d+$/.test(String(cats))) return [`Category #${cats}`];
      return [String(cats)];
    },
    authorTitle() {
      const u = this.course.created_by;
      if (!u) return "";
      const name = [u.first_name, u.last_name].filter(Boolean).join(" ");
      return name || u.username || `User #${u.id || ""}`;
    },
    authorImageSrc() {
      const u = this.course.created_by || {};
      return u.avatar || u.image || u.profile_image || this.authorPlaceholder;
    }
  },
  methods: {
    goToCourse() {
      if (this.course && this.course.slug) {
        this.$router.push({ name: 'Course', params: { slug: this.course.slug } }).catch(()=>{})
      }
    },
    enroll() {
      this.$emit("enroll", this.course);
    },
  },
};
</script>

<style scoped>
.course-card {
  cursor: pointer;
  transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
  outline: none;
  border: 2px solid transparent;
  border-radius: 8px;
}
.course-card:focus,
.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 28px rgba(10,10,10,0.12), 0 6px 12px rgba(10,10,10,0.08);
  border-color: rgb(148, 0, 211);
}

/* image wrapper */
.image-wrapper {
  position: relative;
  overflow: hidden;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}

/* duration badge (top-left) */
.duration-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 60;
}
.duration-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding-left: 8px;
  padding-right: 8px;
  border-radius: 999px;
  background: rgba(255,255,255,0.94);
  color: #222;
  font-weight: 600;
}
.clock-icon { color: rgb(148, 0, 211); }

/* category tags (top-right) */
.category-tags {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 60;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.category-tag {
  background: rgba(255,255,255,0.95);
  color: #222;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 0.75rem;
}

/* overlay - hidden by default */
.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(10,10,10,0.0) 0%, rgba(0,0,0,0.46) 100%);
  opacity: 0;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 1rem;
  transition: opacity 200ms ease, transform 200ms ease;
  z-index: 50;
  pointer-events: none;
}
.course-card:hover .image-overlay,
.course-card:focus .image-overlay,
.course-card:focus-within .image-overlay {
  opacity: 1;
  pointer-events: auto;
}

/* overlay actions */
.overlay-actions {
  width: 100%;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}
.overlay-actions .button {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 150ms ease, transform 150ms ease;
}
.course-card:hover .overlay-actions .button,
.course-card:focus .overlay-actions .button {
  opacity: 1;
  transform: translateY(0);
}

/* author image (circular) */
.author-image-figure img {
  border-radius: 50%;
  object-fit: cover;
  width: 48px;
  height: 48px;
}

/* truncate description */
.desc {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* rating style */
.rating .star { margin-right: 3px; color: #ffdd57; }
.rating i.fas.fa-star-o { color: rgba(0,0,0,0.12); }

/* card footer */
.card-footer { border-top: 1px solid rgba(10,10,10,0.05); }
.card-footer-item { cursor: pointer; }
</style>
