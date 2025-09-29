export default {
  presets: [['@babel/preset-env', {targets: {node: 'current'}}]],
  plugins: [
    ['module-resolver', {
      root: ['./'],
      alias: {
        '@js': '../authors/static/authors/js'
      }
    }]
  ]
};