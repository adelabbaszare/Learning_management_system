<template>
  <!-- استفاده از ساختار Card جدید مورد نظر شما -->
  <div class="card mb-5">
    
    <header class="card-header">
      <!-- نمایش شماره سوال -->
      <p class="card-header-title is-size-4 has-text-light">
        سوال {{ questionIndex + 1 }} از {{ totalQuestions }}:
      </p>
    </header>

    <div class="card-content">
      <div class="content">
        
        <!-- 1. استفاده از v-html برای نمایش سؤال (که اکنون RichText است) -->
        <!-- محتوای Rich Text سوال -->
        <div class="quiz-question mb-5 content" v-html="quiz.question"></div>

        <!-- 2. بخش پاسخ‌ها -->
        <div class="control">
          <!-- تکرار بر روی گزینه‌های شافل شده -->
          <label 
            v-for="(option, index) in shuffledOptions" 
            :key="index"
            class="radio option-label"
            :class="getOptionClass(option)"
            @click="selectOption(option)"
          >
            <!-- توجه: v-model مستقیماً به selectedAnswer متصل است -->
            <input 
              type="radio" 
              :name="'quiz-' + quiz.id" 
              v-model="selectedAnswer" 
              :value="option"
              :disabled="submitted"
              class="mr-3"
            >
            <span class="ml-2">{{ option }}</span>
          </label>
        </div>

        <!-- پیام انتخاب نشدن گزینه -->
        <p v-if="submitAttempted && !selectedAnswer" class="help is-danger mt-3 ">
          لطفاً یک گزینه را انتخاب کنید
        </p>

        <!-- 3. نتایج (پس از ثبت) -->
        <div v-if="submitted" class="mt-4">
          <div v-if="quizResult === 'correct'" class="notification is-success is-light has-text-weight-bold">
            ✅ آفرین! پاسخ شما صحیح بود
          </div>
          <div v-if="quizResult === 'incorrect'" class="notification is-danger is-light has-text-weight-bold">
            ❌ متاسفانه پاسخ اشتباه بود
            <br>
            <strong>پاسخ صحیح:</strong> {{ quiz.answer }}
          </div>
        </div>

      </div>
    </div>

    <!-- 4. دکمه‌های اقدام (Footer) -->
    <footer class="card-footer">
      <a 
        href="#" 
        class="card-footer-item button is-info" 
        v-if="!submitted" 
        @click.prevent="submitQuiz"
      >
        بررسی پاسخ
      </a>
      
      <a 
        href="#" 
        class="card-footer-item button is-link" 
        v-if="submitted" 
        @click.prevent="nextQuestion"
      >
        {{ (questionIndex + 1) < totalQuestions ? 'سوال بعدی ←' : 'مشاهده نتایج' }}
      </a>
    </footer>
  </div>
</template>

<script>
import hljs from 'highlight.js';

