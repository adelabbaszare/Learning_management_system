<template>
  <nav class="navbar is-info" role="navigation" aria-label="main navigation" style="min-height: 5rem;">
    <div class="navbar-brand">
      <a class="navbar-item is-size-4" href="/">LearnwithAdel</a>
    </div>

    <div id="navbar-item" class="navbar-menu">
      <div class="navbar-start">
        <a class="navbar-item">Home</a>
        <a class="navbar-item">About</a>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-primary"><strong>Sign Up</strong></a>
            <a class="button is-light">Log in</a>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <router-view/>

  <footer class="footer">
    <div class="content has-text-centered">
      <p class="made-by">
        Made with <span class="purple-heart">💜</span> by Adel
      </p>
      <p>
        © 2025 <strong>LearnwithAdel</strong>. All rights reserved.
      </p>
    </div>
  </footer>
</template>

<style lang="scss">
@import '../node_modules/bulma';

// انیمیشن قلب بنفش
@keyframes heartbeat {
  0%, 20%, 40%, 60%, 80%, 100% {
    transform: scale(1);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: scale(1.3);
  }
}

.purple-heart {
  display: inline-block;
  color: purple;
  animation: heartbeat 4s infinite;
}

.made-by {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}
</style>