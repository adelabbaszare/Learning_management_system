<template>
  <Nav/>

  <router-view/>

  <Footer/>
</template>

<script>
  import Footer from './components/Footer.vue';
  import Nav from '@/components/Nav.vue'
  export default {
    name: 'App',
    components: {
      Nav,
      Footer
    }
  }
</script>


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