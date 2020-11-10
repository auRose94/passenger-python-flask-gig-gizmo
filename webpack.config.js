const path = require('path');

let optimization = {
    usedExports: true,
    removeEmptyChunks: true,
    mergeDuplicateChunks: true,
    splitChunks: {
        cacheGroups: {
            commons: {
                test: /[\\/]node_modules[\\/]/,
                name: 'vendors',
                chunks: 'all'
            }
        }
    }
};

let performance = {
    maxAssetSize: 1000000,
    maxEntrypointSize: 1000000
};

let entry = {
    "index": "./frontend/index.ts"
};

let rules = [{
    test: /\.tsx?$/,
    use: 'ts-loader',
    exclude: /node_modules/,
}, {
    test: /\.(scss)$/,
    use: [{
        loader: 'style-loader', // inject CSS to page
    }, {
        loader: 'css-loader', // translates CSS into CommonJS modules
    }, {
        loader: 'postcss-loader', // Run post css actions
        options: {
            postcssOptions: function() { // post css plugins, can be exported to postcss.config.js
                return {
                    plugins: [
                        require('precss'),
                        require('autoprefixer')
                    ]
                };
            }
        }
    }, {
        loader: 'sass-loader' // compiles Sass to CSS
    }]
}, {
    test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
    use: [{
        loader: 'file-loader',
        options: {
            name: '[name].[ext]',
            publicPath: "/static/fonts",
            outputPath: 'static/fonts'
        }
    }]
}];

let extensions = ['.tsx', '.ts', '.js'];

module.exports = [{
        //Debug
        mode: "development",
        entry,
        module: {
            rules,
        },
        resolve: {
            extensions,
        },
        output: {
            filename: './static/js/[name].js',
            path: path.resolve(__dirname),
        },
        optimization
    },
    {
        mode: "production",
        devtool: "source-map",
        entry,
        module: {
            rules,
        },
        resolve: {
            extensions,
        },
        output: {
            filename: './static/js/[name].min.js',
            path: path.resolve(__dirname),
        },
        optimization,
        performance
    }
];