export default {
  props: {
    quiz: {
      type: Object,
      required: true
    },
    questionIndex: {
      type: Number,
      required: true
    },
    totalQuestions: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      selectedAnswer: null, 
      submitted: false, 
      quizResult: null,
      submitAttempted: false,
      shuffledOptions: [], // برای نگهداری گزینه‌های شافل شده
    }
  },
  mounted() {
    // فراخوانی هایلایت کد پس از رندر شدن محتوای HTML داینامیک
    this.$nextTick(() => {
      // این خط برای پردازش تگ‌های <code> جدیدی که توسط v-html تزریق شده‌اند ضروری است.
      hljs.highlightAll(); 
    });
  },
  created() {
    this.shuffleOptions();
  },
  watch: {
    // هر بار که پرآپ quiz تغییر کند (سوال جدید لود شود)، وضعیت را ریست و گزینه‌ها را دوباره به هم می‌ریزد
    quiz: {
      handler() {
        this.resetQuizState();
        this.shuffleOptions();
        
        // اطمینان از هایلایت مجدد هنگام تغییر سؤال
        this.$nextTick(() => {
            hljs.highlightAll();
        });
      },
      deep: true,
    }
  },
  methods: {
    shuffleOptions() {
      let options = this.quiz.options || [];

      options = options.filter(o => o !== null && o !== '' && typeof o !== 'undefined');
      options = [...new Set(options)]; // حذف تکرارها

      for (let i = options.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [options[i], options[j]] = [options[j], options[i]];
      }

      this.shuffledOptions = options;
      },

    selectOption(option) {
    if (!this.submitted) {
        this.selectedAnswer = option;
        }
    },

    submitQuiz() {
      this.submitAttempted = true;

      if (!this.selectedAnswer) {
        return;
      }

      this.submitted = true;
      
      const isCorrect = this.selectedAnswer === this.quiz.answer;
      this.quizResult = isCorrect ? 'correct' : 'incorrect';
    },

    getOptionClass(option) {
      // کلاس‌های مربوط به هاور و انتخاب (قبل از ثبت)
      let classes = '';
      if (!this.submitted) {
          classes += ' has-cursor-pointer';
          if (option === this.selectedAnswer) {
              classes += ' selected'; 
          }
          return classes;
      }
      
      // کلاس‌های مربوط به نمایش نتیجه (بعد از ثبت)
      if (option === this.quiz.answer) {
          return 'correct-answer-style'; // پاسخ صحیح
      }
      if (option === this.selectedAnswer && this.quizResult === 'incorrect') {
          return 'incorrect-answer-style'; // پاسخ غلط انتخابی کاربر
      }
      // گزینه‌های دیگر پس از ثبت، بدون استایل خاص
      return 'submitted-default'; // برای جلوگیری از استایل‌های ناخواسته
    },

    nextQuestion() {
      if (!this.submitted) return;

      const isCorrect = this.quizResult === 'correct';
      this.$emit('next', isCorrect); // ارسال وضعیت پاسخ به والد (Course.vue)

      this.resetQuizState();
    },

    resetQuizState() {
      this.selectedAnswer = null;
      this.submitted = false;
      this.quizResult = null;
      this.submitAttempted = false;
    }
  }
}
</script>

<style scoped>
/* **رفع باگ‌های استایل و بازگرداندن Hover اصلی** */

.has-cursor-pointer {
    cursor: pointer;
}

.option-label {
    font-size: 1rem;
    font-weight: 500;
    display: flex; 
    align-items: center;
    padding: 0.75em 2em;
    margin-bottom: 1em;
    border-radius: 8px;
    border: 1.4px solid #930dd1;
    transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    background-color: #fcfcfc;
    box-shadow: 0 4px 6px rgba(101, 6, 104, 0.1); 
    color: #4a4a4a; /* رنگ متن پیش‌فرض برای خوانایی */
}

.option-label[disabled] {
    cursor: default;
    opacity: 0.8; /* کمی کاهش شفافیت برای گزینه‌های غیرفعال */
}

.option-label:active {
    transform: scale(0.99);
}

.option-label.selected {
    background-color: #820db8; 
    color: white; /* متن سفید برای گزینه انتخاب شده */
    border: 1.5px solid #ffffff;
    box-shadow: 0 4px 8px rgba(147, 13, 209, 0.6);
}

.option-label input[type="radio"] {
    /* اطمینان از نمایش رادیو باتن */
    margin-right: 0.5rem;
    flex-shrink: 0; /* جلوگیری از کوچک شدن دکمه رادیویی */
}

/* **رفع باگ رنگ خاکستری:** اطمینان از رنگ متن مناسب */
.correct-answer-style {
    border: 2px solid #48c78e !important;
    background-color: #e6ffed !important;
    color: #1c743c !important; /* رنگ سبز تیره برای متن صحیح */
    font-weight: bold;
}

.incorrect-answer-style {
    border: 2px solid #f14668 !important;
    background-color: #fff0f3 !important;
    color: #943343 !important; /* رنگ قرمز تیره برای متن اشتباه */
    font-weight: bold;
}

/* استایل برای گزینه‌های دیگر پس از ثبت (فقط برای جلوگیری از استایل‌های ناخواسته) */
.submitted-default {
    opacity: 0.6;
}


/* تضمین می‌کنیم که استایل‌های highlight.js اعمال شوند */
.quiz-question.content code {
    white-space: pre-wrap;
    word-break: break-word;
}
</style>