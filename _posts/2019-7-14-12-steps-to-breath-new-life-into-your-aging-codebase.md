---
layout: post
title: 12 Steps to Breath New Life into Your Aging Codebase
author: Liam Bellows
---

# Intro

Note: My intention is not to put down the current codebase but to identify specific reasons why I did what I did. I understand how sometimes even good coders can end up with a non-optimal solution due to things evolving over years and years.

Before we get started, how about some background? I was recently staffed to a project that was using some dated technology such as _Razor pages_ and _Telerik UI_ and _Jquery_ for front end. Besides that, the javascript was either inline the Razor view or all stuck in a single javascript file. All together, this led to problems such as many postbacks, missing code features (ES5 only), and overall tedious and sluggish development in order to support IE.

My goal was to create a proper build system, make development easier, provide a better end user experience, and make the solution more future ready while reusing existing tech choices where possible. I also wanted to do this without the major risk and time commitment a complete rewrite/refactor would include -- it would basically be transparent to existing devs, QA and UAT teams. So how did I do this? Here we go!

# 1. Create the Build Process

I want to focus on the techniques to achieve this more so than the exact commands and code in order to keep this post a reasonable length. In the future I may add some more detail but hopefully this will be enough to get going.

You will need to have NodeJS and NPM installed as we're trying to get away from Razor and C# in the views. Roughly stated, run these:
* npm init -y
* npm install --save-dev @babel/cli @babel/core @babel/plugin-proposal-class-properties @babel/preset-env babel-loader browser-sync browser-sync-webpack-plugin webpack webpack-cli webpack-notifier

Add the following to your `package.json`:

```json
"scripts": {
    "dev": "webpack --mode development --watch",
    "build": "webpack"
}
```

Create a `webpack.config.js` at the root and add the following:

```javascript
var path = require("path");
var WebpackNotifierPlugin = require("webpack-notifier");
var BrowserSyncPlugin = require("browser-sync-webpack-plugin");

module.exports = {
    entry: "./src/index.js",
    output: {
        path: path.resolve(__dirname, "./dist"),
        filename: "bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }
        ]
    },
    devtool: "inline-source-map",
    plugins: [new WebpackNotifierPlugin(), new BrowserSyncPlugin()]
};
```

Create a `.babelrc` file and add:

```json
{ 
  "presets": ["@babel/preset-env"], 
  "plugins": ["@babel/plugin-proposal-class-properties"] 
}
```

All of this should allow you to use ES6+ and all the cool stuff newer browsers are letting you do in Javascript and let it run in IE. Your JS should also be minified which is great for speed!

# 2. Create a Folder Struture

All of the previous files were created at the root. You will want to add at least two more folders **src** and **dist** where you source files and compiled JS files will reside, respectively.  My source folder has an `index.js` at the root where everything is imported. This is called the entry point. I created JS files for each page that posted back. I also created files or subfolders for utils and each feature I was creating to make everything obvious.

# 3. Add Your JS to Your Page Layout/Masterpage

I would add the script include to your minimized JS file (`./dist/bundle.js` if using the JSON from the first step) right after any previous custom and vendor JS.  You can also create another vendor JS bundle via webpack code splitting if you want things to be even better.

Also, I created a new CSS file and added that after all previous CSS files so that I can override effectively and also keep it separate.

# 4. Set up the Entry Point File with a State Object

This is the main JS file which will bridge the gap between what you're developing and the existing code base.  Everything will be imported into here and we'll set up some other things.

Let's say my client is the "Super Cool Corporation".  I will add the following to my entry point that will create our main state object.

```javascript
window['SCC'] = window['SCC'] || {}
```

This is a concept taken from React and we'll use it here to basically build a React Lite (yes, I know about Preact) using mostly just Jquery to keep things simple. The main difference here is that we need to repopulate the state on each postback and rebuild the object properties using the server code and injecting it into our front end. We avoid global namespace poplution by keeping everything wrapped up in the state object. Note, we use a string accessor for SCC to avoid any type of property renaming that could occur in the webpack build process. This will also give you more flexibility over just exporting the SCC if you need to split the SCC instantiating between locations.

# 5. Wire-up Some Events

This will allow us to execute our compiled code in the Razor pages whenever we need to. Add a `home.js` file to your src directory. Paste in the following:

```javascript
export function loaded(){
  console.log('hello world')
}
```

Then modify your entry JS file adding the below:

```javascript
import * as home from './home'
window['SCC']['home'] = window['SCC']['home'] || home
```

# 6. Call From the View Page

Here we will access our state object and we will have access to anything exported from the home.js file.  Edit your .cshtml or .aspx file and add the following at the bottom before the `</body>` tag:

```html
<script>
  $(function() {
    SCC.home.loaded()
  })
</script>
```

Using the Jquery ready function, this will call our loaded function once the page is loaded and we don't pollute the view page with extra code that we may need to use on load. Note, we still need to continue using the old ES5 standard in our view pages if we want it to work with IE. Things like arrow functions will not work, even with a polyfill, since its considered a syntax error.

# 7. Build and Test

Congrats! You have the basic example complete. To build, you should be able to run `npm run dev` in the root where your package.json file is. This will build the JS code and also watch for changes. Whenever you save a JS file again, the code will recompile.

Load up the browser (if it didn't load automatically via browsersync) and check the console where you should see *hello world*.

# 8. Inject the Data Model and ViewBag

If you have a server side driven view, you will want to inject all the data you may need to use into your state object. Note, you will want to make sure this isn't private data and it is OK to have exposed on the front end. Open your page layout/masterpage and add something like the following:

```html

```

Note, make sure this is after where your bundle is included but before your `SCC.home.loaded()` events and such.


# TBD ... some more things to do...

# Great, what now?

This is a great technique if you're taking over an old project and want to add new features and fixes that will minimize side effects. When something goes wrong and it isn't your fault, you can clearly point to the new code you've added and it will be cleanly seperated from the archaic stuff. It also avoids breaking something that **was** working because there is a variable in the JS file that is used somewhere in a view you weren't expecting.

This seemed like a bit of work but think about all the benefits we received: access to ES6 and beyond, a package manager, code splitting, better organization, minification... the list goes on! Even for newer developers, this should only take one workday at max to setup and you can build the rest as you go. How you want to extend this will depend on your needs and the needs of your client.

```javascript
Code
```