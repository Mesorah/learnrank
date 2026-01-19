export default {
  presets: [['@babel/preset-env', {targets: {node: 'current'}}]],
  plugins: [
    ['module-resolver', {
      root: ['./'],
      alias: {
        '@jsAuthors': '../authors/static/authors/js',
      }
    }]
  ]
};