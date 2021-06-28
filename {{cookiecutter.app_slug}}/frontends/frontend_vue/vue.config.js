const path = require("path");

module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        logLevel: 'debug',
        pathRewrite: { '^/api': '/' },
      },
    },
  },
  outputDir: path.resolve(__dirname, "build/"),
  assetsDir: "."
}
