var webpackBaseConfig = require('./webpack.config.js');
var extended = webpackBaseConfig();

extended.devServer = {
  open: true,
  progress : false,
  port : 8081,
  inline : true,
  openPage: 'build/index.html',
  publicPath: '',
};


extended.optimization = {
  ...extended.optimization,
  removeAvailableModules: false,
  removeEmptyChunks: false,
};

extended.devtool = 'source-map';

module.exports = extended;