<template>
    <div class="card mb-5">
        <header class="card-header">
            <p class="card-header-title is-size-4">
                سوال {{ questionIndex + 1 }} از {{ totalQuestions }}: {{ quiz.question }}
            </p>
        </header>

        <div class="card-content">
            <div class="content">
                <div class="control">
                    <label 
                        v-for="(option, index) in quiz.options" 
                        :key="index"
                        class="radio option-label"
                        :class="getOptionClass(option)"
                        :disabled="submitted"
                    >
                        <input 
                            type="radio" 
                            :name="quiz.question" 
                            v-model="selectedAnswer" 
                            :value="option"
                            :disabled="submitted"
                        >
                        {{ option }}
                    </label>
                </div>

                <p v-if="submitAttempted && !selectedAnswer" class="help is-danger mt-3 ">
                    لطفاً یک گزینه را انتخاب کنید
                </p>

                <div v-if="submitted" class="mt-4">
                    <div v-if="quizResult === 'correct'" class="notification is-success is-light">
                        ✅ آفرین! پاسخ شما صحیح بود
                    </div>
                    <div v-if="quizResult === 'incorrect'" class="notification is-danger is-light">
                        ❌ متاسفانه پاسخ اشتباه بود
                        <br>
                        <strong>پاسخ صحیح:</strong> {{ quiz.answer }}
                    </div>
                </div>
            </div>
        </div>

        <footer class="card-footer">
            <a 
                href="#" 
                class="card-footer-item button is-info" 
                v-if="!submitted" 
                @click.prevent="submitQuiz"
            >
                ثبت پاسخ
            </a>
            
            <a 
                href="#" 
                class="card-footer-item button is-link" 
                v-if="submitted" 
                @click.prevent="nextQuestion"
            >
                <!-- متن دکمه بسته به اینکه سوال بعدی وجود دارد یا خیر تغییر می‌کند -->
                {{ (questionIndex + 1) < totalQuestions ? 'سوال بعدی ←' : 'مشاهده نتایج' }}
            </a>
        </footer>
    </div>
</template>

<script>
export default {
    props: {
        quiz: {
            type: Object,
            required: true
        },
        questionIndex: { // جدید: برای نمایش شماره سوال
            type: Number,
            required: true
        },
        totalQuestions: { // جدید: برای نمایش تعداد کل سوالات
            type: Number,
            required: true
        }
    },
    data() {
        return {
            selectedAnswer: '',
            submitted: false,      
            quizResult: null,    
            submitAttempted: false 
        }
    },
    watch: {
        // ریست کردن وضعیت کوییز هنگام تغییر سوال
        quiz: {
            handler() {
                this.selectedAnswer = '';
                this.submitted = false;
                this.quizResult = null;
                this.submitAttempted = false;
            },
            deep: true
        }
    },
    methods: {
        submitQuiz() {
            this.submitAttempted = true;

            if (!this.selectedAnswer) {
                return;
            }

            this.submitted = true;
            
            // چک کردن پاسخ
            const isCorrect = this.selectedAnswer === this.quiz.answer;
            this.quizResult = isCorrect ? 'correct' : 'incorrect';
        },
        
        getOptionClass(option) {
            
            if (!this.submitted) {
                let classes = 'has-cursor-pointer';
                if (option === this.selectedAnswer) {
                    
                    classes += ' selected'; 
                }
                return classes;
            }
            if (option === this.quiz.answer) {
                return 'has-text-success has-text-weight-bold correct-answer-style'; 
            }
            if (option === this.selectedAnswer && this.quizResult === 'incorrect') {
                return 'has-text-danger incorrect-answer-style'; 
            }
            return '';
        },

        nextQuestion() {
            // ارسال نتیجه (درست یا غلط بودن) به کامپوننت والد
            const isCorrect = this.quizResult === 'correct';
            this.$emit('next', isCorrect);

            // ریست کردن وضعیت در کامپوننت والد انجام می‌شود
            this.selectedAnswer = '';
            this.submitted = false;
            this.quizResult = null;
            this.submitAttempted = false;
        }
    }
}
</script>

<style scoped>

.has-cursor-pointer {
    cursor: pointer;
}

.option-label {
    font-size: 1rem;
    font-weight: 500;
    display: block;
    padding: 0.75em 2em;
    margin-bottom: 1em;
    border-radius: 8px;
    border: 1.4px solid #930dd1;
    transition: background-color 0.2s ease;
    background-color: #fcfcfc;
    box-shadow: 0 4px 6px rgba(101, 6, 104, 0.522);
}

.option-label:not([disabled]):hover {
    background-color: #ffffff;
    cursor: pointer;
    border: 1.8px solid #930dd1;
}

.option-label[disabled]:hover {
    cursor: pointer;
    background-color: transparent;
    border: 1.8px solid #ffffff;
}

.option-label:active {
    transform: scale(0.98);
}

.option-label.selected {
    background-color: #930dd1; /* A distinct blue for selected items */
    color: white;
    border: 1.5px solid #ffffff;
}

.correct-answer-style {
    border: 2px solid #48c78e;
    background-color: #f6fdf9;
}

.incorrect-answer-style {
    border: 2px solid #f14668;
    background-color: #fff5f7;
}

/* اصلاح استایل‌های Bulma برای وضوح بیشتر */
.has-text-success.has-text-weight-bold {
    /* از کلاس‌های Bulma برای تغییر رنگ متن در اینجا جلوگیری می‌شود
       و از کلاس‌های سفارشی استفاده می‌شود تا استایل صحیح اعمال شود */
}

.has-text-danger {
    /* از کلاس‌های Bulma برای تغییر رنگ متن در اینجا جلوگیری می‌شود
       و از کلاس‌های سفارشی استفاده می‌شود تا استایل صحیح اعمال شود */
}
</style>