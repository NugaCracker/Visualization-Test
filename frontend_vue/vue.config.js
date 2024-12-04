const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8081', // Flask 서버 주소
        changeOrigin: true,
      },
    },
  },
};