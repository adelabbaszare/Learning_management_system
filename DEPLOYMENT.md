# Frontend deployment

The Vue 3 application in `learnwithadel_vue/` is published as a static GitHub Pages project site:

**https://adelabbaszare.github.io/Learning_management_system/**

## Deployment workflow

- GitHub Actions builds the frontend when changes are pushed to `main`, and validates pull requests targeting `main`.
- The build runs `npm ci` and `npm run build` from `learnwithadel_vue/`.
- Only the generated `learnwithadel_vue/dist/` directory is uploaded to GitHub Pages.
- Deployment is restricted to pushes or manual runs on `main`. Pull requests can build but cannot deploy.
- The workflow uses the `github-pages` environment and the short-lived GitHub Actions OIDC token. No personal access token or long-lived deployment secret is required.

## GitHub Pages setting

In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.

## Django API configuration

GitHub Pages hosts static files only; it does not run Django, Python, a database, or background workers. Host the Django REST API separately over HTTPS.

If the API is hosted at a different origin, add a repository Actions **variable** named `VUE_APP_API_URL` with the public API base URL, including the API prefix, for example:

```text
https://api.example.com/api/v1/
```

Configure this under **Settings → Secrets and variables → Actions → Variables**. The workflow injects this value at build time. It is a public endpoint, not a secret. Never put passwords, private keys, Django secret keys, database credentials, or privileged API tokens in `VUE_APP_*` variables: frontend build values are visible to every site visitor.

The Django deployment must:
- serve the API over HTTPS;
- allow the Pages origin `https://adelabbaszare.github.io` in its CORS configuration;
- configure allowed hosts and CSRF trusted origins for the actual API host when applicable;
- enforce authentication and authorization on the server for every protected endpoint.

If `VUE_APP_API_URL` is unset, the frontend uses the relative fallback `/api/v1/`. This is useful only when an API is served from the same origin; GitHub Pages itself does not provide that API.

## Routing and base path

The Vue CLI production build uses `/Learning_management_system/` as its public base path. Vue Router uses hash history so deep links and refreshes work on static hosting without a server-side rewrite rule.
