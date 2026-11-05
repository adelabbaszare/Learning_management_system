const { defineConfig } = require('@vue/cli-service')

const isProduction = process.env.NODE_ENV === 'production'

module.exports = defineConfig({
  // This repository is published as a project site, not a user/organization site.
  publicPath: isProduction ? '/Learning_management_system/' : '/',
  outputDir: 'dist',
  assetsDir: 'assets',
  productionSourceMap: false,
  transpileDependencies: true
})
