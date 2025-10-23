<template>
  <div class="signup">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Sign Up</h1>

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

                    <div class="field">
                        <lable>Repeat Password</lable>
                        <div class="control">
                            <input type="password" class="input"></input>
                        </div>
                    </div>


                    <div class="filed">
                        <div class="control">
                            <div class="button is-dark">Sign Up</div>
                        </div>
                    </div>

                </form>

                <hr>
                Or <router-link to="/log-in">Click Here</router-link> to log in!
            </hr>
            </div>
        </div>
      </div>
    </section>
  </div>
</template>
