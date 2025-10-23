<template>
  <div class="login">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Log In</h1>

      </div>
    </div>
    <section class="section">
      <div class="container">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <form>
                    <div class="field">
                        <lable>Email</lable>
                        <div class="control">
                            <input type="email" class="input"></input>
                        </div>
                    </div>

                    <div class="field">
                        <lable>Password</lable>
                        <div class="control">
                            <input type="password" class="input"></input>
                        </div>
                    </div>

                    <div class="filed">
                        <div class="control">
                            <div class="button is-dark">Log in</div>
                        </div>
                    </div>

                </form>

                <hr>
                Or <router-link to="/sign-up">Click Here</router-link> to Sign Up!
            </hr>
            </div>
        </div>
      </div>
    </section>
  </div>
</template>
