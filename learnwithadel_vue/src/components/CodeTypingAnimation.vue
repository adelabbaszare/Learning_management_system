<template>
  <div class="code-container">
    <div class="code-window">
      <div class="code-header">
        <div class="traffic-lights">
          <div class="dot red"></div>
          <div class="dot yellow"></div>
          <div class="dot green"></div>
        </div>
        <div class="file-name"></div>
      </div>

      <div class="code-body">
        <pre>
          <code class="language-javascript direction-ltr" v-html="highlightedCode"></code><span class="cursor"></span>
        </pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CodeTypingAnimation",
  data() {
    return {
      codeSnippet:
    `const coder = {
    name: 'Adel Zare',
    skills: ['Python', 'Django', 'React'],
    hardWorker: true,
    problemSolver: true,
    hireable: function() {
        return (
        this.hardWorker &&
        this.problemSolver &&
        this.skills.length >= 5
        );
    }
};`,
      typedCode: '',
      intervalId: null,
      timeoutId: null,
    };
  },
  computed: {
    highlightedCode() {
      return this.highlightCode(this.typedCode);
    },
  },
  mounted() {
    this.startAnimation();
  },
  beforeDestroy() {
    clearInterval(this.intervalId);
    clearTimeout(this.timeoutId);
  },
  methods: {
    startAnimation() {
      let i = 0;
      this.typedCode = ''; 
      
      const animateTyping = () => {
        if (i < this.codeSnippet.length) {
          this.typedCode += this.codeSnippet.charAt(i);
          i++;
        } else {
          clearInterval(this.intervalId);
          this.timeoutId = setTimeout(this.startAnimation, 5000); // مکث 5 ثانیه‌ای بعد از اتمام
          return;
        }
      };

      this.intervalId = setInterval(animateTyping, 40); 
    },

    highlightCode(code) {
      // تغییرات برای تم IDE (One Dark / VS Code style)
      const highlighted = code.replace(
        /\b(const|function|return|this)\b|'([^']*)'|\b(true|false|null|5)\b|(\w+)(?=:)|([{}();,])|(&&|>=|:)/g,
        (match, keyword, string, boolean, key, punctuation, operator) => {
          if (keyword !== undefined) {
            if (keyword === 'this') return `<span class="token-this">${keyword}</span>`;
            return `<span class="token-keyword">${keyword}</span>`;
          }
          if (string !== undefined) return `<span class="token-string">'${string}'</span>`;
          if (boolean !== undefined) return `<span class="token-boolean">${boolean}</span>`;
          if (key !== undefined) return `<span class="token-key">${key}</span>`; // کلیدهای آبجکت
          if (punctuation !== undefined) return `<span class="token-punctuation">${punctuation}</span>`;
          if (operator !== undefined) return `<span class="token-operator">${operator}</span>`;
          return match;
        }
      );
      // هایلایت براکت‌ها و نام تابع
      return highlighted
             .replace(/ = /g, ' <span class="token-operator">=</span> ')
             .replace(/hireable/g, '<span class="token-function">hireable</span>'); 
    },
  },
};
</script>

<style scoped>
/* 1. کانتینر اصلی */
.code-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  width: 100%;
}

/* 2. پنجره کد (شبیه VS Code) */
.code-window {
  width: 100%;
  max-width: 600px; /* عرض مناسب */
  background-color: #282c34; /* رنگ پس زمینه One Dark */
  border-radius: 8px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  overflow: hidden;
  font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
}

/* هدر پنجره */
.code-header {
  display: flex;
  align-items: center;
  background-color: #21252b;
  padding: 10px 15px;
  border-bottom: 1px solid #181a1f;
}

.traffic-lights {
  display: flex;
  gap: 8px;
}
.dot { width: 12px; height: 12px; border-radius: 50%; }
.red { background-color: #ff5f56; }
.yellow { background-color: #ffbd2e; }
.green { background-color: #27c93f; }

.file-name {
  margin-left: 20px;
  color: #abb2bf;
  font-size: 0.8rem;
  opacity: 0.6;
}

/* بدنه کد */
.code-body {
  padding: 20px;
  background-color: #282c34;
  
  /* !!! حل مشکل پرش !!! */
  height: 380px; /* ارتفاع ثابت: باعث می‌شود صفحه بالا پایین نرود */
  overflow-y: auto; /* اگر متن بیشتر شد اسکرول بخورد */
  
  /* !!! حل مشکل راست‌چین !!! */
  direction: ltr !important;
  text-align: left !important;
}

pre {
  margin: 0;
  background: transparent;
  color: #abb2bf; /* رنگ پیش‌فرض متن */
  font-size: 15px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.cursor {
  display: inline-block;
  width: 8px;
  height: 18px;
  background-color: #528bff;
  vertical-align: middle;
  margin-left: 2px;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

::v-deep .token-keyword { color: #c678dd; font-weight: bold; } /* بنفش (const, function) */
::v-deep .token-this { color: #e06c75; font-style: italic; }   /* قرمز (this) */
::v-deep .token-string { color: #98c379; }   /* سبز (رشته‌ها) */
::v-deep .token-boolean { color: #d19a66; }  /* نارنجی (true) */
::v-deep .token-key { color: #e5c07b; }      /* زرد (نام ویژگی‌ها) */
::v-deep .token-function { color: #61afef; } /* آبی (نام توابع) */
::v-deep .token-punctuation { color: #abb2bf; } /* خاکستری (پرانتز و کاما) */
::v-deep .token-operator { color: #56b6c2; } /* فیروزه‌ای (=, &&) */

</style>